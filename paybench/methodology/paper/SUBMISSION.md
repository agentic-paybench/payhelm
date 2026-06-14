# arXiv submission — PayBench methods preprint

**Source:** `payhelm-methods.tex` — single self-contained file (no `.bib`/`.bbl`, no figures; packages `geometry`, `amsmath`, `booktabs`, `hyperref`, all arXiv-standard). Upload the one `.tex`.

**Status (2026-06-14):** source is arXiv-ready. Blocked on **(1) a clean compile + page count** and **(2) a cs.CR endorsement**. The preprint is *supplementary* (NOT part of the OSF + Bitcoin + Rekor triad) — not Day-0-blocking.

## Pre-submission checklist
- [ ] **Compile** on a TeX box (gentoo `emerge app-text/texlive`, or Overleaf) — confirm clean 2-pass build; record exact page count.
- [ ] **Endorsement** for `cs.CR` — the real blocker (see below).
- [x] arXiv account email = `mblake@everydayai.link` (done 2026-06-14).
- [ ] Submit with the metadata below; license **CC BY 4.0**.
- [ ] Moderation (~1+ business day; may reclassify category) → arXiv ID.

## Metadata (paste into arXiv)
- **Title:** PayBench: A Pre-Registered Methodology and Calibrated Mock Harness for Agent-to-Agent Payment-Rail Settlement Finality
- **Authors:** Michael Blake
- **Primary category:** `cs.CR`  ·  **Cross-list:** `cs.DC` (optionally `cs.PF`)
- **License:** CC BY 4.0
- **Comments:** "≈8 pages; methodology v1.2, preprint v1" — fill exact page count after compile
- **Abstract (plain text — `\emph`/`\textbf`/math stripped for arXiv's abstract field):**

This preprint describes a pre-registered measurement methodology and a calibrated mock harness; no real-rail funds are moved and no production rail-by-rail ranking is derived or published here. PayBench is an evaluation methodology and benchmark for agent-to-agent (A2A) payment rails. Its first dimension is settlement-finality: the wall-clock time from payment submission to the point at which an autonomous agent may rely on the payment for an irreversible downstream action. We make three contributions. First, a reliance-level doctrine for defining finality across heterogeneous rails (deterministic BFT close, probabilistic rooting, optimistic-rollup soft finality, hash-time-locked preimage release), pairing each rail's ecosystem-canonical reliance level with an explicit trust/equivalence class so that wall-clock comparisons never masquerade as security-model equivalence. Second, a comparative statistical method — Bradley-Terry maximum-likelihood estimation over pairwise finality races, complemented by pass@k = P(finality <= k) and Wilson lower-bound confidence intervals — with explicit caveats on its behaviour under cluster separation. Third, a cryptographic pre-registration protocol (OSF DOI + a transparency-log entry + an independent timestamp anchor + a signed source tag + this preprint) that fixes the design before any scored run, and that cleanly decouples methodology pre-registration from the later real-rail data pre-registration. The methodology and a reproducible mock harness are released as an open tool; publication of real-rail rankings is deferred.

## Endorsement (the blocker)
As an independent researcher on a non-academic email, you won't be auto-endorsed for your first `cs.CR` paper. Starting a submission yields an **endorsement code**; a qualified `cs.CR` author enters it at `arxiv.org/auth/endorse` (a ~2-minute attestation that the work fits the category — not peer review). One endorsement clears you.

**Pick the primary category for where a warm, qualified endorser exists** (the endorser must qualify for that exact class). `cs.CR` is pragmatic because the W3C **Credentials CG / A2WF** crowd you already correspond with publishes `cs.CR`. If a contact is stronger in distributed systems, `cs.DC` is an equally honest primary.

**Candidate endorsers (priority order):**
1. A W3C CCG / A2WF participant you've genuinely interacted with who publishes `cs.CR`.
2. A UK security / distributed-systems academic in your network (Cambridge / UCL / Imperial).
3. Stanford CRFM / Yifan Mai if that relationship develops (skews `cs.LG` → pair with a cross-list).

**Do NOT** cold-email random prolific `cs.CR` authors — arXiv asks endorsers to vouch only for people whose work they recognize; cold asks get declined.

**How to ask (research-framed, AgentPay-invisible):** short email — who you are (independent researcher, everydayai.link), one line on the paper, that it's your first arXiv submission needing a `cs.CR` endorsement, a link to the PDF, and the endorsement code. Make saying yes frictionless.
