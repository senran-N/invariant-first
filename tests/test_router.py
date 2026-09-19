"""Deterministic router tests. These are not LLM-quality measurements."""
from __future__ import annotations
import copy
import importlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from route import RoutingError, load_config, normalize_request, select_route, validate_config
from catalog import render
from export_single import export


class RouterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = load_config(ROOT)
        cls.cases = json.loads((ROOT / "tests/route-cases.json").read_text(encoding="utf-8"))

    def test_routing_fixtures(self):
        for case in self.cases:
            with self.subTest(case=case["name"]):
                result = select_route(self.cfg, case["request"])
                for field, expected in case["expect"].items():
                    if field == "support":
                        actual = [x["id"] for x in result["SUPPORT"]]
                    elif field == "deferred":
                        actual = [x["id"] for x in result["DEFERRED"]]
                    elif field == "next":
                        actual = [x["id"] for x in result["NEXT"]]
                    elif field == "missing":
                        actual = result["CAPABILITIES"]["missing"]
                    else:
                        actual = result[field]
                    self.assertEqual(actual, expected, (case["name"], field, result))
                self.assertTrue((ROOT / result["PRIMARY"]).is_file())

    def test_no_fact_inference_from_hints(self):
        result = select_route(self.cfg, {"task": "Fix a concurrency bug"})
        self.assertEqual(result["SUPPORT"], [])
        self.assertIn("state", [x["id"] for x in result["SUGGESTED_SUPPORT"]])
        self.assertTrue(result["needs_intent_check"])

    def test_requested_sequence_only(self):
        result = select_route(self.cfg, {"task": "Build and deploy everything", "intent": "build"})
        self.assertEqual(result["NEXT"], [])
        self.assertIn("No permission", result["authorization"])

    def test_all_confirmed_support_retained(self):
        result = select_route(self.cfg, {"task": "Implement the feature", "intent": "build",
                                         "facts": {key: True for key in self.cfg["facts"]}})
        self.assertEqual(len(result["SUPPORT"]), len(self.cfg["specialists"]))
        paths = result["LOAD_NOW"][1:] + [x["path"] for x in result["DEFERRED"]]
        self.assertEqual(paths, [x["path"] for x in result["SUPPORT"]])

    def test_reject_invalid_requests(self):
        bad = [None, {}, {"task": ""}, {"task": "x", "intent": "unknown"},
               {"task": "x", "sequence": "build"},
               {"task": "x", "intent": "fix", "sequence": ["build", "release"]},
               {"task": "x", "facts": {"shared_state": "true"}},
               {"task": "x", "facts": {"shared_state": 1}},
               {"task": "x", "facts": {"invented": True}},
               {"task": "x", "stage": "production-ready"},
               {"task": "x", "capabilities": ["imaginary-tool"]},
               {"task": "x", "auth_granted": True}]
        for request in bad:
            with self.subTest(request=request):
                with self.assertRaises(RoutingError):
                    normalize_request(self.cfg, request)

    def test_manifest_resource_boundaries(self):
        for value in ["../outside.md", "/etc/passwd", "C:/outside.md", "missing.md"]:
            with self.subTest(path=value):
                cfg = copy.deepcopy(self.cfg)
                cfg["routes"][0]["path"] = value
                with self.assertRaises(RoutingError):
                    validate_config(cfg, ROOT)

    def test_manifest_priority_and_patterns(self):
        cfg = copy.deepcopy(self.cfg)
        cfg["priority"].pop()
        with self.assertRaises(RoutingError):
            validate_config(cfg, ROOT)
        cfg = copy.deepcopy(self.cfg)
        cfg["routes"][0]["rules"][0]["any"] = ["["]
        with self.assertRaises(RoutingError):
            validate_config(cfg, ROOT)

    def test_catalog_is_single_source(self):
        for name, expected in render(self.cfg).items():
            self.assertEqual((ROOT / name).read_text(encoding="utf-8"), expected)

    def test_cli_has_no_project_side_effects(self):
        with tempfile.TemporaryDirectory() as cwd:
            result = subprocess.run([sys.executable, str(ROOT / "scripts/route.py"),
                                     "--task", "Fix the error", "--intent", "fix"],
                                    cwd=cwd, text=True, encoding="utf-8", capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["route_id"], "fix")
            self.assertEqual(list(Path(cwd).iterdir()), [])

    def test_cli_invalid_request_fails_cleanly(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/route.py"), "--request", "-"],
                                input='{"task":"x","auth_granted":true}', text=True,
                                encoding="utf-8", capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_single_entry_export_keeps_semantics(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = export(ROOT, Path(temp) / "invariant-first")
            self.assertEqual(len(list(dest.rglob("SKILL.md"))), 1)
            exported_cfg = load_config(dest)
            for case in self.cases:
                a = select_route(self.cfg, case["request"])
                b = select_route(exported_cfg, case["request"])
                self.assertEqual(a["route_id"], b["route_id"])
                self.assertEqual([s["id"] for s in a["SUPPORT"]], [s["id"] for s in b["SUPPORT"]])
                self.assertTrue((dest / b["PRIMARY"]).is_file())
            result = subprocess.run([sys.executable, str(dest / "scripts/route.py"),
                                     "--task", "Write a guide", "--intent", "document"],
                                    capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(result.stdout)["PRIMARY"].endswith("GUIDE.md"))
            with self.assertRaises(RoutingError):
                export(ROOT, dest)


if __name__ == "__main__":
    unittest.main(verbosity=2)
