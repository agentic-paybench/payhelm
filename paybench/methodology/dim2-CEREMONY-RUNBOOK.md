# Dim-2 (RAPL / authorization-latency) pre-registration ceremony runbook

**Scope:** the **dimension-2** pre-reg pass — a SEPARATE freeze from the landed dim-1 settlement-finality
v1.2 pass (`CEREMONY-RUNBOOK.md`). It reuses the identical mechanics (OpenTimestamps → cosign/Rekor →
signed git tag → OSF/DOI → arXiv) over a **dim-2 manifest**. The dim-1 anchors are untouched.

**Gate to start (now CLEARED, 2026-06-28):** the checklist in `dim2-auth-latency.DRAFT.md` §7 said *"do not
start the dim-2 pass until topology-2 lands (numbers scored)."* Topology-2 has landed — FR4 satisfied across
3 network-distinct vantages (T1 devbox / T2a Codespaces / T2b OCI-London), the round-2 measurement review is
fully resolved, AP2 has durable both-mode captures, and the Stellar T2b cell was re-run full-N. The scored set
is complete. **This runbook is now live, pending the founder prerequisites in §0.**

---

## 0. Founder prerequisites BEFORE the freeze (judgment acts — not mechanical)

The freeze commits to exact bytes, so these must be done first, in order:

1. **De-draft the doctrine** → **DRAFT READY (`dim2-auth-latency.md`).** Canonical de-draft of the DRAFT
   doctrine (DRAFT/PLACEHOLDER removed; scored numbers single-sourced to `dim2-scored-results.md`; §5
   seed-namespace in scope per the Hybrid freeze decision). **Awaiting founder review/ratification.**
2. **Finalize `dim2-scored-results.md`** → **PENDING.** Drop its "## Pending before this becomes the frozen
   pre-registered set" section (all items now ✅ except this ceremony) — or reduce to "frozen at ceremony."
   Confirm the scored table is the set you stand behind.
