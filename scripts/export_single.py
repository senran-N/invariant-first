#!/usr/bin/env python3
"""Build a single-entry runtime package and publish it after validation.

Nested entrypoints become GUIDE.md resources. The source is never edited;
conversion happens in a temporary sibling directory, not the final target.
"""
from __future__ import annotations
import argparse
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from route import ROOT, RoutingError, validate_config
from catalog import render, render_entrypoint


def export(source: Path, destination: Path) -> Path:
    source, destination = source.resolve(), destination.resolve()
    if destination == source or destination.is_relative_to(source) or source.is_relative_to(destination):
        raise RoutingError("Export destination must be separate from the source tree")
    if destination.exists():
        raise RoutingError("Export destination already exists; use a new, empty location")
    cfg = json.loads((source / "config/routing.json").read_text(encoding="utf-8"))
    validate_config(cfg, source)
    mapping: dict[str, str] = {}
    for entry in cfg["routes"] + cfg["specialists"]:
        old = entry["path"]
        new = str(Path(old).with_name("GUIDE.md")).replace("\\", "/")
        if new in mapping.values() or (new != old and (source / new).exists()):
            raise RoutingError(f"Export resource collision: {new}")
        mapping[old] = new
    ignore = shutil.ignore_patterns(".git", ".hg", ".svn", ".github", "__pycache__", "*.pyc", ".pytest_cache")
    for directory, dirs, files in os.walk(source, followlinks=False):
        excluded = ignore(directory, dirs + files)
        dirs[:] = [name for name in dirs if name not in excluded]
        for name in dirs + [name for name in files if name not in excluded]:
            if (Path(directory) / name).is_symlink():
                raise RoutingError("Export expects a self-contained package without symlinks")

    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f".{destination.name}-", dir=destination.parent) as temp:
        staged = Path(temp) / "package"
        shutil.copytree(source, staged, ignore=ignore)
        for entry in cfg["routes"] + cfg["specialists"]:
            old = entry["path"]
            new = mapping[old]
            if old != new:
                (staged / old).rename(staged / new)
            entry["path"] = new
            metadata = (staged / new).parent / "agents"
            if metadata.is_dir():
                shutil.rmtree(metadata)
        for path in staged.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".json"}:
                text = path.read_text(encoding="utf-8")
                for old, new in mapping.items():
                    text = text.replace(old, new)
                text = text.replace("skills/if-*/SKILL.md", "skills/if-*/GUIDE.md")
                path.write_text(text, encoding="utf-8")
        (staged / "config/routing.json").write_text(
            json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        for name, content in render(cfg).items():
            (staged / name).write_text(content, encoding="utf-8")
        entrypoint = staged / "SKILL.md"
        entrypoint.write_text(render_entrypoint(cfg, entrypoint.read_text(encoding="utf-8")), encoding="utf-8")
        (staged / "EXPORT.md").write_text(
            "# Single-entry runtime export\n\nGenerated from the canonical source package. Only the root SKILL.md is discoverable; "
            "specialists are relative GUIDE.md resources with unchanged instructions. "
            "Use this form for recursive-discovery harnesses such as Pi and for single-skill importers. "
            "Do not edit this export as a second source of truth.\n", encoding="utf-8")
        validate_config(cfg, staged)
        if len(list(staged.rglob("SKILL.md"))) != 1:
            raise RoutingError("Export did not produce exactly one entrypoint")
        if destination.exists():
            raise RoutingError("Export destination appeared during preparation; use a different location")
        staged.rename(destination)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="New destination skill directory")
    args = parser.parse_args()
    try:
        print(export(ROOT, args.output))
        return 0
    except (RoutingError, OSError, json.JSONDecodeError, UnicodeError) as exc:
        print(f"export: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
