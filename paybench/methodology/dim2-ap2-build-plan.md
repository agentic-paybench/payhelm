# Dim-2 (RAPL) — AP2 (R6) adapter build plan

**Feasibility: BUILDABLE LOCALLY** (scoping research `w56fqhjyl`, 2026-06-22). Closes the R6 gap —
AP2 can be measured first-party like the other rails, no GCP payment service / card network / live
Credential Provider needed.

## What exists
- **Official Google reference impl:** `github.com/google-agentic-commerce/AP2` (Python, Apache-2.0,
  actively maintained mid-2026). **Pin to a specific commit/tag** (v0.1→v0.2 had terminology +
  structural drift — e.g. `CartMandate` → `Checkout Mandate`).
- **Runnable locally** via a single `run.sh` (the *human-present cards* scenario): four A2A agents —
  Shopping (:8000), Merchant (:8001), **Credentials Provider (:8002)**, Merchant Payment Processor
  (:8003). Canonical path: `code/samples/python/...`; spec: `docs/ap2/specification.md`.

## The authorization primitive to time (maps to Sub-ranking A)
The verify→issue boundary is a **discrete, observable** step inside the **Credentials Provider
Agent** (`code/samples/python/src/roles/credentials_provider_agent/tools.py`):
- `handle_get_payment_method_raw_credentials` — **verifies the PaymentMandate SD-JWT** (real, local
  crypto) then retrieves credentials;
- `handle_create_payment_credential_token` — **mints a tokenized credential** (mock, in-memory).

→ Time **mandate-presented → credential-issued**. This is AP2's authorization primitive; it does
**not** settle. AP2 is **Sub-ranking A only** (no 402 challenge), tagged **scope = whole rail**
(per §2 / RR6).

## Decompose the dispatch out (gate requirement, satisfied)
The dispatch hop is a **separate** agent — the Merchant Payment Processor (:8003, gated by a mock OTP
`123`). So timing the CP verify→issue **excludes** dispatch cleanly (the §2.3 "dispatch decomposed
out" requirement).

## The key measurement decision — instrument the CP functions DIRECTLY (LLM-free)
`run.sh` requires a free **Google AI Studio `GOOGLE_API_KEY`** (or Vertex ADC) because the ADK agents
call **Gemini** for reasoning. **That LLM is NOT part of the authorization primitive** — the
verify→issue functions contain no LLM call. So: **time the two CP functions directly** (a thin harness
that calls them, or instrument the A2A request→response boundary at :8002), **not** the end-to-end
agent wall-clock (which would fold in Gemini round-trips and pollute the number). The Google API key
is needed to stand the scenario up, but the **timed path stays local + LLM-free.**

## What it needs
- Python 3.11+, the `uv` package manager, a **free Google AI Studio API key** (agent runtime only).
- The reference repo's generated **certs/keys** for the SD-JWT verify path (`certs/` +
  `AGENT_PROVIDER_PUBLIC_KEY_PATH`) — confirm `run.sh` provisions these, else a one-time setup step.
- *(No testnet wallet / no chain RPC — AP2's number is mock-issuance + real-local-crypto-verify, which
  is the right shape for an authorization primitive. FR7 RPC-pinning does not apply; pin the AP2
  repo commit instead.)*

## Build steps (the adapter)
1. Clone AP2 at a pinned commit; `uv` install; provision the key + certs; confirm `run.sh` brings up
   the cards scenario.
2. Add a thin `measure_rapl.py`-equivalent that drives a mandate through and **times the CP
   verify→issue** (directly, LLM-free), with the **same review-fixed shape** as Base/Solana
   (warm-up, min-floor where a baseline applies, raw-primary, outcome taxonomy ok/rejected/timeout/
   harness_error). No `/rapl/rtt` if measuring in-process; if measuring the :8002 A2A boundary, add a
   same-path baseline.
3. Decompose the MPP dispatch out; emit `samples/R6-gcp-ap2.rapl.samples.jsonl`.
4. **Review** (same independent measurement review as Base/Solana) before trusting numbers.

## Caveats (carry into the doctrine)
- AP2 number = **real local SD-JWT verify + mock credential retrieval** → an *authorization-logic*
  latency, deliberately excluding any real network/issuer round-trip (which a production CP would add).
  Disclose this (it is the AP2 analogue of the testnet-vs-mainnet caveats), alongside the
  whole-scope tag.
- **Pin the commit** (terminology/structure drift). Optionally cross-check the *human-not-present
  cards / x402* scenario, but human-present cards is the most stable target.

## Verdict
**Build it.** Modest effort, first-party, closes the R6 gap properly before pre-registration. The one
non-obvious thing — instrument the CP functions directly so Gemini isn't in the timed path — is the
make-or-break measurement decision.
