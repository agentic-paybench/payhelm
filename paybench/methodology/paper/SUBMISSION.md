# arXiv submission — PayBench methods preprint

**Source:** `payhelm-methods.tex` — single self-contained file (no `.bib`/`.bbl`, no figures; packages `geometry`, `amsmath`, `booktabs`, `hyperref`, all arXiv-standard). Upload the one `.tex`.

**Status (2026-06-30):** combined two-dimension version — now covers **settlement-finality (v1.2)** AND **authorization-latency / RAPL** (frozen 2026-06-29). Source is arXiv-ready. Blocked on **(1) a clean compile + page count** (will be longer than the 6-page dim-1 version) and **(2) a cs.CR endorsement**. The preprint is *supplementary* (NOT part of the OSF + Bitcoin + Rekor triad) — not Day-0-blocking.

## Pre-submission checklist
- [ ] **Compile** on a TeX box (gentoo `emerge app-text/texlive`, or Overleaf) — confirm clean 2-pass build; record exact page count.
- [ ] **Endorsement** for `cs.CR` — the real blocker (see below).
- [x] arXiv account email = `mblake@everydayai.link` (done 2026-06-14).
- [ ] Submit with the metadata below; license **CC BY 4.0**.
- [ ] Moderation (~1+ business day; may reclassify category) → arXiv ID.

## Metadata (paste into arXiv)
- **Title:** PayBench: A Pre-Registered Methodology and Calibrated Mock Harness for Agent-to-Agent Payment Rails
- **Authors:** Michael Blake
- **Primary category:** `cs.CR`  ·  **Cross-list:** `cs.DC`, `cs.PF` (RAPL adds a latency/performance dimension → `cs.PF` is now a firm cross-list)
- **License:** CC BY 4.0
- **Comments:** "Two pre-registered dimensions: settlement-finality v1.2 + authorization-latency (RAPL); preprint v1" (record exact page count after the recompile)
- **Abstract (plain text — `\emph`/`\textbf`/math stripped for arXiv's abstract field):**

This preprint describes pre-registered measurement methodologies and a calibrated mock harness; no real-rail funds are moved and no production rail-by-rail ranking is derived or published here. PayBench is an evaluation methodology and benchmark for agent-to-agent (A2A) payment rails, with two benchmarked timing dimensions. Settlement-finality is the wall-clock time from payment submission to the point at which an autonomous agent may rely on the payment for an irreversible downstream action; authorization latency is the earlier, distinct point at which the rail accepts the payment as allowed to proceed. We make four contributions. First, a reliance-level doctrine for defining finality across heterogeneous rails (deterministic BFT close, probabilistic rooting, optimistic-rollup soft finality, hash-time-locked preimage release), pairing each rail's ecosystem-canonical reliance level with an explicit trust/equivalence class so that wall-clock comparisons never masquerade as security-model equivalence. Second, a split authorization-primitive doctrine that races each rail only against rails whose authorization point is the same kind of object -- separating payment-validation from challenge-issuance after an adversarial review found that racing them together is a category error -- together with a group-and-decompose analysis that groups rails by work class (local-complete vs network-dependent), ranks within a group, and compares across groups only through a per-rail decomposition rather than a single cross-class ordinal. Third, comparative statistical methods -- Bradley-Terry maximum-likelihood estimation over pairwise races, pass@k = P(. <= k), and Wilson lower-bound intervals -- hardened for the sub-second regime with a ties extension, a censoring/competing-risks rule, and a pre-specified survival-model fallback under stated numeric triggers. Fourth, a cryptographic pre-registration protocol (OSF DOI + a transparency-log entry + an independent timestamp anchor + a signed source tag + this preprint), run once per dimension, that fixes each design before any scored run and decouples methodology pre-registration from the later real-rail data pre-registration. The methodologies and a reproducible mock harness are released as an open tool; publication of real-rail rankings is deferred.

## Endorsement (the blocker)
As an independent researcher on a non-academic email, you won't be auto-endorsed for your first `cs.CR` paper. Starting a submission yields an **endorsement code**; a qualified `cs.CR` author enters it at `arxiv.org/auth/endorse` (a ~2-minute attestation that the work fits the category — not peer review). One endorsement clears you.

**Pick the primary category for where a warm, qualified endorser exists** (the endorser must qualify for that exact class). `cs.CR` is pragmatic because the W3C **Credentials CG / A2WF** crowd you already correspond with publishes `cs.CR`. If a contact is stronger in distributed systems, `cs.DC` is an equally honest primary.

**Candidate endorsers (priority order):**
1. A W3C CCG / A2WF participant you've genuinely interacted with who publishes `cs.CR`.
2. A UK security / distributed-systems academic in your network (Cambridge / UCL / Imperial).
3. Stanford CRFM / Yifan Mai if that relationship develops (skews `cs.LG` → pair with a cross-list).

**Do NOT** cold-email random prolific `cs.CR` authors — arXiv asks endorsers to vouch only for people whose work they recognize; cold asks get declined.

**How to ask (research-framed, AgentPay-invisible):** short email — who you are (independent researcher, everydayai.link), one line on the paper, that it's your first arXiv submission needing a `cs.CR` endorsement, a link to the PDF, and the endorsement code. Make saying yes frictionless.
