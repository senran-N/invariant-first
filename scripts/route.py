#!/usr/bin/env python3
"""Read-only, offline route selection. Python 3.10+; standard library only.

An explicit intent is a caller decision. Text matching is an advisory candidate,
not an authorization parser. This program never edits the target repository,
installs packages, starts agents, or executes a route's suggested actions.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


class RoutingError(ValueError):
    """Invalid manifest or request, reported without a Python traceback."""


def local_file(root: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or "\\" in value:
        raise RoutingError("Resource paths must be non-empty relative POSIX paths")
    rel = PurePosixPath(value)
    if rel.is_absolute() or ".." in rel.parts or ":" in value:
        raise RoutingError(f"Resource escapes the skill: {value}")
    target = (root / rel).resolve()
    if not target.is_relative_to(root.resolve()) or not target.is_file():
        raise RoutingError(f"Missing or out-of-package resource: {value}")
    return target


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RoutingError(f"Cannot read JSON from {path}: {exc}") from exc


def validate_config(cfg: Any, root: Path = ROOT) -> dict[str, Any]:
    if not isinstance(cfg, dict) or cfg.get("schema_version") != 1:
        raise RoutingError("Expected routing schema_version 1")
    required = {"version", "routes", "specialists", "priority", "fallback",
                "facts", "stages", "capabilities", "aliases", "max_support_now"}
    if not required.issubset(cfg):
        raise RoutingError(f"Missing configuration keys: {sorted(required - cfg.keys())}")
    if not isinstance(cfg["routes"], list) or not cfg["routes"]:
        raise RoutingError("routes must be a non-empty list")
    if not isinstance(cfg["specialists"], list):
        raise RoutingError("specialists must be a list")
    ids: list[str] = []
    resources: list[str] = []
    for entry in cfg["routes"] + cfg["specialists"]:
        if not isinstance(entry, dict) or not {"id", "path", "label", "action", "capabilities"}.issubset(entry):
            raise RoutingError("Each entry needs id, path, label, action and capabilities")
        if not re.fullmatch(r"[a-z][a-z0-9-]*", entry["id"]):
            raise RoutingError("Invalid route id")
        ids.append(entry["id"])
        resources.append(entry["path"])
        local_file(root, entry["path"])
        if not set(entry["capabilities"]).issubset(cfg["capabilities"]):
            raise RoutingError(f"Unknown capability for {entry['id']}")
        for rule in entry.get("rules", []):
            if not isinstance(rule.get("weight"), int):
                raise RoutingError("Rule weights must be integers")
            if not rule.get("any"):
                raise RoutingError("Each rule needs at least one any pattern")
            for key in ("any", "all", "none"):
                for pattern in rule.get(key, []):
                    try:
                        re.compile(pattern, re.IGNORECASE)
                    except (re.error, TypeError) as exc:
                        raise RoutingError(f"Invalid pattern in {entry['id']}: {exc}") from exc
        for pattern in entry.get("hints", []):
            try:
                re.compile(pattern, re.IGNORECASE)
            except (re.error, TypeError) as exc:
                raise RoutingError(f"Invalid hint in {entry['id']}: {exc}") from exc
    if len(ids) != len(set(ids)) or len(resources) != len(set(resources)):
        raise RoutingError("Route ids and resource paths must be unique")
    primary_ids = {route["id"] for route in cfg["routes"]}
    if set(cfg["priority"]) != primary_ids or len(cfg["priority"]) != len(primary_ids):
        raise RoutingError("priority must contain each primary route exactly once")
    if cfg["fallback"] not in primary_ids:
        raise RoutingError("fallback must identify a primary route")
    if not set(cfg["aliases"].values()).issubset(primary_ids):
        raise RoutingError("Aliases must point to primary routes")
    for spec in cfg["specialists"]:
        if not spec.get("when_any") or not set(spec["when_any"]).issubset(cfg["facts"]):
            raise RoutingError(f"Unknown or missing fact trigger for {spec['id']}")
    if type(cfg["max_support_now"]) is not int or cfg["max_support_now"] < 1:
        raise RoutingError("max_support_now must be a positive integer")
    return cfg


def load_config(root: Path = ROOT) -> dict[str, Any]:
    return validate_config(read_json(root / "config" / "routing.json"), root)


def normalize_request(cfg: dict[str, Any], raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise RoutingError("Request must be a JSON object")
    allowed = {"task", "intent", "sequence", "facts", "stage", "capabilities"}
    if set(raw) - allowed:
        raise RoutingError(f"Unknown request keys: {sorted(set(raw) - allowed)}")
    task = raw.get("task", "")
    if not isinstance(task, str) or not task.strip():
        raise RoutingError("task must be a non-empty string")
    route_ids = {route["id"] for route in cfg["routes"]}

    def canonical(value: Any) -> str:
        if not isinstance(value, str):
            raise RoutingError("intent and sequence entries must be strings")
        result = cfg["aliases"].get(value, value)
        if result not in route_ids:
            raise RoutingError(f"Unknown intent: {value}")
        return result

    intent = canonical(raw["intent"]) if raw.get("intent") is not None else None
    sequence_raw = raw.get("sequence", [])
    if not isinstance(sequence_raw, list):
        raise RoutingError("sequence must be a list")
    sequence = [canonical(value) for value in sequence_raw]
    if intent and sequence and intent != sequence[0]:
        raise RoutingError("Explicit intent must equal sequence[0]; pass only the remaining requested sequence")
    stage = raw.get("stage", "unknown")
    if not isinstance(stage, str) or stage not in cfg["stages"]:
        raise RoutingError("Unknown stage")
    facts = raw.get("facts", {})
    if not isinstance(facts, dict) or set(facts) - set(cfg["facts"]):
        raise RoutingError("facts must use names from config/routing.json")
    if any(type(value) is not bool for value in facts.values()):
        raise RoutingError("Facts must be JSON booleans, not guesses, strings or numbers")
    caps = raw.get("capabilities")
    if caps is not None and (not isinstance(caps, list) or
                             any(not isinstance(x, str) for x in caps) or
                             not set(caps).issubset(cfg["capabilities"])):
        raise RoutingError("capabilities must be a list of supported semantic capability names")
    return {"task": task.strip(), "intent": intent, "sequence": sequence,
            "stage": stage, "facts": facts, "capabilities": caps}


def candidate_text(task: str) -> str:
    # A narrow reduction of quoted-code false positives, not a security boundary.
    text = re.sub(r"```.*?```", " ", task, flags=re.DOTALL)
    text = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith(">"))
    return re.sub(r"\s+", " ", text).strip()


def text_candidates(cfg: dict[str, Any], task: str) -> list[dict[str, Any]]:
    text = candidate_text(task)
    scores: list[dict[str, Any]] = []
    priority = {name: index for index, name in enumerate(cfg["priority"])}
    for route in cfg["routes"]:
        hits = []
        for index, rule in enumerate(route.get("rules", [])):
            has = lambda pattern: re.search(pattern, text, re.IGNORECASE) is not None
            if (any(has(p) for p in rule["any"]) and
                    all(has(p) for p in rule.get("all", [])) and
                    not any(has(p) for p in rule.get("none", []))):
                hits.append({"rule": index, "weight": rule["weight"]})
        if hits:
            scores.append({"id": route["id"], "weight": max(h["weight"] for h in hits),
                           "matched_rules": [h["rule"] for h in hits]})
    return sorted(scores, key=lambda x: (-x["weight"], priority[x["id"]]))


def select_route(cfg: dict[str, Any], raw: Any) -> dict[str, Any]:
    request = normalize_request(cfg, raw)
    routes = {route["id"]: route for route in cfg["routes"]}
    candidates = text_candidates(cfg, request["task"])
    if request["intent"]:
        route_id, selection = request["intent"], "explicit-intent"
    elif request["sequence"]:
        route_id, selection = request["sequence"][0], "explicit-sequence"
    elif candidates:
        route_id, selection = candidates[0]["id"], "text-candidate"
    else:
        route_id, selection = cfg["fallback"], "fallback"
    route = routes[route_id]
    support = []
    suggested = []
    for spec in cfg["specialists"]:
        active = [fact for fact in spec["when_any"] if request["facts"].get(fact) is True]
        if active:
            support.append({"id": spec["id"], "path": spec["path"], "facts": active,
                            "action": spec["action"]})
        elif any(re.search(p, candidate_text(request["task"]), re.IGNORECASE)
                 for p in spec.get("hints", [])):
            suggested.append({"id": spec["id"], "path": spec["path"],
                              "status": "text-hint-only; confirm relevant facts before loading"})
    limit = cfg["max_support_now"]
    preferred = list(route["capabilities"])
    for selected in support:
        spec = next(s for s in cfg["specialists"] if s["id"] == selected["id"])
        preferred.extend(cap for cap in spec["capabilities"] if cap not in preferred)
    available = request["capabilities"]
    missing = None if available is None else [cap for cap in preferred if cap not in available]
    next_routes = [{"id": item, "path": routes[item]["path"]}
                   for item in request["sequence"][1:]]
    return {
        "schema_version": 1, "config_version": cfg["version"],
        "task": request["task"], "route_id": route_id, "PRIMARY": route["path"],
        "selection": selection, "reason": route["intent"],
        "needs_intent_check": selection in {"text-candidate", "fallback"},
        "ACTION": route["action"], "DONE": route["done"],
        "stage": request["stage"], "stage_policy": cfg["stages"][request["stage"]],
        "facts": request["facts"], "SUPPORT": support,
        "LOAD_NOW": [route["path"]] + [s["path"] for s in support[:limit]],
        "DEFERRED": support[limit:], "SUGGESTED_SUPPORT": suggested,
        "CAPABILITIES": {"preferred": preferred, "available": available, "missing": missing,
                         "guide": "references/runtime.md"},
        "NEXT": next_routes, "CANDIDATES": candidates,
        "authorization": "No permission is inferred or granted; follow the actual user and host scope.",
        "side_effects": "none: this command only reads the skill and prints a routing decision"
    }


def text_output(result: dict[str, Any]) -> str:
    lines = [f"PRIMARY -> {result['PRIMARY']}",
             f"Selection: {result['selection']} | intent-check: {result['needs_intent_check']}",
             f"Reason: {result['reason']}", f"ACTION: {result['ACTION']}",
             "LOAD_NOW: " + ", ".join(result["LOAD_NOW"]),
             "DEFERRED: " + (", ".join(s["path"] for s in result["DEFERRED"]) or "none"),
             "NEXT (requested only): " + (", ".join(s["id"] for s in result["NEXT"]) or "none")]
    if result["CAPABILITIES"]["missing"]:
        lines.append("Missing capabilities: " + ", ".join(result["CAPABILITIES"]["missing"]))
    lines.append(result["authorization"])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--task", help="Current user goal; raw text matching remains advisory")
    source.add_argument("--request", help="JSON request path; '-' reads stdin")
    parser.add_argument("--intent", help="Explicit, semantically chosen primary route")
    parser.add_argument("--facts", help="Comma-separated confirmed positive facts")
    parser.add_argument("--stage", choices=["preview", "adopted", "unknown"])
    parser.add_argument("--capabilities", help="Comma-separated actual capabilities; empty means none")
    parser.add_argument("--format", choices=["json", "text"], default="json")
    args = parser.parse_args()
    try:
        cfg = load_config()
        if args.request:
            raw = json.load(sys.stdin) if args.request == "-" else read_json(Path(args.request))
            if not isinstance(raw, dict):
                raise RoutingError("Request must be an object")
        else:
            raw = {"task": args.task}
        if args.intent is not None:
            raw["intent"] = args.intent
        if args.stage is not None:
            raw["stage"] = args.stage
        if args.facts is not None:
            raw["facts"] = {item.strip(): True for item in args.facts.split(",") if item.strip()}
        if args.capabilities is not None:
            raw["capabilities"] = [item.strip() for item in args.capabilities.split(",") if item.strip()]
        result = select_route(cfg, raw)
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.format == "json" else text_output(result))
        return 0
    except (RoutingError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"route: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
