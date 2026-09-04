import json
import pathlib
import sys
import subprocess
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "scripts"))
from evaluate_cases import classify  # type: ignore

FIXTURES = pathlib.Path(__file__).parent.parent / "fixtures" / "capture_cases.json"
EVALUATOR = pathlib.Path(__file__).parent.parent / "scripts" / "evaluate_cases.py"

def expected(case):
    m = case.get("manifest", {})
    s = case.get("signer", {})
    cp = case.get("capture_path", {})
    manifest_valid = bool(m.get("present") and m.get("signature_valid") and m.get("hash_binding_valid") and not m.get("tampered"))
    signer_trusted = bool(s.get("on_trust_list") and s.get("cert_valid") and not s.get("revoked") and m.get("present") and m.get("signature_valid"))
    capture_path_evidence_present = bool(cp.get("evidence_present"))
    capture_path_compromised = bool(cp.get("compromised"))
    scene_truth_not_established = True
    return {
        "manifest_valid": manifest_valid,
        "signer_trusted": signer_trusted,
        "capture_path_evidence_present": capture_path_evidence_present,
        "capture_path_compromised": capture_path_compromised,
        "scene_truth_not_established": scene_truth_not_established,
    }

class TestEvaluateCases(unittest.TestCase):
    def test_evaluator_output_matches_expected(self):
        proc = subprocess.run([sys.executable, str(EVALUATOR)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"evaluator failed: {proc.stderr}")
        out = json.loads(proc.stdout)
        data = json.loads(FIXTURES.read_text())
        by_id = {c["id"]: c for c in data["cases"]}
        self.assertEqual(out["total_cases"], len(by_id))
        for row in out["cases"]:
            cid = row["id"]
            self.assertIn(cid, by_id)
            exp = expected(by_id[cid])
            got = row["classifications"]
            self.assertEqual(got, exp, f"mislabeled {cid}: expected {exp} got {got}")
            for bad in ("photo_is_real", "c2pa_proves_truth", "attack_proves_c2pa_broken"):
                self.assertNotIn(bad, got)
            self.assertTrue(got["scene_truth_not_established"])

    def test_specific_central_boundaries(self):
        data = json.loads(FIXTURES.read_text())
        by_id = {c["id"]: c for c in data["cases"]}
        c01 = expected(by_id["c01_valid_trusted_intact"])
        self.assertTrue(c01["manifest_valid"])
        self.assertTrue(c01["signer_trusted"])
        self.assertTrue(c01["capture_path_evidence_present"])
        self.assertFalse(c01["capture_path_compromised"])
        self.assertTrue(c01["scene_truth_not_established"])
        c02 = expected(by_id["c02_valid_trusted_root_compromised"])
        self.assertTrue(c02["manifest_valid"])
        self.assertTrue(c02["signer_trusted"])
        self.assertTrue(c02["capture_path_compromised"])
        self.assertTrue(c02["scene_truth_not_established"])
        c03 = expected(by_id["c03_valid_untrusted_signer"])
        self.assertTrue(c03["manifest_valid"])
        self.assertFalse(c03["signer_trusted"])
        c04 = expected(by_id["c04_tampered_manifest_invalid"])
        self.assertFalse(c04["manifest_valid"])
        c05 = expected(by_id["c05_conforming_no_scene_truth"])
        self.assertTrue(c05["manifest_valid"])
        self.assertTrue(c05["scene_truth_not_established"])
        c06 = expected(by_id["c06_photographed_display_analog_hole"])
        self.assertTrue(c06["manifest_valid"])
        self.assertTrue(c06["signer_trusted"])
        self.assertFalse(c06["capture_path_compromised"])
        self.assertTrue(c06["scene_truth_not_established"])
        c07 = expected(by_id["c07_valid_signature_revoked_cert"])
        self.assertFalse(c07["signer_trusted"])
        c08 = expected(by_id["c08_missing_manifest"])
        self.assertFalse(c08["manifest_valid"])
        self.assertFalse(c08["signer_trusted"])

    def test_forbidden_outputs_never_emitted(self):
        proc = subprocess.run([sys.executable, str(EVALUATOR)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        out = json.loads(proc.stdout)
        for row in out["cases"]:
            for bad in ("photo_is_real", "c2pa_proves_truth", "attack_proves_c2pa_broken"):
                self.assertNotIn(bad, row["classifications"])
        self.assertNotIn("photo_is_real", proc.stdout)
        self.assertNotIn("c2pa_proves_truth", proc.stdout)
        self.assertNotIn("attack_proves_c2pa_broken", proc.stdout)
