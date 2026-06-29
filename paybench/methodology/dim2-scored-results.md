# Dim-2 RAPL — scored results (group-and-decompose, DR4)

> **Frozen-candidate (founder-ratified 2026-06-29).** This is the scored set the dim-2 pre-registration
> freezes (`dim2-CEREMONY-RUNBOOK.md`); per-rail numbers here are the single source of truth (the doctrine
> references but does not duplicate them). Anchored only when the signed tag lands.

This set consolidates the run-validated pilots (`dim2-q4-pilot-log.md`) into the **DR4 group-and-decompose**
format (§2.5.1) and **supersedes the DRAFT placeholders** (retired into the calibrated mock fixtures). All
medians are **lognormal**; times in ms; topologies **T1 = devbox**, **T2a = GitHub Codespaces/Azure**,
**T2b = OCI uk-london-1 (x64)**. The pre-freeze gates — Stellar `harness_error` (tight-allowlist `1a869c0`),
the round-2 measurement review, the AP2 durable re-capture, and the Stellar T2b full-N re-run — are **all
closed** (see the resolution log at the bottom). Remaining: the freeze ceremony itself.

Reporting rules applied: **P50/P95/P99 + N + per-topology** (D4a/D4e); **group by work-class, rank within,
compare across only via the decomposition** (D4c); **E2E headline + local/backing decomposition** (D4b);
**Tempo TTL as warm/cold, not a bucket** (D4d). **No single cross-class ordinal.**

---

## Sub-ranking A — Payment-Validation

### Group A1 — Local-complete (no per-call network round-trip)
| Rail (mode) | median | P95 | P99 | N | topology | class note |
|---|---|---|---|---|---|---|
| **AP2 — delegated/DPC** (2 ES256) *(headline)* | **1.58** | 1.60 | 1.62 | 30 | in-process (invariant) | holder-KB chain verify |
| AP2 — human-present (issuer-only, 1 ES256) | 0.68 | 0.71 | 0.76 | 30 | in-process (invariant) | single-token verify |
| Tempo-Session (voucher accept) | **8.2 / 11.2 / 19.5** | — | ~10–19 | 30 | T2b / T2a / T1 | local crypto **+ amortized ~5 s TTL RPC tick**; median is **host-CPU-dependent** (faster host → lower) |

- AP2 is in-process → **topology-invariant by construction** (measured on devbox; blocker-fixed). Numbers from **durable, replay-forever captures** (embedded pubkey + exp-tolerant replay; AP2 pinned `e1ea56d`; captures+samples committed `agentpay 423a612`/`bed6298`) — both modes 30/30 ok, 0 harness_error.
- Tempo-Session: warm (cache-hit) voucher = the numbers above; **cold (TTL miss → one chain-RPC read) ≈ 360 ms** (`L_cold`, disclose with the request inter-arrival). Local-class because steady-state has no per-call RPC.

### Group A2 — Network-dependent (facilitator / chain-RPC round-trip per call)
E2E is **backing-service-dominated**; the local-compute floor is sub-ms (signature build/verify), so
**E2E ≈ backing-service component**. Report per-topology (the absolute median is path-dependent); the
**within-group order is the scored result**.

| Rail | T1 | T2a | **T2b** | P95(T2b) | P99(T2b) | N(T2b) | censoring | backing service |
|---|---|---|---|---|---|---|---|---|
| **x402-Solana** | 400 | 180 | **212** | 370 | 416 | 30 | 0% | x402.org facilitator |
| **x402-Stellar** | 464 | 364 | **289** | 366 | 553 | 40 | **0%** | OZ facilitator |
| **x402-Base** | 777 | 420 | **492** | 576 | 726 | 30 | 0% | facilitator → Base-Sepolia RPC |

**SCORED ORDER (robust across all 3 topologies): Solana < Stellar < Base.** That ordinal — not the
absolute ms — is the FR4-satisfied result. Absolute medians compress on cloud egress (T2a/T2b closer to
the facilitators than devbox).

---

## Sub-ranking B — Challenge-Issuance

### Group B1 — Local-complete (local 402 template emit)
| Rail (402) | median (range across T1/T2a/T2b) | N | class note |
|---|---|---|---|
| x402-Base / Solana / Stellar, MPP-Tempo | **~1.6 – 3.0** | 30 ea | local emit; **median topology-invariant**, tails host-jitter-fattened on shared cloud hosts |

### Group B2 — Network-dependent (backing-service issuance)
| Rail | T1 | T2a | **T2b** | N | backing service |
|---|---|---|---|---|---|
| **MPP-Lightning** (BOLT11 mint) | 936 | 771 | **552** | 30 | Spark/LN node round-trip |

