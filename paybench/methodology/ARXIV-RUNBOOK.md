# arXiv preprint — the public methods paper (defence-in-depth, longest lead time)

> **Execution note** (memory: `execution-ready-runsheets`). This file is the reusable **template** — it
> carries `<placeholders>`. To EXECUTE a specific instance, don't substitute by hand: ask me for a
> **fully-substituted runsheet** — every value pre-resolved (full hashes / block / Rekor index / commit /
> exact paths), each paste-block format-matched + **labelled with its destination field** (PLAINTEXT vs
> markdown), and artifacts pre-built. The operator substitutes nothing.


The public-scholarship leg. **Not part of the trust-anchor triad** (OSF DOI + Bitcoin + Rekor) — it's
additional defence-in-depth + dissemination. **Start the account/endorsement early**: a first-time submitter
usually needs an endorsement, which gates the whole timeline. Reusable across dimensions; **worked example =
dim-2 (RAPL)**. See also `paper/SUBMISSION.md` (the dim-1 metadata + compile/endorser checklist) and
`paper/payhelm-methods.tex` (the dim-1 methods paper to mirror/extend).

## Step 0 — endorsement (do this FIRST; it's the long pole)
- arXiv requires new submitters to be **endorsed** for a category before their first submission. Some
  affiliations auto-endorse; otherwise you need an existing arXiv author in that category to endorse you.
- Create the **arxiv.org** account (canonical identity — author **Michael Blake**, affiliation **Independent
  researcher**; keep the persona consistent with the OSF reg + the signed tag).
- Request endorsement for the **primary category** (below) early; track it. Nothing else gates on a date, but
  this can take days–weeks.

## Step 1 — the paper
- A **self-contained methods paper** rendered from the frozen doctrine (standard `article` +
  amsmath/booktabs/hyperref/geometry — compiles on arXiv's TeX Live). Either a **dim-specific paper** or a
  **section added** to the existing `paper/payhelm-methods.tex`.
  - *dim-2:* a RAPL methods paper (or a RAPL § in the existing paper) covering the SPLIT design, the
    measurement/stats package, DR4 group-and-decompose, and the FR1/FR4 conditions.
- **Category:** **`cs.PF`** (Performance — fits a latency benchmark) as primary, cross-listed **`cs.CR`**
  (the pre-registration / trust-anchor framing) and optionally `cs.DC`. *(dim-1 used cs.CR; pick what fits the
  dimension and keep cross-lists consistent.)*

## Step 2 — the three non-negotiables (cross-LLM hardening)
1. **Watermark in the TITLE** (F-req): the title MUST contain "Mock Harness" or "Simulated Fixtures" so the
   mock parameters can't be screenshotted as a real ranking. e.g.
   > *"PayBench: A Pre-Registered Methodology and Calibrated Mock Harness for Agent-to-Agent Payment-Rail
   > Authorization Latency"*
   Carry the mock-harness disclaimer into the abstract's first lines too.
2. **No real-rail leaderboard in the public preprint (F14-mirror).** Keep **per-rail absolute numbers OUT** of
   the public paper. Publishable: the doctrine + the **FR4-satisfied within-group *order*** (qualitative,
   e.g. "local-crypto ≪ facilitator-network; Solana < Stellar < Base across three topologies"), **not** a
   per-rail ms table. The full scored numbers live in the (embargoed) OSF registration, not the preprint.
3. **v1-only canonical (F17).** Embed the **manifest hash** in the PDF, and state in `<DIM>-PRE-REGISTRATION.md`
   that **only arXiv v1 is the canonical frozen version** (later revisions under the same arXiv id are
   post-freeze errata). arXiv allows same-id revisions, so this note prevents a later v2 being mistaken for the
   frozen claim.

## Step 3 — embed the anchors in the PDF
State, in the paper's pre-registration section: the manifest SHA-256, the Bitcoin block (OpenTimestamps), the
Rekor logIndex, the signed tag + commit, and the OSF DOI (once released) / OSF GUID.
- *dim-2:* hash `46a19eab…1dcd388`, Bitcoin block 955977, Rekor logIndex 2012836917, tag
  `paybench-rapl-prereg-v1`, commit `3dd74caa`.

## Step 4 — submit
1. Compile locally on TeX Live; fix any arXiv-flagged issues (it re-compiles server-side).
2. Upload source (`.tex` + any figures/`.bbl`) — arXiv prefers source over a bare PDF.
3. Set the category (primary + cross-lists), title (watermarked), abstract (disclaimer), authors.
4. Submit → arXiv assigns an **id** (e.g. `arXiv:26xx.xxxxx`). Note it; **v1 is canonical**.

## Step 5 — record + write-back
1. Add the **arXiv id** to the `*-CEREMONY-RUNBOOK.md` disposition (arXiv row) + the OSF page.
2. Do NOT edit the frozen narrative/manifest to carry the arXiv id (breaks the anchored hash) — it's process
   metadata. Tell me the arXiv id and I'll do the disposition write-back.

## Provenance posture (same as the other legs)
The preprint establishes **public precedence + dissemination**, not authorship of the commodity primitives
(JCS, SHA-256, cosign, OpenTimestamps). The original contribution is the **doctrine** (for dim-2: the SPLIT
authorization-primitive design + the DR4 group-and-decompose work-class methodology). Frame precedence at that,
never at the canonicalisation/anchoring technique.
