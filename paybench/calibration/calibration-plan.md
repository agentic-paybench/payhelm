# PayBench calibration sourcing plan

**Status: STARTED 2026-06-04** (Friday-1 "calibration sourcing started" deliverable). Companion to `paybench/methodology/methodology.md` §6–§7.

## What we calibrate

Per-rail **settlement-finality distributions** for the **5 settling rails** that race on the Day-0 finality benchmark (AP2/R6 is on the Day-30 authorization-latency dimension per methodology §8 Resolution B, so it is out of scope here):

- **R1** x402-Base
- **R2** x402-Stellar
- **R9** x402-Solana
- **R10** MPP-on-Tempo (Stripe PSP)
- **R11** MPP-on-Lightning (Lightspark)

A "calibrated fixture" needs a *distribution*, not a point estimate. The Day-0 metrics — BT MLE on pairwise finality races, pass@k = P(finality ≤ k s), Wilson LB CIs — all sample finality times, so each rail needs a central tendency **and** a characterised spread/tail.

**Motivating evidence (why point estimates fail).** The R1 Friday-1 reference run logged **6.781s** (two-org) vs **2.521s** (single-org) — ~2.7× spread across just two trials. Calibration must capture that variance, not average it away.

## Sources (per methodology §7)

Three source types, combined per rail:

1. **First-party testnet/devnet observations** — our own POC adapter runs (most defensible; reproducible). Today: R1 (Base Sepolia), R9 (Solana devnet), R3 Lightning regtest (informs R11).
2. **Rail documentation** — published finality semantics (block times, confirmation depth, ledger close, HTLC resolution).
3. **Public telemetry** — e.g. x402scan for x402 rails; explorers for block-time distributions.

## Per-rail status

Documentary sweep done 2026-06-04 — starting log-normal parameters sourced per rail (provenance files alongside). Refine with first-party trials (n≥30) per the hybrid plan.

| Rail | Finality model | Median (s) | sigma_log (tail) | Confidence | First-party next |
|---|---|---|---|---|---|
| R1 x402-Base | probabilistic, soft@block | 3.0 | 0.45 | medium | extend adapter to n≥30 (runs today) |
| R2 x402-Stellar | deterministic @ ledger close | 6.0 | 0.26 | medium | capture adapter run |
| R9 x402-Solana | probabilistic, 32-slot **finalized** | 13.5 | 0.25 | high (tail est.) | extend adapter (devnet, runs today) |
| R10 MPP-on-Tempo | deterministic BFT (Simplex) | 1.0 | 0.30 | **low (proxy)** | run vs provisioned Tempo testnet |
| R11 MPP-on-Lightning | off-chain HTLC, instant | 0.8 | 0.80 | medium (body) / est. tail | R3 regtest body proxy; R11 access pending |

Three load-bearing cautions from the sweep: (1) **Solana `finalized` ≠ `confirmed`** — the ~1–2s figure is confirmed/optimistic; true finality is ~13s (~10× difference, the most likely source of a wrong fixture). Methodology §3 already commits to `finalized` — correct. (2) **R10 Tempo is genuinely thin** — design targets on a private testnet, no measured variance; every Tempo parameter is low-confidence proxy. (3) **Stellar + Lightning tails** are real but under-quantified (one Stellar 11s outlier; Lightning's qualitative retry mechanism) — P99s parameterised by us, flagged as estimates. The x402 facilitator envelope (~0.5–0.7s, near-constant) is folded into R1/R2/R9 medians.

## Distribution approach (RECOMMENDED — to confirm)

- **Default family: log-normal** — finality times are positive, right-skewed, bounded below by the rail mechanism; log-normal fits that shape and is parameter-light (μ, σ).
- **Empirical / bootstrap** where first-party samples are rich enough (target n ≥ 30 per rail).
- **Parametric from docs + telemetry** where first-party samples are thin: doc-derived central estimate sets the location; public telemetry / block-time variance sets the spread.
- Each fixture **records which approach + parameters it used** in its provenance file. No rail silently uses a different method without it being on the record.

## Provenance schema

One provenance file per fixture (`provenance/<rail>-finality.provenance.yaml`), recording: rail, dimension, distribution family + parameters, every source (type / ref / date / sample size), calibration date, confidence, and the content hash of the generated fixture. Template at `provenance/_TEMPLATE.provenance.yaml`. Seed example at `provenance/R1-x402-base-finality.provenance.yaml`.

## Reproducibility

Seeded RNG drives all sampling; fixtures are content-addressed (hash recorded in provenance). Same seed + same fixtures → bit-for-bit reproducible run (methodology §5.4 fix-list item 6, §6).

## Sourcing method — DECIDED: Hybrid (C), 2026-06-04

First-party measurement where adapters already run (R1 Base, R9 Solana, R3 Lightning regtest → R11 proxy); rail docs + public telemetry for the rest and for spread/tail. Documentary track done this session (table above). **Next: the first-party track** — extend the R1 + R9 adapters into n≥30-trial measurement loops to replace the doc-derived medians with empirical distributions, and capture an R2 Stellar run. R10 (Tempo) and R11 (Lightspark) stay doc-proxy until full access lands.
