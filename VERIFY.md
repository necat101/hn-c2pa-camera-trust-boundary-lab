# VERIFY — hn-c2pa-camera-trust-boundary-lab

Clean-clone verification of the implementation commit. The later documentation commit (this file) is a descendant and was not itself clean-clone verified unless re-verified separately.

## Tested revision

- implementation commit (verified): `18ce76c83633ca06cf0ec3f2ac99df233fea2dc9`
- verification clone: `file:///tmp/hn-c2pa-camera-trust-boundary-lab` cloned to `/tmp/verify-clone`, checked out `18ce76c83633ca06cf0ec3f2ac99df233fea2dc9` (detached HEAD)

## Commands and exit codes

```sh
git clone /tmp/hn-c2pa-camera-trust-boundary-lab /tmp/verify-clone
cd /tmp/verify-clone
git checkout 18ce76c83633ca06cf0ec3f2ac99df233fea2dc9
python3 scripts/evaluate_cases.py > /tmp/verify_out.json
# exit 0
python3 -m unittest tests.test_evaluate_cases -v
# exit 0 — 3 tests OK
python3 tests/test_evaluate_cases.py
# exit 0 — all tests passed
diff -u /tmp/final_out.json /tmp/verify_out.json
# exit 0 — COMPARE OK: regenerated matches committed output
git status --porcelain
# (empty — clean working tree)
python3 --version
# Python 3.12.3
```

## Environment

- python: Python 3.12.3
- platform: Linux (same host as implementation), stdlib + shell only, no external packages
- date (UTC): 2026-09-04

## Classification totals (regenerated)

```
Evaluated 12 synthetic cases.
  capture_path_compromised: true=2 false=10
  capture_path_evidence_present: true=8 false=4
  manifest_valid: true=10 false=2
  scene_truth_not_established: true=12 false=0
  signer_trusted: true=7 false=5
```

## Comparison result

- Regenerated `/tmp/verify_out.json` is byte-identical to the pre-commit `/tmp/final_out.json` that was used to write `RESULTS.md` in the implementation commit — **match**.
- Unittest suite: 3 tests, 0 failures, 0 errors.
- Direct test runner: all tests passed.

## Working-tree state at tested revision

```
# in /tmp/verify-clone at 18ce76c83633ca06cf0ec3f2ac99df233fea2dc9
$ git status --porcelain
(empty)
$ git rev-parse HEAD
18ce76c83633ca06cf0ec3f2ac99df233fea2dc9
$ git ls-files
.github/workflows/audit.yml
.gitignore
README.md
RESULTS.md
fixtures/capture_cases.json
scripts/evaluate_cases.py
tests/__init__.py
tests/test_evaluate_cases.py
```

Note: This VERIFY.md will be committed in a later descendant documentation commit. The descendant commit itself is not claimed to have been clean-clone verified unless a separate verification is performed on that descendant SHA.
