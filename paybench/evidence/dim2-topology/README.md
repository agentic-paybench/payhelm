# Dim-2 (RAPL) — multi-topology raw sample evidence

Curated copy of the **raw per-trial RAPL measurement samples** across three network-distinct topologies. This
is the empirical basis for **FR4** (the ≥2-topology requirement) and the scored within-group network order
(Solana R9 < Stellar R2 < Base R1, stable across all three topologies). One JSON object per line = one trial.

## Status — supporting evidence, NOT a frozen/anchored artefact
Added **2026-06-30, post-freeze**. This directory is **not** part of the dim-2 pre-registration manifest
(`sha256:46a19eab…1dcd388`) and does not change any anchored hash. The **canonical, anchored** artefacts remain:
- calibration inputs → the frozen fixtures `paybench/fixtures/<rail>-auth-latency-{A,B}.fixture.json`;
- the 3-topology **order** → `paybench/methodology/dim2-scored-results.md`.
These raw samples are *gitignored by design* in the agentpay instrumentation repo
(`agentpay`, branch `dim2-rapl-instrumentation`: *"raw run samples; curated copies live in the payhelm
fork"*) — **this directory is that curated copy.** Integrity: `SHA256SUMS` (verify with `sha256sum -c SHA256SUMS`).

## Topologies
| Dir | Vantage | When |
|---|---|---|
| `T1-devbox/` | local devbox | ~2026-06-22 |
| `T2a-codespaces/` | GitHub Codespaces | ~2026-06-24 |
| `T2b-oci/` | OCI London VM | ~2026-06-28 |

## Schema (per line)
`trial` · `ts` (ISO-8601) · `rtt_floor_s` (same-path min-RTT baseline) · `challenge_raw_s` (B leg, where
applicable) · `accept_raw_s` (A leg) · `outcome` (`ok`/`rejected`) · plus per-rail extras
(`status`/`saw_challenge`/`has_receipt`; AP2 carries `mode`). These are **derived** measurements, not raw rail
response transcripts — golden-transcript adapter tests therefore cannot be backfilled from them (see
`ERRATA.md` E6 / `gauntlet-r1-disposition-sheet.md` G-P4).

## Per-rail / per-topology trial counts
- **T1-devbox:** R1 30 · R2 30 · R9 30 · R10 30 · R10-session 20 · R11 30 · R6(AP2) chain/full/issueronly 30 each
- **T2a-codespaces:** R1 30 · R2 30 · R9 30 · R10 31 · R10-session 30 · R11 30
- **T2b-oci:** R1 30 · R2 **40 (canonical)** · R9 30 · R10 31 · R10-session 30 · R11 30

## Notes
- **Stellar (R2) at T2b — two runs preserved.** The canonical `R2-x402-stellar.rapl.samples.jsonl` is the
  **full-N re-run, 40/40, 0 censoring** (evening 2026-06-28; median accept ≈ 0.284 s ≈ the scored 289 ms),
  captured *after* the censoring-classifier fix. The earlier `R2-x402-stellar.morning-pre-censoring-fix…`
  (30 trials, **4 rejected ≈ 13%**) is kept for transparency: it shows the pre-fix rejection *rate* behind the
  G-R7 censoring discussion. Note the rejected rows carry only `outcome: rejected` + timing — **not** the
  per-reject reason strings (those lived in harness logs that were not preserved; the raw-reason ask in G-R7
  remains for the real-rail run).
- **AP2 (R6) is in-process / topology-invariant** — its `mode` variants (chain / full / issueronly) sit under
  `T1-devbox/` for completeness; its *replayable raw captures* (`captured-*.json`) live in
  `agentpay/poc/rail-ap2/` and are the one rail with true golden transcripts today.
- **Read the order as "rail+facilitator-as-deployed"** (each rail on a different facilitator; all topologies
  reach the same pinned backend) — see `ERRATA.md` E2 / G-R3.

Cross-refs: `methodology/dim2-auth-latency.md` (FR4) · `methodology/dim2-scored-results.md` ·
`methodology/ERRATA.md` · `methodology/gauntlet-r1-disposition-sheet.md`.
