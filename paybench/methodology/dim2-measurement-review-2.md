# Dim-2 RAPL — independent measurement review, round 2 (new/changed harnesses)

Adversarial, read-only audit of the harnesses built or materially changed since round 1
(`dim2-measurement-review.md`): **AP2 full-verify, Tempo-Session A, Stellar (retry), topology2 driver**.
Four independent reviewers, 2026-06-28, against the branch `dim2-rapl-instrumentation` (`3e5dbe1`).

## Verdicts
| Harness | Verdict | Blockers | Headline |
|---|---|---|---|
| AP2 full-verify | yes-with-caveats | 0 | Chain **1.58 ms** verified + reconciles to the sample exactly; blocker-fixes confirmed. **0.68 ms HP has no surviving sample** (overwritten). |
| Tempo-Session A | **1 blocker** | 1 | Value reconciles (8.2 ms), but **voucher monotonicity is never recorded/asserted** → can't rule out a cached-receipt false-fast; regime not recorded. |
| **Stellar (retry)** | **3 blockers** | 3 | Latency distribution fine, but **the retry SUPPRESSES real FR1 censoring** — its regex matches 26/28 OZ reject reasons + funds-declines. |
| topology2 driver | **1 blocker** | 1 | Faithful per-rail execution, but **a fully-failed rail (0/30) is reported "done"** with a green SUMMARY. |

## BLOCKERS (fix before scoring)

### Stellar retry — censoring suppression (3 blockers; the most serious — introduced by my own fix `3e5dbe1`)
- The construction-race regex includes `invalid_exact_stellar_payload` and `simulation`, but **every** OZ
  reject is namespaced `invalid_exact_stellar_payload_*` (26/28 reason codes match), and **insufficient-funds
  / no-trustline** — the canonical FR1 censoring event — surfaces as `simulation_failed`. So a **genuine
  payment decline is retried 8× then booked as `harness_error` and excluded from FR1.** The "Stellar
  censoring 0%" claim is therefore not measurement-sound: a real decline is structurally invisible.
- Exhaustion → `harness_error` (excluded). But a reject that **persists across all 8 fresh-ledger retries is
  NOT a transient race** → it should fall through to **`rejected`** (feed FR1), not `harness_error`.
- **Fix:** allowlist ONLY the demonstrated race codes by **exact reason** —
  `invalid_exact_stellar_signature_expiration_too_far` (and a *gated* `…_simulation_failed` only when the
  error string indicates an RPC/ledger fault, never a funds decline); route **persistent-after-retry →
  `rejected`**; reserve `harness_error` for transport/build exceptions. The **latency median (~0.44 s) is
  unaffected** — only the reject classification is wrong.

### Tempo-Session A — voucher monotonicity not auditable (1 blocker)
- The harness asserts `status 200 && receipt != null` but **never records or checks that the channel
  advanced** (no `cumulativeAmount`/voucher-nonce). An idempotent/replayed voucher returning a cached
  200+receipt would score as a legitimate ~8 ms accept (false-fast). **Fix:** record
  `res.receipt.cumulativeAmount` per trial, assert strict increase, demote a non-advancing trial to
  `harness_error`.

### topology2 driver — silent failure (1 blocker)
- `run-topology2.sh` runs the measure command, **ignores its exit code, and unconditionally notes "done"**;
  the harnesses exit 0 even at 0/30 ok. So a rail whose server boots but every trial errors lands in the
  SUMMARY as `done … RAW {"n":0}` — reads as passing, feeds an empty distribution. **Fix:** have the driver
  inspect the `outcomes:` line and downgrade to **FAILED/SUSPECT** when `ok < trials` or `harness_error > 0`
  or `n:0` (and ideally make the harnesses exit non-zero on `ok==0`).

## MAJORS
- **AP2 0.68 ms unreconcilable:** single `SAMPLES_PATH` (mode `"w"`) → the chain run overwrote the
  human-present run's samples; the only single-token file on disk is the OLD contaminated 1.68 ms data. The
  0.68 ms rests only on the pilot-log table. **Fix:** make `SAMPLES_PATH` mode-dependent; re-run the
  issuer-only capture under `_full.py` and commit its samples. (Chain 1.58 ms is fine.)