3. **Write the dim-2 pre-registration narrative** → **DRAFT READY (`dim2-PRE-REGISTRATION.md`).** Mirrors the
   dim-1 `PRE-REGISTRATION.md`; carries the watermark (mock-harness / no real-rail funds) and the Variant-E
   framing. **Awaiting founder review.** *(Add the "Rekor + OpenTimestamps independently sufficient even if OSF
   unavailable" clause — cross-LLM F16 — if not already present.)*
4. **Build the calibrated-mock leg (Variant-E baseline — new, per the Hybrid freeze decision)** → **PENDING.**
   Calibrate the six placeholder fixtures (`calibration/provenance/<rail>-auth-latency.provenance.yaml`) from
   the pilot `{median, σ}` (retire the "NOT measured" markers), wire + record the **dim-2 mock-pipeline
   reproduction hash** (the analogue of dim-1's `895f99ed…`), and re-verify `test_auth_latency.py`. This is the
   dim-2 calibrated-mock baseline that ships under Variant E; it must exist before the freeze.

Once §0 is done, the freeze (§2) and anchors (§3–§7) are pure mechanics.

## 1. Candidate frozen set (what the dim-2 manifest will commit to)

| File | Role | Status |
|---|---|---|
| `methodology/dim2-auth-latency.md` | doctrine §1–§5: SPLIT + stats + DR4 + FR1 thresholds + FR4 topology list + seed-namespace | draft ready (§0.1) |
| `methodology/dim2-scored-results.md` | scored per-rail `{median,P95,P99}` + calibration record (multi-topology order) | finalize §0.2 |
| `methodology/dim2-PRE-REGISTRATION.md` | OSF narrative | draft ready (§0.3) |
| `calibration/provenance/<rail>-auth-latency.provenance.yaml` (×6) | calibrated mock fixtures (from pilot `{median, σ}`) — Variant-E baseline | **§0.4 pending** |
| dim-2 **mock-pipeline reproduction hash** | deterministic reproducibility leg (analogue of dim-1 `895f99ed…`) | **§0.4 pending** |

**Excluded by design** (mirrors dim-1, which excludes the adversarial-review companion): the cross-LLM review
files (`dim2-review*`, `dim2-worktype-*`, `dim2-measurement-review*`), the pilot log (`dim2-q4-pilot-log.md`),
and runbooks — they accrue dispositions / are process, not the frozen claim.

> **Preview deferred.** The doctrine + narrative drafts exist, but the manifest also commits to the 6
> calibrated fixtures + the mock-pipeline hash (§0.4), which don't exist yet — so a meaningful manifest preview
> waits until calibration lands. (Earlier 3-file preview `sha256:5f50…` is stale.)

## 2. Freeze — generate the dim-2 manifest

```bash
cd paybench
# list every frozen file (one sha256 line each), header mirrors the dim-1 manifest:
{
  echo "# PayBench RAPL (authorization-latency, dim-2) pre-registration manifest — frozen $(date +%F)"
  echo "# Paths relative to paybench/. Verify: cd paybench && sha256sum -c methodology/dim2-prereg-manifest.sha256"
  echo "# Mechanics mirror the dim-1 v1.2 pass (CEREMONY-RUNBOOK.md); dim-1 anchors untouched."
  sha256sum methodology/dim2-auth-latency.md \
            methodology/dim2-scored-results.md \
            methodology/dim2-PRE-REGISTRATION.md \
            calibration/provenance/R1-x402-base-auth-latency.provenance.yaml \
            calibration/provenance/R2-x402-stellar-auth-latency.provenance.yaml \
            calibration/provenance/R9-x402-solana-auth-latency.provenance.yaml \
            calibration/provenance/R10-mpp-tempo-auth-latency.provenance.yaml \
            calibration/provenance/R11-mpp-lightning-auth-latency.provenance.yaml \
            calibration/provenance/R6-gcp-ap2-auth-latency.provenance.yaml
} > methodology/dim2-prereg-manifest.sha256
# PRE-FLIGHT before freezing (mirrors dim-1 §1): the calibrated mock pipeline must reproduce + tests pass
# python3 -m paybench.mockbench.cli run    | grep run_hash   # == the recorded dim-2 mock-pipeline hash
# python3 -m pytest paybench/mockbench/tests/test_auth_latency.py -q --noconftest

sha256sum -c methodology/dim2-prereg-manifest.sha256      # all OK
sha256sum    methodology/dim2-prereg-manifest.sha256      # <-- THIS is the dim-2 anchored value
git add methodology/dim2-prereg-manifest.sha256 && git commit -m "dim2: freeze RAPL pre-reg manifest"
```
The `sha256sum` of the manifest file is the single value all anchors below commit to. If any frozen file
changes afterward, re-freeze (regenerate the manifest) and re-anchor from scratch.

## 3. OpenTimestamps → Bitcoin (headless, do first)
```bash
cd paybench
ots stamp methodology/dim2-prereg-manifest.sha256        # writes .ots immediately; refuses to overwrite
ots upgrade methodology/dim2-prereg-manifest.sha256.ots  # bake Bitcoin attestation once confirmed (hrs)
ots info  methodology/dim2-prereg-manifest.sha256.ots    # no-node verify (or opentimestamps.org)
git add methodology/dim2-prereg-manifest.sha256.ots && git commit -m "dim2: OTS Bitcoin anchor"
```

## 4. cosign → Rekor transparency log (your machine, browser OIDC)
```bash
cosign sign-blob --yes \
  --bundle paybench/methodology/dim2-prereg-manifest.sha256.cosign.bundle \
  paybench/methodology/dim2-prereg-manifest.sha256
# logIndex: jq -r '.verificationMaterial.tlogEntries[0].logIndex' …cosign.bundle
```

## 5. Signed git tag (your machine, YubiKey plugged in)
```bash
gpg --card-status                                        # YubiKey OpenPGP present
git config user.signingkey <YUBIKEY_KEYID>               # ed25519 signing subkey (same key as dim-1)
git tag -s paybench-rapl-prereg-v1 <FROZEN_COMMIT> \
  -m "PayBench RAPL (authorization-latency) pre-registration — dim-2; manifest <dim2 hash>"
git tag -v paybench-rapl-prereg-v1                       # verify
git push origin paybench-rapl-prereg-v1
```
Signer identity `Michael Blake <mblake@everydayai.link>` (canonical). Hardware-signed, same posture as dim-1.

## 6. OSF pre-registration → DOI (web)
Paste `dim2-PRE-REGISTRATION.md` as the narrative; attach the tagged commit's `dim2-prereg-manifest.sha256`
+ the de-drafted doctrine. Watermark sentence in the abstract (mock harness / no real-rail funds). Embargo
to **2026-07-17 (POC Day-0)**, early-release permitted. Independently archive (IA/IPFS) for F16 robustness.

## 7. arXiv (longest lead — start endorsement early)
Either a dim-2 methods paper or a § added to the existing `paper/payhelm-methods.tex` (F14: no per-rail
finality numbers in the public preprint — for dim-2, mirror with no raced per-rail ranking, only the
doctrine + the FR4-satisfied *order*). Category **cs.CR**. Embed the dim-2 manifest hash; arXiv v1 canonical.

---

## Disposition table (fill as anchors land)
| Anchor | Status | Reference |
|---|---|---|
| Founder §0 (de-draft + narrative) | **pending** | §0.1 doctrine de-draft · §0.2 scored final · §0.3 narrative |
| Freeze (dim-2 manifest) | pending | `dim2-prereg-manifest.sha256` → anchored hash `—` |
| OpenTimestamps (Bitcoin) | pending | — |
| cosign → Rekor | pending | — |
| Signed git tag | pending | `paybench-rapl-prereg-v1` on `<FROZEN_COMMIT>` |
| OSF DOI | pending | embargo 2026-07-17 |
| arXiv | pending | cs.CR |

## Where each step runs
| Step | Runs on | Blocker |
|---|---|---|
| Freeze / manifest | anywhere (this devbox OK) | — |
| OpenTimestamps | headless OK | `pipx install opentimestamps-client` |
| cosign + Rekor | **interactive machine** | browser OIDC |
| Signed git tag | **interactive machine** | YubiKey in `gpg --card-status` |
| OSF / arXiv | web | account / endorsement |

The two signing steps (cosign keyless, git tag) are deliberately human-gated — the point of a trust-anchor
ceremony. The freeze + OTS I can drive from this devbox session the moment §0 is done.
