#!/usr/bin/env python3
"""Generate human-readable routing views from the single manifest."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from route import ROOT, RoutingError, load_config


def cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render(cfg: dict) -> dict[str, str]:
    lines = ["# MASTER-ROUTING", "",
             "Generated from `config/routing.json`; edit the manifest, not this table.", "",
             "## PRIMARY", "",
             "Choose the current deliverable, not every keyword in a full specification. Explicit intent wins.",
             "For text candidates: highest matching rule weight wins; ties use the listed priority.",
             "A text candidate always needs an intent check. No route grants permission to act.", "",
             "| Priority | ID | Deliverable / intent | Open now | First action |",
             "| --- | --- | --- | --- | --- |"]
    by_id = {r["id"]: r for r in cfg["routes"]}
    for pos, route_id in enumerate(cfg["priority"], 1):
        route = by_id[route_id]
        lines.append(f"| {pos} | {route_id} | {cell(route['intent'])} | [{route['label']}]({route['path']}) | {cell(route['action'])} |")
    lines += ["", f"No useful text match: provisional `{cfg['fallback']}`; resolve from the user's goal, not guesswork.",
              "Use explicit `--intent` or the equivalent semantic choice; do not ask the user to choose a routing menu.", "",
              "## SUPPORT", "",
              "Load only for confirmed facts. Text hints are suggestions, not facts.",
              f"Start with up to {cfg['max_support_now']} relevant specialists; remaining matches stay visible in DEFERRED.",
              "Load a deferred specialist before working on its boundary; deferred does not mean waived.", "",
              "| ID | Confirmed facts | Open when needed | Action |",
              "| --- | --- | --- | --- |"]
    for spec in cfg["specialists"]:
        facts = "; ".join(cfg["facts"][f] for f in spec["when_any"])
        lines.append(f"| {spec['id']} | {cell(facts)} | [{spec['label']}]({spec['path']}) | {cell(spec['action'])} |")
    lines += ["", "## STAGE", "", "Stage adjusts obligations; it is not another pipeline.", ""]
    lines += [f"- **{stage}**: {description}" for stage, description in cfg["stages"].items()]
    lines += ["", "## NEXT / CAPABILITIES", "",
              "NEXT is only the remaining user-requested sequence. It is never inferred as an authorization.",
              "Missing capabilities use [runtime](references/runtime.md); no auto-installation or model switching.",
              "Selection, instruction loading, implementation and observed execution remain separate facts.", ""]
    index = ["# INDEX", "", "Generated from `config/routing.json`. This is a map, not a reading checklist.", "",
             "| Kind | ID | Module | Preferred capabilities |", "| --- | --- | --- | --- |"]
    for kind, entries in [("PRIMARY", cfg["routes"]), ("SUPPORT", cfg["specialists"])]:
        for entry in entries:
            index.append(f"| {kind} | {entry['id']} | [{entry['label']}]({entry['path']}) | {', '.join(entry['capabilities'])} |")
    index += ["", "## Facts accepted by the router", ""]
    index += [f"- `{key}`: {value}" for key, value in cfg["facts"].items()]
    index += ["", "## Read on demand", "",
              "- [Rules](RULES.md): shared action, architecture and delivery constraints.",
              "- [Runtime adaptation](references/runtime.md): only when execution is blocked.",
              "- [Experience](experience/README.md): scoped learning without global self-modification.",
              "- [Pain-point research](references/ai-coding-pain-points.md): provenance, not runtime overhead.",
              "- [Source lessons](references/source-lessons.md): inherited repository lessons.", ""]
    return {"MASTER-ROUTING.md": "\n".join(lines), "INDEX.md": "\n".join(index)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail on drift, without writing")
    args = parser.parse_args()
    try:
        outputs = render(load_config())
        drift = []
        for name, content in outputs.items():
            path = ROOT / name
            if args.check:
                if not path.is_file() or path.read_text(encoding="utf-8") != content:
                    drift.append(name)
            else:
                path.write_text(content, encoding="utf-8")
                print(f"Generated {name}")
        if drift:
            print("Generated-file drift: " + ", ".join(drift), file=sys.stderr)
            return 1
        if args.check:
            print("Catalog matches routing.json")
        return 0
    except (OSError, RoutingError) as exc:
        print(f"catalog: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
