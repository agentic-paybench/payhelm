# Dim-2 RAPL — candidate scored results (group-and-decompose, DR4)

**Status: CANDIDATE scored set — NOT yet frozen.** Consolidates the run-validated pilots
(`dim2-q4-pilot-log.md`) into the **DR4 group-and-decompose** format (§2.5.1). It *supersedes the DRAFT
placeholders at the pre-registration ceremony* — it is not itself pre-registered. **Gating before
freeze:** (a) the pre-reg ceremony; (b) **re-check Stellar censoring** (the one FR1-trigger crossing); (c)
independent measurement review of the AP2/Tempo/Lightning harnesses. All medians are **lognormal**; times
in ms; topologies **T1 = devbox**, **T2a = GitHub Codespaces/Azure**, **T2b = OCI uk-london-1 (x64)**.

Reporting rules applied: **P50/P95/P99 + N + per-topology** (D4a/D4e); **group by work-class, rank within,
compare across only via the decomposition** (D4c); **E2E headline + local/backing decomposition** (D4b);
**Tempo TTL as warm/cold, not a bucket** (D4d). **No single cross-class ordinal.**

---

## Sub-ranking A — Payment-Validation

### Group A1 — Local-complete (no per-call network round-trip)
| Rail (mode) | median | P95 | P99 | N | topology | class note |
|---|---|---|---|---|---|---|
| **AP2 — delegated/DPC** (2 ES256) *(headline)* | **1.58** | — | 1.74 | 30 | in-process (invariant) | holder-KB chain verify |
| AP2 — human-present (issuer-only, 1 ES256) | 0.68 | — | 0.75 | 30 | in-process (invariant) | single-token verify |
| Tempo-Session (voucher accept) | **8.2 / 11.2 / 19.5** | — | ~10–19 | 30 | T2b / T2a / T1 | local crypto **+ amortized ~5 s TTL RPC tick**; median is **host-CPU-dependent** (faster host → lower) |

- AP2 is in-process → **topology-invariant by construction** (measured on devbox; blocker-fixed).
- Tempo-Session: warm (cache-hit) voucher = the numbers above; **cold (TTL miss → one chain-RPC read) ≈ 360 ms** (`L_cold`, disclose with the request inter-arrival). Local-class because steady-state has no per-call RPC.

### Group A2 — Network-dependent (facilitator / chain-RPC round-trip per call)
E2E is **backing-service-dominated**; the local-compute floor is sub-ms (signature build/verify), so
**E2E ≈ backing-service component**. Report per-topology (the absolute median is path-dependent); the
**within-group order is the scored result**.

| Rail | T1 | T2a | **T2b** | P95(T2b) | P99(T2b) | N(T2b) | censoring | backing service |
|---|---|---|---|---|---|---|---|---|
| **x402-Solana** | 400 | 180 | **212** | 370 | 416 | 30 | 0% | x402.org facilitator |
| **x402-Stellar** | 464 | 364 | **289** | 428 | **915** | 26 | **13.3% (T2b only)** | OZ facilitator |
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
- **FR1 censoring (the one trigger crossing):** **Stellar T2b 13.3% > 5%** (4/30 OZ `/verify` invalids,
  clustered, transient; **0% on T1/T2a**). Treat as **censored, not dropped**; **re-run to confirm** — if
  representative, the **BT → Cox-PH/competing-risks fallback fires** (FR1). All other rail×topology cells:
  **0% censoring**.
- **Work-clause (RR5/FR2/FR7):** the backing-service hop (facilitator / chain-RPC / Lightning node) is the
  **real authorization work** — reported as a diagnostic, **never subtracted** from E2E. The min-RTT floor
  removes only the localhost transport.
- **Scope tags (RR6):** AP2 = whole-rail, in-process (no transport); a sidecar deployment would add an IPC
  hop — disclosed. x402/MPP numbers are the authorization *slice* of a larger flow.

## Pending before this becomes the frozen pre-registered set
1. Pre-registration ceremony (signed tag, dim-2 pass — `CEREMONY-RUNBOOK.md`).
2. Stellar censoring re-check (FR1).
3. Independent measurement review of the AP2/Tempo/Lightning harnesses.
4. (Bonus) A1/ARM topology if uk-london-1 capacity frees — a free portability point.
