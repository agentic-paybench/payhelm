# Dim-2 (RAPL) — independent measurement review

Adversarial, independent review of the per-rail measurement harnesses (distinct from the cross-lineage
*doctrine* gate in `dim2-adversarial-review.md`). Checks that each harness's published numbers are
TRUSTWORTHY: tight timed window, B1/S1/S2/S3 shape, correct min-RTT floor, honest stats, valid scope
claim. Base (R1) and Solana (R9) were review-fixed earlier; this round covers **AP2 (R6), Tempo (R10),
Lightning (R11)**, run 2026-06-24 (three independent reviewers, one per harness).

## Verdicts

| Rail | Verdict | Blockers | Disposition |
|---|---|---|---|
| **Tempo R10** | ✅ yes | 0 | Numbers stand. Apply 2 nits (below). |
| **Lightning R11** | ✅ yes-with-caveats | 0 | Numbers stand; **re-run at n=30** for sibling-consistency. |
| **AP2 R6** | ⚠️ yes-with-caveats | **2** | **Number contaminated** — fix blockers + re-run before it can be scored. |

## AP2 R6 — findings (`poc/rail-ap2/measure_rapl_ap2.py`)

- **[BLOCKER #1] File reads inside the timed window.** `_verify_payment_mandate` re-reads + re-parses the
  agent pubkey PEM and the X.509 trusted-root cert PEM from disk on EVERY call (uncached). README's
  "no file reads inside the timed window" is false. **Fix:** pre-load + pre-parse the key/cert once
  outside the loop; time the crypto only (call the underlying `MandateClient().verify(...)` with a
  pre-built JWK, not the disk-reading wrapper).
- **[BLOCKER #2] Logging I/O inside the timed window.** `MandateClient.verify()` calls `_log_event()`
  twice per call; each does `mkdir` + a JSON append-write to a logfile. Variable disk latency fattens
  the tail / inflates σ_log. **Fix:** no-op / redirect the SDK logger (or `LOG_FILE_PATH=/dev/null`) for
  the timed run and disclose; or time below the `MandateClient.verify` facade.
- **[MAJOR #3 — JUDGMENT CALL] Verify is weaker than production.** The no-aud/no-nonce path skips
  audience + key-binding/nonce checks; the issuer ES256 signature IS still verified, but the live CP
  path binds `expected_aud="credential-provider"` + `expected_nonce`. **Decision needed (founder):**
  (a) keep issuer-signature-only verify + disclose loudly, or (b) capture the aud/nonce and time the
  full production verify. Changes what AP2's "A" represents. **[OPEN]**
- **[MAJOR #4] README / naming over-claims issuance.** Code never calls `account_manager` (imported,
  unused); `verify_and_issue()` only verifies. README step 3 + the name contradict the code. **Fix:**
  rename → `verify_only`, drop the unused import, correct README to "issuance excluded."
- **[MAJOR #5] Cross-rail A comparability.** AP2's A is in-process (no transport) and now carries its own
  uncontrolled disk floor (#1/#2); x402's A is an HTTP+network `/verify`. After #1/#2, disclose that
  AP2's A excludes all transport → A-vs-A across these classes is a *disclosed* apples-to-oranges (this
  is the same heterogeneity the §2.5 work-type disclosure is meant to own). **Fix:** disclosure, not code.
- Clean: monotonic clock, n honest, raw-primary, no wrongful RTT subtraction, warmup excludes cold-start,
  crypto genuinely runs each iteration (not cached/short-circuited). Nits: leaked file handle (`:96`),
  p99@n=30 == max.

**Net:** ~1.68 ms is a valid UPPER BOUND on warm ES256 SD-JWT verify; the clean number (post-fix) is
expected to be smaller — which *strengthens* the A-heterogeneity finding. Must fix #1/#2 + decide #3 +
re-run (n=30) before scoring.

## Lightning R11 — findings (`poc/rail-lightning-mpp/src/measure-rapl.ts`)

- **[MAJOR #4] n=15 vs n=30 siblings.** Median stable (SE of log-median ≈ ±3%; the ~420× gap survives any
  resampling), but the asymmetry invites challenge and the tail (p95/p99) is unreliable at n=15.
  **Fix:** re-run at n=30. Will not move the median materially.
- Confirmed sound: cold-start (10.2 s) lands in warmup iter-1 and never enters the scored sample
  (`Math.max(warmup,1)` guarantees ≥1 `/data` warmup hit); timed window tight; floor (1.2 ms) negligible
  vs 1252 ms and correctly NOT subtracting the Spark hop; unimodal (no cached fast-path / bimodality);
  15/15 ok consistent with the taxonomy. Headline heterogeneous-B finding is sound.
- Optional hardening: assert the first warmup `/data` exceeded a threshold, so a future no-cold-start
  regression is caught rather than silently scored.

## Tempo R10 — findings (`poc/rail-tempo-mpp/src/measure-rapl.ts`) — NO blockers

- All shape checks pass; sample artifact reproduces the published numbers exactly (median 2.954 ms,
  σ_log 0.142, 30/30 ok, 0% censoring); 402 path does real HMAC-bound challenge-gen; keep-alive counter
  independently re-verified to fire (2 connects) on Node 22.
- **[NIT #9]** `socket_connects` is printed but NOT written to the JSONL → not auditable from the sample
  alone. **Fix:** write it into a summary/trailer record.
- **[NIT #10]** Stale header comment ("REVIEW DRAFT — not yet run") though the run happened. **Fix:**
  update header.
- (Reviewer flagged the Solana sibling's raw `__dirname` as an ESM hazard — N/A: Solana's package is CJS
  node16, so raw `__dirname` is correct there. Not a defect.)

## Action punch-list (post-review)

1. **AP2 [blockers]** — pre-load PEM/cert + suppress SDK logging so the timed window is crypto-only;
   rename `verify_and_issue`→`verify_only`, drop unused import, fix README; then re-run n=30. **Gated on
   the #3 decision (aud/nonce in or out).**
2. **Lightning** — re-run at n=30 (rigor/consistency); optional cold-start assert.
3. **Tempo** — apply the 2 nits (write `socket_connects` to JSONL; fix stale header); re-run optional
   (numbers already validated).
4. Then: doctrine ratify (§2.5 work-type disclosure), FR4 2nd topology, pre-reg track.
