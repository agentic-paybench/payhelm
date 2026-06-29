# Dim-2 RAPL — scored results (group-and-decompose, DR4)

The scored per-rail `{median, P95, P99}` for authorization-latency (RAPL), in the **DR4
group-and-decompose** format (doctrine §2.5.1). These numbers are the **single source of truth** — the
doctrine references but does not duplicate them. All medians are **lognormal**; times in ms; topologies
**T1 = devbox**, **T2a = GitHub Codespaces/Azure**, **T2b = OCI uk-london-1**.

Reporting rules: **P50/P95/P99 + N + per-topology** (D4a/D4e); **group by work-class, rank within, compare
across only via the decomposition** (D4c); **E2E headline + local/backing decomposition** (D4b); **Tempo TTL
as warm/cold, not a bucket** (D4d). **No single cross-class ordinal.**

---

## Sub-ranking A — Payment-Validation

### Group A1 — Local-complete (no per-call network round-trip)
| Rail (mode) | median | P95 | P99 | N | topology | class note |
|---|---|---|---|---|---|---|
| **AP2 — delegated/DPC** (2 ES256) *(headline)* | **1.58** | 1.60 | 1.62 | 30 | in-process (invariant) | holder-KB chain verify |
| AP2 — human-present (issuer-only, 1 ES256) | 0.68 | 0.71 | 0.76 | 30 | in-process (invariant) | single-token verify |
| Tempo-Session (voucher accept) | **8.2 / 11.2 / 19.5** | — | ~10–19 | 30 | T2b / T2a / T1 | local crypto **+ amortized ~5 s TTL RPC tick**; median is **host-CPU-dependent** (faster host → lower) |

- AP2 is in-process → **topology-invariant by construction**. Both modes are measured from **durable,
  replay-forever captures** (embedded verifying pubkey + exp-tolerant replay) — 30/30 ok, 0 harness_error.
- Tempo-Session: warm (cache-hit) voucher = the numbers above; **cold (TTL miss → one chain-RPC read) ≈ 360 ms**
  (`L_cold`, disclose with the request inter-arrival). Local-class because steady-state has no per-call RPC.

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

**SCORED RESULT: local-402 (~2–3 ms) ≪ Lightning invoice-mint (~0.5–0.9 s)** — a **several-hundred-fold** gap
(~200–600× across topologies), robust. (Lightning faster from London; still orders of magnitude above local
emit.)

---

## Cross-cutting (carry into the frozen set)
- **Topology sensitivity (D4e, FR4 satisfied):** network rails move in the **median** (the path); local
  rails are **host-sensitive** (compute-heavy → median tracks CPU; all → tails track host scheduling).
  Report the **per-topology spread**; do **not** present a single absolute number for a network rail.
- **FR1 censoring — NO trigger fires.** The apparent Stellar ~13% "censoring" on T2b was a **harness bug,
  not a payment decision**: reject-reason capture showed **all** invalids were `auth_expiration_too_far` — OZ
  rejecting our **own malformed Soroban-auth payload** (a ledger-view race, *insensitive* to
  `maxTimeoutSeconds`). The race trials are **retried** past (rebuild + re-verify, bounded tries);
  expiration-race exhaustion → **`harness_error`** (instrumentation), a genuine persistent decline →
  **`rejected`** (feeds FR1). Net: **FR1 censoring = 0% on all rail×topology cells; the BT→Cox-PH fallback
  does not fire.** (The latency median is unaffected — the retry only recovers yield.)
- **Work-clause (RR5/FR2/FR7):** the backing-service hop (facilitator / chain-RPC / Lightning node) is the
  **real authorization work** — reported as a diagnostic, **never subtracted** from E2E. The min-RTT floor
  removes only the localhost transport.
- **Scope tags (RR6):** AP2 = whole-rail, in-process (no transport); a sidecar deployment would add an IPC
  hop — disclosed. x402/MPP numbers are the authorization *slice* of a larger flow.
