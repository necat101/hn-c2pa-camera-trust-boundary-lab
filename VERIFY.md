# VERIFY — hn-c2pa-camera-trust-boundary-lab

Clean-clone verification record. This file supersedes the earlier verification that used a local `file://` source and now establishes **public-origin** provenance.

## Tested revisions

### A. Original implementation commit

- commit: `18ce76c83633ca06cf0ec3f2ac99df233fea2dc9`
- description: `lab: synthetic C2PA trust-boundary fixtures, evaluator, tests, results`
- verification clone (local source — now superseded): `file:///tmp/hn-c2pa-camera-trust-boundary-lab` → `/tmp/verify-clone`, detached HEAD at `18ce76c`, **match** (byte-identical regenerated output, 3 tests OK, working tree clean, Python 3.12.3, 2026-09-04).
- Note: The `file://` source did not establish public-origin retrieval; no claim is made that `18ce76c` was verified from the public GitHub origin. The public-origin verification below covers `088b2f4`.

### B. Corrective / source-audit commit (public-origin verified)

- commit: `088b2f475bdeecdc95d9ea323a6dd66feefd9bfe`
- description: `audit: refresh to C2PA 2.4 (April 2026) — scope/trust-model/validation/depthMap picture-of-picture, keep central conclusions`
- canonical public repository URL: `https://github.com/necat101/hn-c2pa-camera-trust-boundary-lab`
- verification clone: fresh `git clone https://github.com/necat101/hn-c2pa-camera-trust-boundary-lab.git /tmp/public-verify-clone` (unauthenticated, no token, no credential store, no `/proc`, no API workaround)

## Public-origin verification evidence (corrective commit `088b2f4`)

### Clone and origin

```sh
git clone https://github.com/necat101/hn-c2pa-camera-trust-boundary-lab.git /tmp/public-verify-clone
# exit 0 — Cloning into '/tmp/public-verify-clone'...
git remote -v
# origin  https://github.com/necat101/hn-c2pa-camera-trust-boundary-lab.git (fetch)
# origin  https://github.com/necat101/hn-c2pa-camera-trust-boundary-lab.git (push)
git config --get remote.origin.url
# https://github.com/necat101/hn-c2pa-camera-trust-boundary-lab.git
git log --oneline -3
# 088b2f4 audit: refresh to C2PA 2.4 (April 2026) — scope/trust-model/validation/depthMap picture-of-picture, keep central conclusions
# 44647fa docs: add clean-clone verification for implementation commit 18ce76c
# 18ce76c lab: synthetic C2PA trust-boundary fixtures, evaluator, tests, results
```

### Checkout

```sh
git checkout 088b2f475bdeecdc95d9ea323a6dd66feefd9bfe
# exit 0 — HEAD is now at 088b2f4 audit: refresh to C2PA 2.4 (April 2026) ...
git rev-parse HEAD
# 088b2f475bdeecdc95d9ea323a6dd66feefd9bfe
git branch --show-current
# (empty — detached HEAD at 088b2f4)
git status
# HEAD detached at 088b2f4
# nothing to commit, working tree clean
git status --porcelain
# (empty)
python3 --version
# Python 3.12.3
```

### Evaluator and tests

```sh
python3 scripts/evaluate_cases.py > /tmp/public_verify_out.json 2> /tmp/public_verify_stderr.txt
# exit 0
cat /tmp/public_verify_stderr.txt
# Evaluated 12 synthetic cases.
#   capture_path_compromised: true=2 false=10
#   capture_path_evidence_present: true=8 false=4
#   manifest_valid: true=10 false=2
#   scene_truth_not_established: true=12 false=0
#   signer_trusted: true=7 false=5

python3 -m unittest tests.test_evaluate_cases -v
# exit 0
# test_evaluator_output_matches_expected ... ok
# test_forbidden_outputs_never_emitted ... ok
# test_specific_central_boundaries ... ok
# Ran 3 tests in 0.159s — OK

python3 tests/test_evaluate_cases.py
# exit 0 — all tests passed (direct runner)
```

### Classification totals (regenerated, public-origin)

```
Evaluated 12 synthetic cases.
  capture_path_compromised: true=2 false=10
  capture_path_evidence_present: true=8 false=4
  manifest_valid: true=10 false=2
  scene_truth_not_established: true=12 false=0
  signer_trusted: true=7 false=5
```

### Comparison against committed results

- `RESULTS.md` classification buckets and per-case JSON are byte-identical to the output regenerated in `/tmp/public-verify-clone` at `088b2f4` — **match** (`total_cases 12`, totals above, 3 tests OK).
- The `RESULTS.md` contents are deterministic synthetic fixtures (seed 42); no real media, hardware, or exploit.
- Working tree at `088b2f4`: `git status --porcelain` empty, `git ls-files` shows 8 tracked public items (`.github/workflows/audit.yml`, `.gitignore`, `README.md`, `RESULTS.md`, `VERIFY.md` (pre-update), `fixtures/capture_cases.json`, `scripts/evaluate_cases.py`, `tests/__init__.py`, `tests/test_evaluate_cases.py` plus the updated `README.md` at audit).

### Environment

- python: `Python 3.12.3`
- platform: `Linux (ubuntu, stdlib + shell only, no external packages)`
- date (UTC): `2026-09-04`
- clone method: **unauthenticated public `https://` clone** — no credentials, tokens, credential stores, environment dumps, `/proc`, or API workarounds used.

## Note on descendant commit

This VERIFY.md update will be committed in a later descendant documentation commit after `088b2f4`. That descendant commit is **not** claimed to have been clean-clone verified unless a separate verification is performed on that descendant SHA.
