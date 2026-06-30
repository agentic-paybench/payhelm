# PayBench — competing interests & funding statement (public)

Benchmarks that rank third-party systems carry an inherent conflict-of-interest risk. The accepted standard
for managing it is **disclosure, not anonymity** (cf. ICMJE competing-interest practice). PayBench therefore
states its interests plainly here rather than presenting itself as an unaffiliated, interest-free "independent"
effort. This statement is public and is referenced from the methodology paper.

## Who runs PayBench, and the interest
PayBench is designed, operated, and published by the author (Michael Blake, everydayai.link) in connection with
the author's commercial work on agent-to-agent (A2A) payments. That work gives the author a **competing
interest**: a credible, openly-pre-registered benchmark of A2A payment rails also serves to establish technical
standing for that commercial work. A reader should weigh the benchmark in that light.

Concretely, the two design choices that openness and reproducibility **cannot** by themselves neutralise — and
which a conflicted operator could in principle exercise to flatter a preferred outcome — are:
1. **Rail selection** — which rails are included vs omitted; a favourable omission is undetectable from the
   frozen artefacts alone.
2. **Per-rail reliance level** (dimension 1) — each rail is pinned to its own ecosystem-canonical finality
   bar, and those bars are not equi-conservative (`methodology.md` §3).
The rail set under test includes rails the author's commercial work may integrate with, build upon, or compete
against. These choices are operator judgements and should be read as such.

## What is *not* the case
No rail operator or other third party commissioned, funded, or had pre-publication approval over this benchmark,
its design, or its results, and no party was paid for — or paid to obtain — any particular ranking.

## Mitigations (what reduces the residual risk, and what doesn't)
- **Cryptographic pre-registration (strong, but bounded).** The full design — rail set, definitions, metrics,
  seeds, fixtures — is frozen and triple-anchored before any scored run, so it provably cannot be tuned to a
  scored result after the fact. This guarantees the design was *fixed*, not that it was *neutral*: freezing a
  slanted design makes it auditable-as-consistent, not unbiased. Disclosure (this document) covers the gap.
- **Adversarial review of the two open-blind levers.** The per-rail reliance-level doctrine was tested by a
  four-model cross-LLM adversarial review (upheld 3–1 over the uniform-optimistic alternative). This is a
  mitigation, not independence, because the operator framed and reported it.
- **Pre-committed, mechanical rail-inclusion criteria (planned).** To remove discretion from rail selection,
  objective inclusion criteria will be pre-registered *before* the rail set is chosen for the next dimension /
  the real-rail run, so the comparison set is not a curated omission.
- **Open instrument.** Methodology, harness, and calibration provenance are released so any third party can
  re-run the design and propose alternatives; a right-of-reply / corrections posture is maintained
  (`methodology.md` §10, `ERRATA.md`).

## Branding
Earlier materials presented the work under a "PayBench / independent researcher" label with the commercial
affiliation de-emphasised. Going forward the affiliation and competing interest are disclosed (this document),
because concealment of a sponsor while publishing as "independent" is precisely the pattern the COI standard
exists to prevent.

Internal tracking: `gauntlet-r1-disposition-sheet.md` row **G-P3**; `DEFENSE-DOSSIER.md` §4 P3 / §6 G-P3.