**SCORED RESULT: local-402 (~2–3 ms) ≪ Lightning invoice-mint (~0.5–0.9 s)** — a ~250–500× gap, robust
across topologies. (Lightning faster from London; still an order-of-magnitude above local emit.)

---

## Cross-cutting (carry into the frozen set)
- **Topology sensitivity (D4e, FR4 satisfied):** network rails move in the **median** (the path); local
  rails are **host-sensitive** (compute-heavy → median tracks CPU; all → tails track host scheduling).
  Report the **per-topology spread**; do **not** present a single absolute number for a network rail.
- **FR1 censoring — NO trigger fires (re-checked 2026-06-28).** The apparent Stellar 13.3% "censoring"
  on T2b was a **harness bug, not a payment decision**: reject-reason capture (n=100 devbox re-run) showed
  **all** invalids were `auth_expiration_too_far` — OZ rejecting our **own malformed Soroban-auth payload**
  (ledger-view race; *insensitive* to `maxTimeoutSeconds`). Reclassified to **`harness_error`** (not
  `rejected`) → **FR1 censoring = 0% on all rail×topology cells; the BT→Cox-PH fallback does NOT fire.**
  - **Stellar yield — RESOLVED + T2b re-run DONE 2026-06-28:** the ~12–43% expiration/simulation race
    trials are now **retried** past (build+verify, 8 tries / 1.5 s spacing; `agentpay 1a869c0`). The T2b cell
    above was **re-run full-N on a fresh uk-london-1 E5.Flex vantage** (`193.123.189.152`, post-fix): **40/40
    ok, `harness_error 0`, censoring 0%**, `accept_retries` observed (races retried, all cleared). The
    **median is identical (289 ms)** to the pre-fix N=26 cell — the fix tightened the tail (P99 915→553,
    P95 428→366) and lifted N 26→40; the `†`/`‡` artifacts are retired. (An instrumentation fix, not a rail
    property.) Samples: `agentpay poc/topology2/results-T2b-oci/R2-x402-stellar.rapl.samples.jsonl`.
    - **Review-2 correction:** the first cut (`3e5dbe1`) used a *broad* race-regex that matched 26/28 OZ
      reject codes + funds-declines, which would have **suppressed real FR1 censoring**. Replaced with a
      tight exact-code allowlist (`expir(ation|ed)` + gated `simulation_failed`); persistent-after-retry →
      `rejected` (feeds FR1), expiration-race exhaustion → `harness_error`. `1a869c0` is the sound version.
- **Work-clause (RR5/FR2/FR7):** the backing-service hop (facilitator / chain-RPC / Lightning node) is the
  **real authorization work** — reported as a diagnostic, **never subtracted** from E2E. The min-RTT floor
  removes only the localhost transport.
- **Scope tags (RR6):** AP2 = whole-rail, in-process (no transport); a sidecar deployment would add an IPC
  hop — disclosed. x402/MPP numbers are the authorization *slice* of a larger flow.

## Status — frozen-candidate; all pre-freeze gates closed
This set is ready to freeze at the ceremony. The pre-freeze resolution log (all ✅):
- ✅ **Stellar `harness_error = 0`** (retry-on-construction-race, tight allowlist `agentpay 1a869c0`; supersedes the broad-regex `3e5dbe1` review-2 flagged for censoring-suppression): 40/40 clean. FR1 was already resolved (harness bug, not censoring).
- ✅ **Independent measurement review round 2** (`dim2-measurement-review-2.md`): 3 BLOCKERS + Tempo-idempotency MAJOR + the AP2 evidentiary gap all closed.
- ✅ **AP2 durable both-flow re-capture** (AP2 pinned `e1ea56d`): HP issuer-only **0.682 ms** / DPC chain **1.580 ms** (30/30 each), replay-forever captures (embedded pubkey + exp-tolerant replay); committed `agentpay 423a612`/`bed6298`.
- ✅ **Stellar T2b full-N re-run** (uk-london-1 E5.Flex `193.123.189.152`, post-`1a869c0`): 40/40 ok, harness_error 0, median 289 ms, P95 366 / P99 553, censoring 0%; replaces the N=26† cell. Order Solana<Stellar<Base unchanged.

**Remaining:** the freeze ceremony itself (signed tag, dim-2 pass — `dim2-CEREMONY-RUNBOOK.md`), which includes the calibrated-mock leg (§0.4). *(Non-blocking bonus: an A1/ARM topology if uk-london-1 free-tier capacity opens — a free portability point.)*
