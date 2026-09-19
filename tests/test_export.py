"""Single-entry publication and resource preservation contracts."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import export_single
from route import RoutingError, load_config


def snapshot(root):
    return {str(p.relative_to(root)): p.read_bytes()
            for p in root.rglob("*") if p.is_file()}


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.parent = Path(self.temp.name)
        self.source = self.parent / "source"
        self.dest = self.parent / "runtime"
        shutil.copytree(ROOT, self.source,
                        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        self.cfg = load_config(self.source)

    def assert_no_output(self):
        self.assertFalse(self.dest.exists())
        self.assertEqual(list(self.parent.glob(".runtime-*")), [])

    def test_repository_automation_is_not_exported(self):
        workflow = self.source / ".github" / "workflows" / "validate.yml"
        workflow.parent.mkdir(parents=True, exist_ok=True)
        workflow.write_text("name: source-only\n", encoding="utf-8")
        result = export_single.export(self.source, self.dest)
        self.assertFalse((result / ".github").exists())

    def test_existing_resource_is_not_overwritten(self):
        entry = self.cfg["routes"][1]
        guide = self.source / Path(entry["path"]).with_name("GUIDE.md")
        # In a runtime source this is the registered method, not a collision.
        # Relocate it first to exercise the same conversion contract.
        original = self.source / entry["path"]
        if original == guide:
            renamed = original.with_name("METHOD.md")
            original.rename(renamed)
            entry["path"] = renamed.relative_to(self.source).as_posix()
            (self.source / "config/routing.json").write_text(json.dumps(self.cfg), encoding="utf-8")
        guide.write_text("Existing supplementary guide.\n", encoding="utf-8")
        before = snapshot(self.source)
        with self.assertRaisesRegex(RoutingError, "resource collision"):
            export_single.export(self.source, self.dest)
        self.assertEqual(snapshot(self.source), before)
        self.assert_no_output()

    def test_two_methods_cannot_publish_the_same_resource(self):
        for entry, name in zip(self.cfg["routes"][:2], ["FIRST.md", "SECOND.md"]):
            target = self.source / "methods" / name
            target.parent.mkdir(exist_ok=True)
            (self.source / entry["path"]).rename(target)
            entry["path"] = target.relative_to(self.source).as_posix()
        (self.source / "config/routing.json").write_text(json.dumps(self.cfg), encoding="utf-8")
        before = snapshot(self.source)
        with self.assertRaisesRegex(RoutingError, "resource collision"):
            export_single.export(self.source, self.dest)
        self.assertEqual(snapshot(self.source), before)
        self.assert_no_output()

    def test_failed_render_is_clean_and_retryable(self):
        entrypoint = self.source / "SKILL.md"
        good = entrypoint.read_text(encoding="utf-8")
        entrypoint.write_text(good.replace("<!-- END ROUTE MAP -->", ""), encoding="utf-8")
        before = snapshot(self.source)
        with self.assertRaisesRegex(RoutingError, "marker pair"):
            export_single.export(self.source, self.dest)
        self.assert_no_output()
        self.assertEqual(snapshot(self.source), before)
        entrypoint.write_text(good, encoding="utf-8")
        result = export_single.export(self.source, self.dest)
        self.assertEqual(result, self.dest)
        self.assertEqual(list(result.rglob("SKILL.md")), [result / "SKILL.md"])
        load_config(result)

    def test_copy_failure_removes_only_staged_files(self):
        before = snapshot(self.source)
        def interrupted(source, target, **kwargs):
            target.mkdir()
            shutil.copy2(source / "RULES.md", target / "RULES.md")
            raise OSError("simulated storage failure")
        with patch.object(export_single.shutil, "copytree", side_effect=interrupted):
            with self.assertRaises(OSError):
                export_single.export(self.source, self.dest)
        self.assert_no_output()
        self.assertEqual(snapshot(self.source), before)

    def test_destination_is_published_after_validation(self):
        before = snapshot(self.source)
        validate = export_single.validate_config
        observed_staging = []
        def inspect(cfg, root):
            if root != self.source:
                observed_staging.append(root)
                self.assertFalse(self.dest.exists())
                self.assertEqual(list(root.rglob("SKILL.md")), [root / "SKILL.md"])
            return validate(cfg, root)
        with patch.object(export_single, "validate_config", side_effect=inspect):
            export_single.export(self.source, self.dest)
        self.assertEqual(len(observed_staging), 1)
        self.assertFalse(observed_staging[0].exists())
        self.assertEqual(snapshot(self.source), before)
        self.assertTrue(self.dest.is_dir())
        self.assertEqual(list(self.parent.glob(".runtime-*")), [])

    def test_destination_created_during_preparation_is_preserved(self):
        render = export_single.render_entrypoint
        def intervening_writer(cfg, text):
            result = render(cfg, text)
            self.dest.mkdir()
            (self.dest / "owned.txt").write_text("Other writer's work.\n", encoding="utf-8")
            return result
        with patch.object(export_single, "render_entrypoint", side_effect=intervening_writer):
            with self.assertRaisesRegex(RoutingError, "appeared during preparation"):
                export_single.export(self.source, self.dest)
        self.assertEqual(snapshot(self.dest), {"owned.txt": b"Other writer's work.\n"})
        self.assertEqual(list(self.parent.glob(".runtime-*")), [])

    def test_cli_conversion_failure_reports_no_success_path(self):
        entrypoint = self.source / "SKILL.md"
        text = entrypoint.read_text(encoding="utf-8")
        entrypoint.write_text(text.replace("<!-- END ROUTE MAP -->", ""), encoding="utf-8")
        result = subprocess.run([sys.executable, str(self.source / "scripts/export_single.py"),
                                 "--output", str(self.dest)], capture_output=True,
                                text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("marker pair", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assert_no_output()


if __name__ == "__main__":
    unittest.main()
