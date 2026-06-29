# PayBench authorization-latency (RAPL) benchmark — Pre-registration

> **RATIFIED (founder, 2026-06-29) — pending the freeze ceremony.** Companion to the landed dimension-1
> settlement-finality pre-registration (`PRE-REGISTRATION.md`), as a **separate dim-2 pass** reusing the same
> anchor stack. The manifest hash + DOI + anchor references below are filled at the ceremony
> (`dim2-CEREMONY-RUNBOOK.md`) once the remaining §0 prerequisites land (finalize `dim2-scored-results.md`; the
> calibrated-mock leg, §0.4).

**Pre-registration of an evaluation methodology and its analysis plan, committed before publication of any
real-rail authorization-latency ranking.**

- **Dimension:** 2 — authorization latency (RAPL: Rail Authorization-Primitive Latency)
- **Doctrine version:** dim-2 v1 (candidate freeze 2026-06-28)
- **Decisions ratified:** 2026-06-24 — **DR4 group-and-decompose** (work-class grouping + per-rail
  decomposition tuple), **FR1 numeric fallback triggers** (tie > 20% / censoring > 5% / cyclic > 10% / BT-fit
  LR p < 0.05), **FR4 ≥2-topology** requirement. The SPLIT design (payment-validation vs challenge-issuance
  sub-rankings) cleared a four-round cross-lineage adversarial review (0–4 → 3–1 → 4/4 pre-registerable →
  DR4). See `dim2-adversarial-review.md`, `dim2-worktype-synthesis.md`.
- **Frozen-method commit (agentic-paybench/payhelm):** tag `paybench-rapl-prereg-v1` *(resolves to the dim-2
  freeze commit — filled at the ceremony)*
- **Manifest:** `paybench/methodology/dim2-prereg-manifest.sha256`
- **Manifest hash (the value the cryptographic anchors commit to):** `sha256:—` *(computed at freeze; §2 of
  the runbook)*

---

## What is being pre-registered

The complete authorization-latency (RAPL) benchmark **design and analysis plan**, fixed in advance of
publishing any rail-by-rail result, so that no element can later be accused of having been chosen to flatter a
rail. The full method is `dim2-auth-latency.md` (the de-drafted doctrine); this document is the registration
record and points at the frozen byte-set.

This pre-registration is the **dimension-2 pass**, distinct from the landed dimension-1 (settlement-finality,
v1.2) pre-registration, reusing the identical anchor stack. It covers the **measurement method and the
first-party pilot/scored calibration**; it does not assert a production real-rail ranking (see Scope, below).

### Frozen design (doctrine §2, §2.5, §2.5.1)

| Element | Frozen value |
|---|---|
| Dimension structure | **SPLIT** — Sub-ranking A (Payment-Validation) and Sub-ranking B (Challenge-Issuance), never raced across each other |
| Sub-ranking A members (C(5,2)=10 pairs) | x402-Base, x402-Stellar, x402-Solana, **Tempo-Session**, AP2 (auth-only/whole-scope). *Tempo-Charge excluded (fused verify+settle).* |
| Sub-ranking B members (C(5,2)=10 pairs) | x402-Base, x402-Stellar, x402-Solana, MPP-on-Tempo, MPP-on-Spark-Lightning (macaroon + BOLT11). *AP2 absent (no 402).* |
| `t = 0` | Pay command on the wire (payload constructed); last-byte stopwatch (FR3); same-path TCP/TLS RTT baseline subtracted, raw + corrected reported (FR4) |
| Work-class grouping (DR4/D4c) | Within each sub-ranking, group **Local-complete** vs **Network-dependent**; rank within a group; compare across only via the decomposition tuple `(local_compute_floor, backing_service_component, E2E)` (D4b) |
| Headline tuple (D4a) | **P50 / P95 / P99 + N + timestamp + topology** per rail |
| FR1 fallback triggers (frozen) | tie-rate > 20% **OR** censoring > 5% **OR** > 10% cyclic triples / BT-fit LR p < 0.05 → switch BT → Cox-PH / competing-risks |
| FR4 topologies (≥2 required, satisfied) | T1 devbox · T2a GitHub Codespaces (Azure) · T2b OCI uk-london-1 — 3 network-distinct vantages (2026-06-28) |
| Scored per-rail `{median,P95,P99}` | `dim2-scored-results.md` (group-and-decompose, 3 topologies). **The scored result is the within-group order**, not the absolute ms. |
| Calibrated mock fixtures + mock-pipeline hashes | 10 per-(rail×sub-ranking) fixtures (`…-auth-latency-{A,B}.provenance.yaml`) calibrated from the pilot `{median, σ}` (placeholders retired) + deterministic reproduction hashes **A `7487c278…` / B `19b91c8d…`** — the **Variant-E baseline** (SPLIT A/B, mirroring dim-1); frozen finality `run_hash 895f99ed…` unperturbed |
| Reproducibility / seed-namespace (§5) | master seed `20260717`; RNG domain-separated `fixture:auth-latency:<rail>` / `pair:auth-latency:<a>:<b>`; asserted by `test_auth_latency.py::test_dimensions_are_rng_domain_separated` |