- **Tempo-Session regime not recorded:** the published warm numbers were produced at effective `--sleep 0`
  (single TTL window, no RPC tick), but the advertised invocation is `--sleep 1` (would cross TTL boundaries
  → periodic ~360 ms spikes). σ_log 0.053 is only valid for the warm regime. **Fix:** record `sleep_s` +
  `regime` in the sample; state the warm/no-tick scope. Also: no trailer (socket_connects/counts not durable).
- **topology2 Tempo not idempotent:** `setup-accounts.ts` regenerates EOAs + re-funds on every run (header
  claims "idempotent" — false). **Fix:** guard behind `[ -s .env ]`. Plus: solana incomplete-.env / health
  passes with a bogus key; `free_port` kills only the first PID.

## What PASSED (confirmed sound)
- AP2 chain: blocker-fixes hold (keys/provider pre-loaded, `_log_event` no-op'd, crypto-only window); 2 ES256
  genuinely run; stats reconcile to 1.58 ms / σ_log 0.020 / p99 1.74 ms exactly.
- Stellar **timing integrity**: `accept_raw_s` is the successful verify only; retry sleeps + failed-attempt
  latencies never leak in; no selection bias on the latency (same primitive); loop bounded, no infinite loop.
- Tempo-Session: timed window tight; `saw_challenge` recorded + true (disclosure accurate); open() not timed;
  funded-buyer precondition + BLOCKED-not-scored on open failure.
- topology2: faithful per-rail execution — correct ports, runtimes (tsx for ESM tempo/lightning, ts-node for
  CJS solana/stellar, venv python for base), trial/flag pass-through unaltered; one-rail-failure isolation OK.

## Fix priority
1. **Stellar retry** — exact-code allowlist + persistent→`rejected` (correctness: affects whether FR1 fires).
2. **topology2 driver** — surface failed/empty rails in the SUMMARY (prevents silent bad data).
3. **Tempo-Session** — record + assert cumulativeAmount; record regime/sleep_s; add trailer.
4. **AP2** — mode-dependent `SAMPLES_PATH`; re-run + commit the issuer-only HP samples.

## Resolution (2026-06-28, branch `dim2-rapl-instrumentation`)
All four code fixes landed and self-validated; pushed to origin.

| # | Item | Commit | Status | Validation |
|---|---|---|---|---|
| 1 | Stellar censoring-suppression | `1a869c0` | **RESOLVED** | tight allowlist `isExpRace`/`isSimFail` only; persistent-after-retry → `rejected`; expiration-race exhaustion → `harness_error`. Re-run 40/40 ok, 0 harness_error. |
| 2 | topology2 silent failure | `56cbd7c` | **RESOLVED** | `verdict()` parses the `outcomes:`/`n:` line → `done`/`SUSPECT`/`FAILED`; wired into run_ts, base, tempo A/B notes. + Tempo `setup-accounts` guarded behind `[ -s .env ]` (idempotency major). |
| 3 | Tempo-Session monotonicity / regime | `3d26508` | **RESOLVED** | `prevCum` strict-increase gate, non-advancing → `harness_error`; trailer records `socket_connects`/`counts`/`sleep_s`/`regime`/`rtt_floor_s`. Re-run: cumulative 5000→6000→7000, 12/12 ok, trailer present. |
| 4 | AP2 mode-dependent `SAMPLES_PATH` | `0ef02d5` | **CODE RESOLVED** | per-mode filenames (`…-chain` / `…-singlekb` / `…-issueronly`); chain & HP captures no longer clobber. **Still pending: a fresh issuer-only capture ceremony to land committed HP (0.68 ms) samples — needs a founder-driven capture run; the 0.68 ms remains pilot-log-only until then.** |

**Net:** all 3 BLOCKERS + the Tempo-idempotency MAJOR closed in code and validated. The AP2 0.68 ms
remains the one open evidentiary gap — the harness is fixed, but the headline still rests on the pilot-log
table until the issuer-only capture is re-run under `_full.py` and its samples committed. The chain
**1.58 ms** (the actual sub-ranking-A headline for AP2) reconciles to its committed sample and is unaffected.
