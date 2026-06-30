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
4. **Build the calibrated-mock leg (Variant-E baseline)** → **DONE 2026-06-29 (`7777418a`).** The mock harness
   was the superseded pre-gate design (single 6-rail/15-pair race, `[0.25..5]s` grid); refactored to the
   ratified **SPLIT** — `auth-latency-A` (R1,R2,R9,R10,R6) + `auth-latency-B` (R1,R2,R9,R10,R11), C(5,2)=10
   pairs each, never cross-raced, ms k-ladder. **10 fixtures calibrated** from the pilot `{median, σ}`
   (representative topology T2b/canonical; placeholders retired). **Mock-pipeline reproduction hashes:**
   A = `sha256:7487c278…d122072b`, B = `sha256:19b91c8d…b4dd7c71`; BT rankings reproduce the doctrine
   within-group order (A: AP2<Tempo-Session<Solana<Stellar<Base; B: local-402≪Lightning). **Frozen finality
   `run_hash 895f99ed…` UNPERTURBED** (guarded by `test_finality_artefact_is_unperturbed`). All 21 mockbench
   tests pass.

Once §0 is done, the freeze (§2) and anchors (§3–§7) are pure mechanics.

## 1. Candidate frozen set (what the dim-2 manifest will commit to)

**32 files**, the full dim-1-parity set (docs + harness code + provenance + fixtures + run reports):

| Group | Files | Role | Status |
|---|---|---|---|
| Docs (3) | `dim2-auth-latency.md`, `dim2-scored-results.md`, `dim2-PRE-REGISTRATION.md` | doctrine + scored set + OSF narrative | ✅ ratified |
| Harness code (7) | `mockbench/{__init__,bench,cli,dimensions,fixtures,paths,stats}.py` | the code the reproduction hashes depend on (mirrors dim-1, which freezes the code) | ✅ done |
| Provenance (10) | `calibration/provenance/<rail>-auth-latency-{A,B}.provenance.yaml` | calibrated mock fixtures (per rail×sub-ranking, from pilot `{median, σ}`) — Variant-E baseline | ✅ done (`7777418a`) |
| Fixtures (10) | `fixtures/<rail>-auth-latency-{A,B}.fixture.json` | content-addressed sample populations | ✅ done |
| Runs (2) | `runs/auth-latency-{A,B}-run.json` | reproduction hashes **A `7487c278…` / B `19b91c8d…`** | ✅ done |

**Excluded by design** (mirrors dim-1): the cross-LLM review files (`dim2-review*`, `dim2-worktype-*`,
`dim2-measurement-review*`), the pilot log (`dim2-q4-pilot-log.md`), the tests, and the runbooks — they accrue
dispositions / are process, not the frozen claim.

> **All §0 prerequisites are now done** (doctrine ratified, scored-results finalized, narrative ratified,
> calibrated-mock leg landed) — the freeze (§2) is ready to run. The manifest commits to the full **32-file**
> dim-1-parity set (3 docs + 7 code + 10 provenance + 10 fixtures + 2 runs); run §2 to compute the binding
> hash. (Earlier 3-file preview `sha256:5f50…` is stale.)

## 2. Freeze — generate the dim-2 manifest

```bash
cd paybench
# list every frozen file (one sha256 line each), header mirrors the dim-1 manifest:
{
  echo "# PayBench RAPL (authorization-latency, dim-2) pre-registration manifest — frozen $(date +%F)"
  echo "# Paths relative to paybench/. Verify: cd paybench && sha256sum -c methodology/dim2-prereg-manifest.sha256"
  echo "# Mechanics mirror the dim-1 v1.2 pass (CEREMONY-RUNBOOK.md); dim-1 anchors untouched."
  # Full dim-1-parity set: docs + harness CODE + provenance + fixtures + run reports. Freezing the code
  # (mockbench/*.py) + fixtures + runs is what cryptographically pins the reproduction hashes — provenance
  # alone is NOT enough. (Tests are excluded, as in dim-1.) Globs expand deterministically (sorted).
  sha256sum \
    methodology/dim2-auth-latency.md methodology/dim2-scored-results.md methodology/dim2-PRE-REGISTRATION.md \
    mockbench/__init__.py mockbench/bench.py mockbench/cli.py mockbench/dimensions.py \
    mockbench/fixtures.py mockbench/paths.py mockbench/stats.py \
    calibration/provenance/*-auth-latency-[AB].provenance.yaml \
    fixtures/*-auth-latency-[AB].fixture.json \
    runs/auth-latency-[AB]-run.json
} > methodology/dim2-prereg-manifest.sha256
# PRE-FLIGHT before freezing (mirrors dim-1 §1): the calibrated mock pipeline must reproduce + tests pass
# python3 -m paybench.mockbench.cli run -d auth-latency-A | grep run_hash   # == sha256:7487c278…d122072b
# python3 -m paybench.mockbench.cli run -d auth-latency-B | grep run_hash   # == sha256:19b91c8d…b4dd7c71
# python3 -m paybench.mockbench.cli run -d finality       | grep run_hash   # == sha256:895f99ed… (UNPERTURBED)
# python3 -m pytest paybench/mockbench/tests/ -q --noconftest               # 21 pass

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
| Founder §0 (de-draft + narrative + mock leg) | **✅ DONE** | doctrine ratified · scored finalized · narrative ratified · SPLIT mock leg (A 7487c278 / B 19b91c8d) |
| Freeze (dim-2 manifest) | **✅ DONE** | `dim2-prereg-manifest.sha256` → anchored hash **`46a19eab516ef3214270513f718bd07a846e18a4f42d9916fcb829da71dcd388`**; freeze commit `3dd74caa` |
| OpenTimestamps (Bitcoin) | **✅ DONE — confirmed Bitcoin block 955977** | upgraded `.ots` (Bitcoin attestation baked in; also blocks 955978/955993); commits to `46a19eab…1dcd388`. |
| cosign → Rekor | **✅ DONE** | Rekor logIndex `2012836917`; bundle committed (`748ff7f5`) over `46a19eab…` |
| Signed git tag | **✅ DONE** | `paybench-rapl-prereg-v1` → freeze commit `3dd74caa` (tag obj `66075feb`), pushed; YubiKey EdDSA `B61635C9…286042AC`, signer `mblake@everydayai.link` |
| OSF registration | **✅ registered — embargoed to 2026-07-17** | Open-Ended Registration under the PayBench project (`Gv8j7`), as the "Authorization latency (RAPL)" component; Summary = plain-text abstract, 5 attachments (4 docs + `dim2-anchor-proofs.zip`). **DOI issues at embargo release** (registration GUID: *TBC*). |
| IA archive (F16) | **✅ archived** | self-verifying file set on the Internet Archive: **https://archive.org/details/dim2-auth-latency** (files: https://archive.org/download/dim2-auth-latency). |
| arXiv | **held — pending endorsement** | dim-1 already started a HELD submission: endorsement code **`3666MT`** (`arxiv.org/auth/endorse?x=3666MT`); endorsers contacted 2026-06-18 (Chishti/NTNU, Ekelhart/SBA; backup Paola Di Maio). License **CC BY**, primary `cs.CR`, cross-list `cs.DC`+`cs.PF`. **Paper now COMBINED (both dimensions)** → on endorsement clearing, recompile (Overleaf) and update the held submission with the new PDF + title/abstract. Full live state: agentpay memory `arxiv-submission-state`. |

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