### Frozen analysis plan (doctrine §2.5, §4)

- **Bradley-Terry MLE** within a sub-ranking only (never across A/B), `prior=1.0`, **Davidson ties extension**
  + explicit **censoring/competing-risks** for reject/timeout (not silently dropped). **Cox-PH /
  Aalen-Johansen pre-specified as the FR1-data-triggered fallback** (not swapped pre-emptively).
- **`P(auth ≤ k)`** — a latency **CDF** (not pass@k), millisecond k-ladder `{20, 50, 100, 250, 500} ms`,
  rank-stability heatmap + variance-aware power analysis; **median / P95 / P99** reported alongside.
- **Wilson score** lower-bound CIs (conservative); **Kaplan-Meier** survival curves for description.
- **Assurance covariate** `P(settled | accept)` recorded per rail; **companion agent-observed total latency**
  (accept + accept→settle gap) reported co-primary.

### Pre-registered disclosed limitations (no silent caps)

1. **Network rails are path-sensitive** — absolute medians track the measuring host's route; only the
   **within-group order** is the scored claim (FR4/D4e; reported per-topology with the min-RTT floor).
2. **Local rails are host-sensitive** — compute-heavy rails' medians track host CPU; tiny rails' tails track
   scheduling. Reported per-host.
3. **Tempo TTL** is reference-impl config, not a rail class — reported as `L_hot`/`L_cold` with the
   inter-arrival distribution, not a taxonomy bucket (D4d).
4. **AP2 is in-process** (topology-invariant by construction); a sidecar deployment would add an IPC hop
   (disclosed, D4f). AP2 numbers are from durable replayable captures; the DPC/delegated number is the
   headline, human-present a variant.
5. The **backing-service component is never subtracted** from E2E (the RPC/facilitator read *is*
   authorization work — RR5/FR2/FR7); it is disclosed as a diagnostic only.

## Scope

These anchors commit to the **method + the calibrated mock baseline** (the dim-2 mock fixtures calibrated from
the first-party pilot `{median, σ}` + the deterministic mock-pipeline hash), **not** a published production
real-rail leaderboard — mirroring the dimension-1 **Variant-E** posture. PayBench ships as an open tool with
calibrated mock fixtures; any public rail-by-rail scoring follows the same pre-registered method against pinned
production endpoints. `dim2-scored-results.md` is included as the **calibration record and disclosed
first-party pilot evidence** — it carries the real multi-topology *within-group order* + decomposition tuples
that a single per-rail log-normal cannot represent (DR4) — and is not, and is not presented as, a mainnet
ranking.

## Cryptographic grounding (defence-in-depth)

The dim-2 manifest hash is committed via the same independent trust anchors as dim-1 (all **pending** until
the ceremony runs):

- **OpenTimestamps** on the manifest → **Bitcoin** block anchor — *pending (headless; do first)*
- **cosign** signature over the manifest → **Rekor** transparency-log entry — *pending (browser OIDC)*
- **Signed git tag** `paybench-rapl-prereg-v1` on the dim-2 freeze commit (YubiKey OpenPGP, same key as dim-1)
  — *pending*
- **OSF pre-registration** → DOI (human-readable anchor; this document) — *pending (embargo to 2026-07-17,
  early-release permitted)*
- **arXiv** preprint / § — *pending (category cs.CR)*

Trust-anchor triad: **OSF DOI + Bitcoin block + Rekor entry** — three independent anchors, no single point of
trust; the signed git tag + arXiv are additional defence-in-depth. The dim-1 anchors are untouched.

## Verification

```
cd paybench
sha256sum -c methodology/dim2-prereg-manifest.sha256     # all frozen files OK
sha256sum    methodology/dim2-prereg-manifest.sha256     # == the dim-2 anchored hash
# AP2 captures are durable/replayable (embedded pubkey + exp-tolerant replay):
#   agentpay poc/rail-ap2/measure_rapl_ap2_full.py --mandate poc/rail-ap2/captured-{hp,dpc}.json
```

## Provenance posture (what the anchors prove — and what they do not)

As with dim-1: the anchors prove **precedence, integrity, and signer-identity** — not authorship of the
cryptographic primitives. PayBench's original contribution on this dimension is the **SPLIT
authorization-primitive doctrine** (payment-validation vs challenge-issuance, the category-error fix) and the
**group-and-decompose work-class methodology** (DR4: decomposition tuple + FR1-triggered survival fallback +
mandatory ≥2-topology), for which this pre-registration establishes precedence. The measurement primitives
(SHA-256, cosign, OpenTimestamps) are commodity standards used as-is and claimed by no one.
