# PayBench settlement-finality benchmark — Pre-registration

**Pre-registration of an evaluation methodology and its analysis plan, committed before
publication of any real-rail ranking.**

- **Methodology version:** v1.1 (frozen 2026-06-06, post-cross-LLM-review)
- **Decisions confirmed:** 2026-06-06 — D1-keep (per-rail-canonical reliance-level finality
  doctrine), D2-freeze (empirical `sigma_log` as-measured + disclosed limitation). A four-model
  cross-LLM adversarial review (Gemini/DeepSeek/Kimi/Qwen) upheld **D1 3–1** and **D2 4/4**; v1.1
  applies its zero-regen hardening (no fixture regen). See `pre-reg-adversarial-review.md`.
- **Frozen-method commit (agentic-paybench/payhelm):** tag `paybench-prereg-v1.1` (resolves to the
  v1.1 freeze commit; the prior v1.0 freeze was `58f656e1`)
- **Manifest:** `paybench/methodology/prereg-manifest.sha256`
- **Manifest hash (the value the cryptographic anchors commit to):**
  `sha256:f0b9b079e72fcfdadde976be9ee5cdcd5ac893e86e86e875b440ac13e3009d99`

---

## What is being pre-registered

The complete settlement-finality benchmark design **and** analysis plan, fixed in advance of
publishing any rail-by-rail result, so that no element can later be accused of having been chosen to
flatter a rail. The full method is `paybench/methodology/methodology.md` (v1.1); this document is the
registration record and points at the frozen byte-set.

This pre-registration covers the **measurement method and the calibrated mock baseline only**. The
eventual real-rail run is a *separate* pre-registration (its production-fixture hashes + run config
committed, same anchor stack, before that run executes — methodology §9).

### Frozen design (methodology §6, §9)

| Element | Frozen value |
|---|---|
| Settling rail set (race on finality) | R1 x402-Base, R2 x402-Stellar, R9 x402-Solana, R10 MPP-on-Tempo, R11 MPP-on-Spark-Lightning |
| Excluded from finality | R6 GCP+AP2 — does not settle independently; measured on the Day-30 authorization-latency dimension (Resolution B) |
| Pairs × trials | C(5,2) = 10 unordered pairs × 500 trials = 5,000 trials, symmetric |
| Master RNG seed | `20260717` (stdlib Mersenne Twister; no wall-clock, no OS entropy) |
| Per-rail finality definitions | §3 — ecosystem-canonical reliance level per rail (Base soft@1-block; Stellar ledger-close; Solana `finalized`; Tempo BFT block; Spark preimage release), with a trust/equivalence-class column |
| Fixture hashes (sha256) | R1 `5e0383b7…e194` · R2 `46afd5c0…b206` · R9 `0659647c…b2fc` · R10 `0798d250…51ee` · R11 `af5c8917…8c9d` |

### Frozen analysis plan (methodology §5)

- **Bradley-Terry MLE** over pairwise finality-race wins → latent comparative strength per rail
  (symmetric smoothing prior = 1.0, to stay well-defined under near-complete separation).
- **pass@k = P(finality ≤ k seconds)**, `k ∈ {2, 3, 5, 10, 15, 20}` seconds (grid frozen, not
  re-fit per run — §5.2).
- **Wilson score intervals**, reporting the **95% lower bound** as the conservative figure, on all
  win rates and pass@k probabilities (§5.3).
- Scored mock run is byte-deterministic; **mock-pipeline verification hash**
  `sha256:895f99ed52567421a1d7e9068ab9a0d7147d6381ec137e1b130b805e63b14ee0` (verifies pipeline
  reproduction — *not* a real-rail ranking result; §9).

### Pre-registered disclosed limitations (no silent caps — §5.4 item 7, §7)

1. The fixture `sigma_log` (tail) values are from quiet testnet/devnet/regtest load and likely
   understate mainnet congestion tails — sharpest for R9 and R11. Central tendencies are
   high-confidence first-party empirical; tails are the disclosed soft spot. Frozen as-measured.
2. R2's fixture is the manual direct-payment **lower bound** on the spec x402-on-Stellar path
   (omits the OZ-facilitator round-trip).
3. R10 is calibrated on Moderato **testnet**; mainnet `Presto` shares the consensus algorithm but
   not necessarily the empirical latency — an optimistic bound pending a mainnet re-measure.

## Scope and Variant E

These anchors commit to the **method and the calibrated mock fixtures**, *not* to a real-rail
ranking. Under Variant E (a closed project decision), PayBench ships as an open tool with calibrated
mock-data fixtures; publication of real-rail rail-by-rail scoring is deferred pending regulatory
clarity. A future real-rail run re-executes **this same pre-registered method** against production
fixtures. The mock run included here demonstrates the pipeline; it is not, and is not presented as, a
real-rail result.

## Cryptographic grounding (defence-in-depth — §9)

The manifest hash above is committed via three independent trust anchors plus two corroborating
records:

- **OSF pre-registration** → DOI (human-readable anchor; this document)
- **cosign** signature over the manifest → **Rekor** transparency-log entry
- **OpenTimestamps** on the manifest → **Bitcoin** block anchor
- **Signed git tag** `paybench-prereg-v1.1` on the v1.1 freeze commit (YubiKey OpenPGP)
- **arXiv** preprint of the methodology

Trust-anchor triad: **OSF DOI + Bitcoin block + Rekor entry** — three independent anchors, no single
point of trust. Bulk trial telemetry (when real-rail runs occur) is signed with a Merkle root +
cosign, not VCDM/SD-JWT (§9).

## Verification

```
cd paybench
sha256sum -c methodology/prereg-manifest.sha256        # all 19 files OK
sha256sum methodology/prereg-manifest.sha256           # == f0b9b079…009d99
python3 -m paybench.mockbench.cli verify               # fixture hashes vs provenance
python3 -m paybench.mockbench.cli run                  # reproduces mock-pipeline hash 895f99ed…14ee0
```
