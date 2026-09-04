# hn-c2pa-camera-trust-boundary-lab

Deterministic synthetic evidence lab for HN item 49439499, “C2PA Cameras Do Not Survive Contact with Reality” ([Buchanan, 2026-08-25](https://www.da.vidbuchanan.co.uk/blog/android-c2pa.html)).

This lab tests the claim:

> “If a camera/app is C2PA conformant and its Content Credentials validate correctly, that proves the photograph depicts a real scene captured by that camera.”

It does so without reproducing exploits, compromising hardware, or asserting anything about a real device. All cases are synthetic JSON fixtures; the evaluator classifies them from their stated facts.

## Scenario

C2PA Content Credentials bind provenance assertions (hashes, capture metadata, actions, ingredients) into a JUMBF manifest with a claim signature over the binding. A validator checks hash bindings, signature math, signer credential validity (validity interval, revocation), time-stamps, and assertions, then presents the information so a human can make a trust decision. Trust ultimately rests on the *identity of the signer* and whether that signer is on a trust list the consumer has chosen to trust. The specification, conformance program, product implementation, device capture path, and physical scene are distinct layers; a green check in one layer does not imply the next.

A single real-world demonstration — David Buchanan’s Android Pixel Camera work — is the anchor for this thread. The lab models the *classes* of distinction that demonstration illustrates, as synthetic cases, without re-running the demonstration.

## C2PA trust / conformance map (inspected sources)

Inspected 2026-09-04 (UTC), refreshed 2026-09-04 (UTC) against the current specification:

- **C2PA Technical Specification 2.4 — April 2026** — current published specification — [spec.c2pa.org, §1.2 Scope / Guiding Principles, §14 Trust Model, §15 Validation, §17 Information Security, §18.22 Depthmap](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html) (previously inspected: 2.2; re-inspection compared 2.2 → 2.4, see below)
- C2PA Conformance Program public repository — [c2pa-org/conformance-public](https://github.com/c2pa-org/conformance-public) (generator product security requirements, conforming-products list, trust-list)
- Buchanan article — [android-c2pa.html](https://www.da.vidbuchanan.co.uk/blog/android-c2pa.html)
- Google blog note on Pixel Camera Assurance Level 2, cited by Buchanan

Re-inspection 2.2 → 2.4: The central boundaries are unchanged. §1.2 (SHOULD NOT provide value judgments), §14 (Trust Model — identity of signer, §14.3 Validation states Well-Formed/Valid/Trusted, §14.4 Trust Lists, §14.5 X.509), §15 (Validation — §15.7 claimSignature.validated / signingCredential.trusted, §15.8 time-stamp, §15.9 revocation, §15.12 asset content), and §17 (Threats/Security Considerations) retain the same normative language in 2.4 as in 2.2. Material addition in 2.4 relevant to this lab: **§18.22 Depthmap** now states depthmap assertions *shall be captured optically, not inferred from a single 2D image via ML*, and Table 6 / §18.3 (assertion metadata validation codes) explicitly enumerates `depthMap.sceneMismatch` ("depth map does not correspond to the scene … e.g., because of a picture-of-picture attack") and `thumbnail.primaryMismatch`. This confirms the specification **acknowledges picture-of-picture as a relevant attack class without claiming to defeat it**, and does not alter the provenance-vs-scene-truth boundary.

Key map (paraphrased; see 2.4 for normative text):

- **Valid manifest/signature.** Passes hash (hard binding) check + claim-signature check against the stated X.509 credential, within the validation flow (§15.6–15.8, §15.12). This is cryptography about *binding bytes to a signer*.
- **Signer trusted.** Even with valid math, the validator must decide whether the *signer identity* is trusted, via trust lists (§14.4 — EKU + trust-anchor configurations with notBefore/notAfter) and credential status (validity period §15.8, revocation §15.9, §14.5). Off-list, expired, or revoked = untrusted. 2.4 adds explicit validation states (§14.3.5 Valid requires claimSignature.validated + claimSignature.insideValidity + not revoked; §14.3.6 Trusted adds signingCredential.trusted).
- **Conforming product.** Separate from manifest validity. The Conformance Program certifies that a *product* (e.g., “Pixel Camera, AL2, Android_KeyAttestation/PlayIntegrity”) meets process/security requirements at evaluation time and appears on the conforming-products list. AL2 is the highest generator level currently defined. Attestation methods (`Android_KeyAttestation`, `Google_PlayIntegrity`) are implementation choices, not cryptographic primitives of the spec.
- **Uncompromised capture path.** Not a property of the spec; it is a property of a *deployed stack* (app, OS, TEE/StrongBox/Titan M2, attestation, patch level, hardware fault-injection resistance). Spec §17 notes threats such as compromised claim generators. This layer requires deployment evidence and is where implementation-specific attacks live.
- **Truth of the depicted scene.** The spec is explicit in Guiding Principles / §1.2: “C2PA specifications SHOULD NOT provide value judgments about whether a given set of provenance data is ‘good’ or ‘bad,’ merely whether the assertions … can be validated as associated with the underlying asset, correctly formed, and free from tampering.” Even an honest, intact capture path that faithfully signs photons cannot prove the physical event was not staged, re-photographed from a display/print, or optically relayed (the “analog hole"). 2.4 reaffirms this and, via `depthMap.sceneMismatch`, shows that when auxiliary signals (depth) disagree with the primary presentation it is reported as a validation code for human judgment — **the specification declines to establish truth ≠ the specification proves every optical attack succeeds**.

The lab’s invariant is therefore:

The lab’s invariant is therefore:

> `valid manifest` ≠ `conforming product` ≠ `uncompromised capture path` ≠ `truth of the depicted scene`.

No finding in this lab upgrades a synthetic “valid + trusted” into proof of a real-world scene, and no synthetic “compromised” case proves the C2PA specification’s cryptography is broken — it proves that a given deployment’s binding between sensor photons and signing keys did not hold in that fixture.

## What Buchanan directly demonstrated vs. argues vs. not established

Careful reading of [android-c2pa.html](https://www.da.vidbuchanan.co.uk/blog/android-c2pa.html):

- **Directly demonstrated (Android/Pixel-scoped):** On inspected Pixel-family devices, the Pixel Camera app (C2PA AL2, attested via Key Attestation / Play Integrity, keys in StrongBox/Titan M2) could be made to sign arbitrary synthetic bytes. Two paths were shown: a software root LPE (including CVE-2026-43499 via the cited [Root-My-Pixel](https://github.com/alex193a/Root-My-Pixel) tooling) and a low-cost hardware DRAM/EMFI fault-injection path (detailed in his earlier [DRAM-EMFI work](https://www.da.vidbuchanan.co.uk/blog/dram-emfi.html), with the `keystork` KeyStore proxy). Root does not exfiltrate the key; it invokes the TEE/StrongBox to sign chosen data, so locked-bootloader attestation as implemented does not detect compromise. Demo artifacts included an AI-generated image and a video that validated as “captured with a camera.”
- **Argues follows:** That Android C2PA as currently architected is broken in a practically unpatchable way — software LPEs will recur (stockpiled or via LLM-accelerated discovery) and hardware vulns in shipped devices are not retroactively fixable — and that every Android C2PA app relying on the same attestation methods is similarly affected (he notes the [conforming-products list](https://github.com/c2pa-org/conformance-public/blob/main/conforming-products/conforming-products-list.json) as the superset).
- **Broader claims the lab does not expand:** The inspected evidence is Android/Pixel-specific. It does not, on its own, establish that every possible capture architecture (e.g., sensor-integrated signing, vendor-TEE cameras, or the rumored Apple Reference mode) is equally affected, nor that the C2PA specification’s cryptography (hash bindings, COSE/JUMBF signing, X.509 trust) is cryptographically broken. Buchanan himself notes mitigations shift lowest-hanging attacks to the optical domain, and that Samsung’s RKP/EL2 hypervisor blocked his then-current PTE-flip strategy, illustrating deployment dependence.

These three buckets must not be collapsed.

## Fixtures

`fixtures/capture_cases.json` — 12 deterministic synthetic cases covering the six required observable boundaries:

1. **Valid + trusted + intact** (`c01`) — green manifest/signer, evidence-present, not compromised.
2. **Valid + trusted + compromised** (`c02`, `c11`) — same greens but `capture_path.compromised: true` via synthetic root-LPE key invocation and synthetic fault-injection attestation bypass.
3. **Valid signer math, untrusted signer** (`c03`, `c09`) — off-list / expired, so validation must treat as untrusted.
4. **Tampered manifest** (`c04`) and **missing manifest** (`c08`) — invalid absences.
5. **Conforming product but no scene truth** (`c05`) — product-conformance metadata with a physically staged scene; also `c12` (conformance claimed but no capture-path evidence field).
6. **Photographed-display / analog hole** (`c06` display, `c10` print) — honest cryptographic chain, sensor-faithful, but the subject is itself a depiction.

Additional cases `c07` (revoked cert) exercise revocation-interval checks. Every case carries a `scene.note` explaining why provenance does not settle scene truth.

## Evaluator

`scripts/evaluate_cases.py` — stdlib-only classifier. Inputs are the stated facts; it computes:

- `manifest_valid` — `present && signature_valid && hash_binding_valid && !tampered`
- `signer_trusted` — `on_trust_list && cert_valid && !revoked && present && signature_valid`
- `capture_path_evidence_present` — literal `capture_path.evidence_present`
- `capture_path_compromised` — literal `capture_path.compromised`
- `scene_truth_not_established` — always `true` (provenance alone never proves the physical event)

It never emits `photo_is_real`, `c2pa_proves_truth`, or `attack_proves_c2pa_broken`.

```sh
python3 scripts/evaluate_cases.py > /tmp/out.json
python3 tests/test_evaluate_cases.py
# or
python3 -m unittest tests.test_evaluate_cases -v
```

## HN claims checked

Every proposition below was retrieved live from HN item 49439499; HN comments are treated as propositions to audit, not as evidence. Assessment uses exactly the four labels specified. Re-inspected against **C2PA 2.4 (April 2026)**; comparison with prior 2.2 inspection is noted. Two distinctions are preserved throughout: **the specification declines to establish truth ≠ the specification proves every optical attack succeeds**, and **the specification acknowledges picture-of-picture as a relevant attack class ≠ every proposed sensor/depth mitigation is ineffective** (mitigations are deployment-specific).

| # | Proposition (paraphrased from comment) | Source | Assessment (against 2.4) |
|---|----------------------------------------|--------|---------------------------|
| 1 | “TPMs / hardware security modules have been broken before; a separate-chip signing path is not sufficient — signing must be baked into the sensor.” | `randomblock1` — id 49441472 (“people have broken TPMs before. It’d have to be baked into the camera sensor.”) | **`requires implementation or deployment evidence`** — Unchanged from 2.2. C2PA 2.4 defines trust via signer identity + EKU/trust-anchor configurations (§14.4) and validation states (§14.3.5–14.3.6, §15.7–15.9). Whether a given TPM/SE/StrongBox/Titan M2 resists a specific bypass is a hardware/deployment claim requiring independent evaluation, not a spec-level theorem. 2.4 does not newly guarantee any hardware. |
| 2 | “Even with sensor-level signing, optical / display re-photography (‘analog hole’) remains possible — you can attack from the next level up with optics and a display.” | `randomblock1` id 49441472 (same comment, second sentence); echoed by `yjftsjthsd-h` id 49441907 (“The analog hole is alive and well”) and `wisty` id 49441578 (“Tripod, camera, clear monitor … just take a real photo of a fake photo.”) | **`supported by inspected c2pa source`** — Confirmed and *strengthened* in 2.4. Provenance binds *bytes to a signer*, not photons to scene truth (§1.2 SHOULD NOT provide value judgments; §14.1–14.3, §17). 2.4 now explicitly enumerates the attack class via validation codes `depthMap.sceneMismatch` (“does not correspond to the scene … e.g., because of a picture-of-picture attack”) and `thumbnail.primaryMismatch` (Table 6 / §18.3) and adds §18.22 requiring depthmaps be captured optically not ML-inferred — acknowledging the class without claiming to defeat re-photography. Declining to establish truth ≠ proving every optical attack succeeds. |
| 3 | “Digital signatures / provenance alone are insufficient to decide whether an image is authentic — presence/absence of a signature will never be the deciding factor.” | `duskwuff` id 49441520 (“The presence/absence of a digital signature will never be the deciding factor in whether people accept/reject an image as authentic.”) | **`supported by inspected c2pa source`** — Unchanged. 2.4 §1.2 and §14.3 (§14.3.1: the consumer “then has to interpret those statements to arrive at conclusions … from those statements and the contents of the asset itself”) plus §14.4/§15 make clear that validation yields Well-Formed/Valid/Trusted statements; truth decisions require trust-list policy and human judgment. |
| 4 | “Buchanan’s Android result (root LPE → arbitrary signing via StrongBox) defeats C2PA generally / proves the C2PA specification itself is cryptographically broken.” | `uqers` id 49441289 (client-side-verification framing) + thread generalization of Buchanan’s Android-scoped demo into a universal claim; Buchanan’s article is Android/Pixel-scoped. | **`not established by the inspected sources`** — Unchanged. The demonstrated failure is a deployed binding between sensor and key invocation (Pixel AL2, Android Key Attestation / Play Integrity, §14-adjacent implementation), not a break of 2.4’s hard bindings / COSE signing / X.509 cryptography (§9, §13, §15.7). 2.4’s cryptography is identical in this respect. Expanding an Android-scoped result to “all C2PA cameras” still exceeds the inspected evidence. |
| 5 | “Apple’s Secure Enclave / LiDAR depth map will solve image provenance (provenance proof is not tenuous).” | `tashian` id 49441201 (“Apple could run the whole signing process inside SEP… integrate a LiDAR depth map as a mitigation against the analog attacks”); contrast `gyomu` id 49441462 (“provenance ‘proof’ … is very tenuous and nowhere near ‘this is a real photo’”) | **`supported only for the inspected implementation/threat model`** — Unchanged, with narrower 2.4 support. 2.4 §18.22 requires depthmaps be optically captured and defines `depthMap.sceneMismatch` as a validation signal for human judgment — acknowledging depth as a *trust signal*, not a proof of scene truth. A vendor-closed TEE + depth may raise cost for *some* bypasses in *that* deployment, but the spec treats mismatch as a code for the consumer to interpret (§14.3.1, §16 UX), and Buchanan notes mitigations shift attacks rather than close the analog hole. No 2.4 source establishes a general “proven real scene” proof; acknowledging the attack class ≠ proving every depth mitigation is ineffective — effectiveness is deployment-specific and requires independent hardware/security evaluation. |
| 6 | “C2PA with hardware attestation is trivially defeated because any rooted device can forge; patching / revocation fixes it.” | `uqers` id 49441289 (“defeated by any rooted device”) / `demibabs` id 49441429 (“It must be rooted via an exploit.”) | **`requires implementation or deployment evidence`** — Unchanged. Whether “any rooted device” suffices depends on unlock-vs-exploit root, patch availability (CVE-2026-43499 discussion), revocation/time-stamp checking (§15.8–15.9, §14.3.5), and hardware fault-injection resistance — all deployment-specific under 2.4 as under 2.2. Revocation and time-stamp checks are necessary (§14.3.5) but not sufficient alone. |

## Narrow conclusions (re-confirmed against 2.4)

- Valid C2PA provenance, even when the manifest validates and the signer is trusted, establishes integrity/binding properties and a trust-list-scoped claim about provenance data — not that the depicted physical event occurred. Re-inspection of 2.4 §1.2 + §14.3 confirms the provenance-vs-scene-truth boundary is unchanged; central conclusion **unchanged**.
- Implementation-specific attacks (Android Key Attestation / Play Integrity bypass via LPE or fault injection) demonstrate failures of deployed attestation and key-invocation binding, not a break of the C2PA specification’s cryptographic primitives.
- Optical re-photography (display or print of a synthetic image) shows a class of attacks provenance alone cannot rule out, even with an honest, sensor-faithful capture path. 2.4’s new `depthMap.sceneMismatch` acknowledges picture-of-picture as a relevant attack class; it does not prove every optical attack succeeds, nor does it prove every depth/sensor mitigation is ineffective — both remain deployment-specific.
- Negative results (e.g., sensor-integrated signing or Apple SEP depth maps “solving” provenance) remain deployment- and threat-model-specific and require independent hardware/security evaluation.
- This lab makes no claim about the security of any real camera, phone, or service; all cases are synthetic and seeded (seed 42).

## Limitations

- No media corpora, no device rooting, no exploit reproduction, no hardware attacks, no Android tooling, no network trust-list fetches, no real certificates.
- Labs are stdlib + shell only; no external Python packages, no containers.
- HN thread excerpts are propositions audited here; they are not authoritative evidence.

## Reproduce

```sh
python3 scripts/evaluate_cases.py
python3 tests/test_evaluate_cases.py
python3 -m unittest tests.test_evaluate_cases -v
```

See `RESULTS.md` for committed output and `VERIFY.md` for the clean-clone verification transcript.
