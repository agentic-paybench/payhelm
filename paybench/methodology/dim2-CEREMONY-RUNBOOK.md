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

1. **De-draft the doctrine.** `dim2-auth-latency.DRAFT.md` still carries the `DRAFT / PROPOSED` banner and
   `PLACEHOLDER` number language. The doctrine was **founder-ratified 2026-06-24** (DR4 group-and-decompose,
   FR1 thresholds, FR4 ≥2-topology) and the placeholders are now **real scored numbers**. Promote it to a
   canonical ratified file (suggest `dim2-auth-latency.md`) with the DRAFT/PLACEHOLDER banners removed and the
   scored values referenced. *This is the one real content act left; everything below is mechanical.*
2. **Finalize `dim2-scored-results.md`.** Drop its "## Pending before this becomes the frozen pre-registered
   set" section (items 1–5 are now all ✅ except this ceremony itself) — or reduce it to "frozen at ceremony."
   Confirm the scored table is the set you stand behind.
3. **Write the dim-2 pre-registration narrative.** Mirror the dim-1 `PRE-REGISTRATION.md` as
   `dim2-PRE-REGISTRATION.md` (the OSF registration narrative): the SPLIT doctrine, FR1/FR4, the
   group-and-decompose scored result, the watermark sentence (mock-harness / no real-rail funds), and the
   "Rekor + OpenTimestamps independently sufficient even if OSF unavailable" clause (cross-LLM F16).

Once §0 is done, the freeze (§2) and anchors (§3–§7) are pure mechanics.

## 1. Candidate frozen set (what the dim-2 manifest will commit to)

| File | Role | Status |
|---|---|---|
| `methodology/dim2-auth-latency.md` *(de-drafted from DRAFT.md)* | doctrine §2 SPLIT + §2.5 stats + §2.5.1/DR4; FR1 thresholds; FR4 topology list | **§0.1 pending** |
| `methodology/dim2-scored-results.md` | scored per-rail `{median,P95,P99}` (group-and-decompose, 3 topologies) | finalize §0.2 |
| `methodology/dim2-PRE-REGISTRATION.md` *(new)* | OSF narrative | **§0.3 pending** |

**Excluded by design** (mirrors dim-1, which excludes the adversarial-review companion): the cross-LLM review
files (`dim2-review*`, `dim2-worktype-*`, `dim2-measurement-review*`), the pilot log (`dim2-q4-pilot-log.md`),
and runbooks — they accrue dispositions / are process, not the frozen claim. *(Optionally fold the FR1/FR4
confirmed values into the doctrine so the frozen set is self-contained.)*

> **Preview only** (current bytes, PRE-de-draft — these hashes WILL change once §0 is done):
> ```
> ae7d0c92…  methodology/dim2-auth-latency.DRAFT.md   (→ becomes dim2-auth-latency.md)
> 27646d35…  methodology/dim2-scored-results.md
> ```

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
            methodology/dim2-PRE-REGISTRATION.md
} > methodology/dim2-prereg-manifest.sha256

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
