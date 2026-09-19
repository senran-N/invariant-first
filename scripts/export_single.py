#!/usr/bin/env python3
"""Export the same instructions with one SKILL.md for single-skill importers.

The canonical package retains independently addressable specialist SKILL.md files.
This exporter renames only nested entrypoints and rewrites local path references.
It never edits the source package and never calls a client or external service.
"""
from __future__ import annotations
import argparse
import json
import shutil
import sys
from pathlib import Path
from route import ROOT, RoutingError, validate_config
from catalog import render


def export(source: Path, destination: Path) -> Path:
    source, destination = source.resolve(), destination.resolve()
    if destination == source or destination.is_relative_to(source) or source.is_relative_to(destination):
        raise RoutingError("Export destination must be separate from the source tree")
    if destination.exists():
        raise RoutingError("Export destination already exists; use a new, empty location")
    cfg = json.loads((source / "config/routing.json").read_text(encoding="utf-8"))
    validate_config(cfg, source)
    for path in source.rglob("*"):
        if path.is_symlink():
            raise RoutingError("Export expects a self-contained package without symlinks")
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    mapping = {}
    for entry in cfg["routes"] + cfg["specialists"]:
        old = entry["path"]
        new = str(Path(old).with_name("GUIDE.md")).replace("\\", "/")
        mapping[old] = new
        (destination / old).rename(destination / new)
        entry["path"] = new
        metadata = (destination / new).parent / "agents"
        if metadata.is_dir():
            shutil.rmtree(metadata)
    for path in destination.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".json"}:
            text = path.read_text(encoding="utf-8")
            for old, new in mapping.items():
                text = text.replace(old, new)
            text = text.replace("skills/if-*/SKILL.md", "skills/if-*/GUIDE.md")
            path.write_text(text, encoding="utf-8")
    (destination / "config/routing.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name, content in render(cfg).items():
        (destination / name).write_text(content, encoding="utf-8")
    (destination / "EXPORT.md").write_text(
        "# Single-entry export\n\nGenerated from the canonical package. Only the root SKILL.md is discoverable; "
        "specialists are relative GUIDE.md resources with unchanged instructions. "
        "Do not edit this export as a second source of truth.\n", encoding="utf-8")
    validate_config(cfg, destination)
    if len(list(destination.rglob("SKILL.md"))) != 1:
        raise RoutingError("Export did not produce exactly one entrypoint")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="New destination skill directory")
    args = parser.parse_args()
    try:
        print(export(ROOT, args.output))
        return 0
    except (RoutingError, OSError, json.JSONDecodeError) as exc:
        print(f"export: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
