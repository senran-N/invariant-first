"""Resource-map contracts, independent of model intent selection."""
from __future__ import annotations

import copy
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from catalog import ROUTE_MAP_START, ROUTE_MAP_END, render_entrypoint
from export_single import export
from route import RoutingError, load_config


class ResourceMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = load_config(ROOT)
        cls.text = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    def map_paths(self, text):
        block = text.split(ROUTE_MAP_START, 1)[1].split(ROUTE_MAP_END, 1)[0]
        return re.findall(r"\]\(([^)]+)\)", block)

    def copy_source(self, target):
        shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))

    def test_entrypoint_matches_all_registered_paths(self):
        self.assertEqual(self.text, render_entrypoint(self.cfg, self.text))
        expected = [entry["path"] for entry in self.cfg["routes"] + self.cfg["specialists"]]
        self.assertEqual(self.map_paths(self.text), expected)
        self.assertTrue(all((ROOT / path).is_file() for path in expected))

    def test_paths_follow_registration_not_naming_conventions(self):
        cfg = copy.deepcopy(self.cfg)
        original = cfg["routes"][1]["path"]
        cfg["routes"][1]["path"] = "resources/implementation.md"
        result = render_entrypoint(cfg, self.text)
        self.assertIn("resources/implementation.md", self.map_paths(result))
        self.assertNotIn(original, self.map_paths(result))
        self.assertEqual(result, render_entrypoint(cfg, result))

    def test_generated_update_preserves_authored_prose(self):
        cfg = copy.deepcopy(self.cfg)
        cfg["routes"][0]["label"] = "Updated label"
        result = render_entrypoint(cfg, self.text)
        self.assertEqual(result.partition(ROUTE_MAP_START)[0], self.text.partition(ROUTE_MAP_START)[0])
        self.assertEqual(result.partition(ROUTE_MAP_END)[2], self.text.partition(ROUTE_MAP_END)[2])

    def test_invalid_marker_boundaries_fail(self):
        for text in ["", ROUTE_MAP_START, ROUTE_MAP_END + ROUTE_MAP_START,
                     self.text + ROUTE_MAP_START, self.text + ROUTE_MAP_END]:
            with self.subTest(text=text[-60:]):
                with self.assertRaises(RoutingError):
                    render_entrypoint(self.cfg, text)

    def test_runtime_map_and_router_survive_relocation(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = export(ROOT, Path(tmp) / "profile with spaces" / "invariant-first")
            cfg = load_config(dest)
            text = (dest / "SKILL.md").read_text(encoding="utf-8")
            expected = [entry["path"] for entry in cfg["routes"] + cfg["specialists"]]
            self.assertEqual(self.map_paths(text), expected)
            self.assertTrue(all((dest / path).is_file() for path in expected))
            self.assertTrue(all(path.endswith("/GUIDE.md") for path in expected))
            self.assertEqual(text, render_entrypoint(cfg, text))
            self.assertEqual(list(dest.rglob("SKILL.md")), [dest / "SKILL.md"])
            cwd = Path(tmp) / "unrelated workspace"
            cwd.mkdir()
            result = subprocess.run([sys.executable, str(dest / "scripts/route.py"),
                                     "--task", "Implement requested capability", "--intent", "build"],
                                    cwd=cwd, text=True, encoding="utf-8", capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            chosen = json.loads(result.stdout)["PRIMARY"]
            self.assertIn(chosen, expected)
            self.assertEqual(list(cwd.iterdir()), [])

    def test_export_regenerates_stale_entrypoint_after_resource_rename(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            self.copy_source(source)
            cfg = copy.deepcopy(self.cfg)
            entry = cfg["routes"][1]
            old = entry["path"]
            renamed = "methods/implementation/METHOD.md"
            (source / renamed).parent.mkdir(parents=True)
            (source / old).rename(source / renamed)
            entry["path"] = renamed
            (source / "config/routing.json").write_text(json.dumps(cfg), encoding="utf-8")
            # The authored root still has the previous generated map.
            dest = export(source, Path(tmp) / "runtime")
            emitted = load_config(dest)
            text = (dest / "SKILL.md").read_text(encoding="utf-8")
            self.assertEqual(self.map_paths(text), [e["path"] for e in emitted["routes"] + emitted["specialists"]])
            self.assertNotIn(old, self.map_paths(text))
            self.assertTrue(all((dest / p).is_file() for p in self.map_paths(text)))

    def test_catalog_check_detects_entrypoint_drift_without_editing(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            self.copy_source(source)
            entrypoint = source / "SKILL.md"
            text = entrypoint.read_text(encoding="utf-8")
            text = text.replace(self.cfg["routes"][0]["path"], "resources/obsolete.md")
            entrypoint.write_text(text, encoding="utf-8")
            result = subprocess.run([sys.executable, str(source / "scripts/catalog.py"), "--check"],
                                    capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("SKILL.md", result.stderr)
            self.assertEqual(entrypoint.read_text(encoding="utf-8"), text)

    def test_missing_registered_resource_is_reported_not_created(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = export(ROOT, Path(tmp) / "runtime")
            cfg = load_config(dest)
            missing = dest / cfg["routes"][1]["path"]
            missing.unlink()
            with self.assertRaisesRegex(RoutingError, "Missing or out-of-package resource"):
                load_config(dest)
            self.assertFalse(missing.exists())
