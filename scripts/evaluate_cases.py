#!/usr/bin/env python3
"""
evaluate_cases.py — deterministic classifier for synthetic C2PA trust-boundary fixtures.

Reads fixtures/capture_cases.json and emits factual classifications.
Never emits photo_is_real / c2pa_proves_truth / attack_proves_c2pa_broken.
Stdlib only.
"""
import json
import pathlib
import sys

FORBIDDEN_KEYS = {"photo_is_real", "c2pa_proves_truth", "attack_proves_c2pa_broken"}
ALLOWED_KEYS = {"manifest_valid", "signer_trusted", "capture_path_evidence_present", "capture_path_compromised", "scene_truth_not_established"}

def classify(case: dict) -> dict:
    m = case.get("manifest", {})
    s = case.get("signer", {})
    cp = case.get("capture_path", {})

    manifest_valid = bool(m.get("present") and m.get("signature_valid") and m.get("hash_binding_valid") and not m.get("tampered"))

    # signer_trusted requires the signer to be on the trust list, cert valid, not revoked,
    # and a manifest is present with a signature that is structurally valid.
    # We deliberately keep signer trust distinct from manifest_valid in the output,
    # but a revoked/expired/off-list signer must not be treated as trusted even if bytes validate.
    signer_trusted = bool(s.get("on_trust_list") and s.get("cert_valid") and not s.get("revoked") and m.get("present") and m.get("signature_valid"))

    capture_path_evidence_present = bool(cp.get("evidence_present"))
    capture_path_compromised = bool(cp.get("compromised"))

    # Scene truth is never established by the synthetic provenance facts alone.
    # Even c01 (intact) and c06 (honest re-photography) must not be read as proof of a real event.
    scene_truth_not_established = True

    result = {
        "manifest_valid": manifest_valid,
        "signer_trusted": signer_trusted,
        "capture_path_evidence_present": capture_path_evidence_present,
        "capture_path_compromised": capture_path_compromised,
        "scene_truth_not_established": scene_truth_not_established,
    }
    # safety: never emit forbidden conclusions
    for k in FORBIDDEN_KEYS:
        assert k not in result
    return result

def main():
    fixtures_path = pathlib.Path(__file__).parent.parent / "fixtures" / "capture_cases.json"
    if not fixtures_path.exists():
        # also try cwd-relative
        alt = pathlib.Path("fixtures/capture_cases.json")
        if alt.exists():
            fixtures_path = alt
        else:
            print(f"fixtures not found: {fixtures_path}", file=sys.stderr)
            sys.exit(2)
    data = json.loads(fixtures_path.read_text())
    cases = data["cases"]

    rows = []
    counts = {k: 0 for k in ALLOWED_KEYS}
    # also track falses for zero-bucket reporting
    for c in cases:
        cls = classify(c)
        rows.append({"id": c["id"], "classifications": cls})
        for k, v in cls.items():
            if v:
                counts[k] += 1

    # totals including zero-count buckets: report both true/false
    total = len(cases)
    bucket_report = {}
    for k in sorted(ALLOWED_KEYS):
        t = counts[k]
        bucket_report[k] = {"true": t, "false": total - t}

    out = {
        "total_cases": total,
        "buckets": bucket_report,
        "cases": rows,
    }

    json.dump(out, sys.stdout, indent=2, sort_keys=False)
    sys.stdout.write("\n")

    # human summary to stderr
    print(f"\nEvaluated {total} synthetic cases.", file=sys.stderr)
    for k in sorted(ALLOWED_KEYS):
        print(f"  {k}: true={bucket_report[k]['true']} false={bucket_report[k]['false']}", file=sys.stderr)

if __name__ == "__main__":
    main()
