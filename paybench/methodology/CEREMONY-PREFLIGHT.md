# Pre-freeze preflight checklist (run BEFORE any pre-registration freeze)

> **Execution note** (memory: `execution-ready-runsheets`). This file is the reusable **template** — it
> carries `<placeholders>`. To EXECUTE a specific instance, don't substitute by hand: ask me for a
> **fully-substituted runsheet** — every value pre-resolved (full hashes / block / Rekor index / commit /
> exact paths), each paste-block format-matched + **labelled with its destination field** (PLAINTEXT vs
> markdown), and artifacts pre-built. The operator substitutes nothing.


A freeze + cryptographic anchor is a point of no return: once anchored, any change to the byte-set means
re-freezing from scratch. This checklist is the **routine gate** that must pass before generating a manifest
(`§2` of a `*-CEREMONY-RUNBOOK.md`). It exists because past freezes accreted avoidable rework — the fixes
below were all caught *late* (or only because someone asked "are you sure?"); run this and they're caught
*early, every time*.

Generic across dimensions. Substitute `DIM` = the dimension being frozen (e.g. `dim2`), `PRIOR` = the last
landed pre-reg (e.g. dim-1 / `methodology.md`). Each item has a **runnable check** and a **pass bar**.

## 1. Frozen-set completeness — parity with the PRIOR freeze
The manifest must freeze everything whose bytes the claim/reproduction depends on, not just the docs.
Mirror what `PRIOR` froze: **docs + harness CODE + provenance + fixtures + run reports** (tests excluded).
```
# what did the prior freeze include? (the parity template)
grep -v '^#' methodology/prereg-manifest.sha256 | awk '{print $2}' | sed -E 's#/.*##' | sort | uniq -c
# dry-run THIS dimension's manifest set (from the runbook §2) and confirm it resolves with no gaps:
{ sha256sum <the §2 file list> ; } > /tmp/DIM-manifest.sha256 2>/tmp/err; cat /tmp/err   # must be empty
sha256sum -c /tmp/DIM-manifest.sha256                                                     # all OK
```
**Pass bar:** every group the prior froze has a counterpart here; dry-run lists the expected file count with
**zero** "No such file" errors; `-c` verifies. *Provenance alone is NOT enough — code+fixtures+runs are what
pin the reproduction hash.*

**Freeze the whole decision pipeline, not just the output numbers.** If a pre-registered numeric *trigger*
exists (e.g. an FR1 censoring threshold), the **classifier/taxonomy that produces its input** must be frozen
too — the exact-string reject-reason → {harness_error, rejected, censored} decision table, not just the
percentage it is compared against. A frozen threshold fed by a mutable labeller is not pre-registered: the
free variable simply moves from the number to the label.
```
# any pre-registered trigger whose INPUT is computed by code not in the manifest? list them, confirm each input rule is frozen:
grep -rniE "censor|reject|trigger|threshold|harness_error" methodology/<the frozen docs>
```
**Pass bar:** every input to a pre-registered trigger is itself a frozen artefact (decision table / allowlist),
not a regex or routing rule living only in un-frozen code. *(This item exists because an FR1 censoring trigger's
reject-reason classifier was left out of a manifest — `gauntlet-r1-disposition-sheet.md` G-R4/R8.)*

## 2. Reproduction pinning + prior-artefact unperturbed
```
python3 -m paybench.mockbench.cli run -d <DIM-dimension(s)> | grep run_hash   # == the recorded hash(es)
python3 -m paybench.mockbench.cli run -d <PRIOR-dimension>  | grep run_hash   # == the FROZEN prior hash
python3 -m pytest paybench/mockbench/tests/ -q --noconftest                   # all pass (--noconftest: root conftest needs helm)
```
**Pass bar:** DIM reproduction hash(es) match what the docs claim; the PRIOR frozen `run_hash` is **byte-for-byte
unchanged** (a shared-code refactor must never perturb an already-anchored artefact); tests green.

## 3. No dangling refs from refactors
```
grep -rnE "\b<OLD_SYMBOL>\b" mockbench/ --include=*.py   # e.g. a removed/renamed dimension descriptor
```
**Pass bar:** no references to removed/renamed symbols anywhere the frozen code runs.

## 4. Internal consistency — no superseded-design tokens
The frozen docs must not contradict the ratified design or each other.
```
grep -niE "<superseded tokens for this dim>" methodology/<the frozen docs>
# dim-2 examples: 15.pair | C\(6,2\) | placeholder | NOT measured | candidate | stale-commit-SHA
```
**After any refactor, also diff the docs' STRUCTURAL claims against the actual code/files** — not just a
fixed token list. A rename (seed-domain format, fixture-filename pattern, dimension keys, schema strings)
leaves the docs describing the OLD shape unless you check. Diff doc-claimed identifiers vs. what the code
emits:
```
# e.g. seed domains the doc claims vs what the code produces:
python3 -c "from paybench.mockbench.dimensions import <DIMS>; ...print fixture_seed_domain / pair_seed_domain"
grep -oE "fixture:[a-z:<>-]+|<rail>-[a-z-]+\.(provenance\.yaml|fixture\.json)" methodology/<frozen docs> | sort -u
ls calibration/provenance/*<dim>* fixtures/*<dim>*    # the real filenames
```
**Pass bar:** no token describing a design the doctrine replaced; **every identifier the docs cite
(seed domains, file paths, dimension keys) matches the frozen code/files exactly**; cross-doc numbers/orders
agree. *(This item exists because a SPLIT refactor renamed the seed domains + fixtures, and the doctrine §5 +
narrative still described the pre-SPLIT shape — caught only on a human read-through.)*

## 5. Required clauses present (cross-LLM hardening)
```
grep -ciE "no real-rail funds|simulated.*harness|mock fixtures" methodology/<DIM>-PRE-REGISTRATION.md   # watermark
grep -ciE "independently sufficient|even if OSF" methodology/<DIM>-PRE-REGISTRATION.md                  # F16
```
**Pass bar:** watermark sentence (simulated harness / no real-rail funds / no production rankings) present;
F16 OSF-independence clause present.

## 6. Frozen-doc hygiene — "frozen = published; process stays out"
The byte-set will be read by an external researcher opening the OSF/arXiv record. It must carry only the
**timeless claim + registration metadata** — NOT session bookkeeping. Process lives in the runbook + pilot
log + git history (none frozen).
```
for f in <the frozen docs>; do
  echo "== $f =="
  grep -nE "\b[0-9a-f]{7,8}\b" $f | grep -viE "sha256:|seed|master"   # stray commit SHAs in prose
  grep -nE "✅|DONE 20|Remaining:|RATIFIED .*\(founder|frozen-candidate|cross-LLM review|pinned [0-9a-f]{7}" $f
  grep -nE "\b(19|20)[0-9]{2}-[0-9]{2}-[0-9]{2}\b" $f   # session dates (keep only registration-metadata dates)
done
```
**Allowed (registration metadata, mirrors PRIOR):** version line, decision-confirmed date, freeze date,
manifest/reproduction hashes, anchor table (DOI/logIndex/block), tag name.
**Not allowed (leakage):** working commit SHAs in prose, ✅/DONE logs, "Remaining:"/status banners,
origin tags like "(cross-LLM review)", IP addresses, resolution logs (those belong in the pilot log).
**Pass bar:** only registration-metadata dates/hashes remain; no status/log/origin scaffolding.

## 7. Born-clean going forward (prevent, don't clean up)
When **authoring** a to-be-frozen doc, never write session status, commit SHAs, dates, or origin tags into
its body — put them in the runbook / pilot log / commit message. The frozen doc is the published claim from
the first keystroke. (This is the shift-left version of item 6.)

## 8. Pre-freeze adversarial gauntlet — break it BEFORE you anchor
A freeze is provenance, not perfection: it proves the bytes existed, not that the design is beyond critique.
The hostile review that *will* happen post-publication must happen **pre-freeze**, so the gaps it finds are
fixed before the anchor instead of corrected by errata after. Run the dossier's gauntlet (`DEFENSE-DOSSIER.md`
§7 prompt) over THIS dimension's load-bearing decisions: spawn adversaries told to *break, not agree*, one per
defence cluster; an attack that survives is a finding.
```
# the gauntlet is a generative review, not a token grep — run it as agents over the frozen-candidate docs,
# then triage findings into: [DOC] over-claim · [DISC] disclose/relabel · [GAP] structural.
```
**Pass bar:** a full gauntlet round surfaces **no surviving `[GAP]`-tier** attack against the to-be-frozen
design (only already-disclosed `[DISC]`-tier items remain). If a `[GAP]` survives, fix it and re-run — do not
freeze on top of a known structural gap. *(This item exists because round 1 ran AFTER the freeze and its
findings — `gauntlet-r1-disposition-sheet.md` — had to be handled by errata + re-anchor instead of pre-empted.)*

## 9. Cross-dimension doctrine consistency — don't break a PRIOR dimension by improving this one
A new dimension's doctrine can silently contradict an already-anchored one. Before freezing, re-run every prior
dimension's load-bearing doctrine against this dimension's and confirm no contradiction (or that any difference
is principled and stated).
- **The split-vs-label rule (canonical, from `ERRATA.md` E1):** *split the comparison when the timed events
  differ in **kind**; use a trust/equivalence-class **label** when the **same** event differs in trust class.*
  Every dimension must apply this rule the same way — a dimension that splits on event-kind must not elsewhere
  race unlike events under a label, and a dimension that labels a trust-class difference must not be accused of
  needing a split it doesn't (there is no event-kind difference to split on).
```
# surface the relevant doctrine claims in each dimension and diff them by hand for the rule above:
grep -niE "split|trust.?class|equivalence.?class|category error|same (event|object)|differ in (kind|degree)" \
  methodology/<PRIOR frozen docs> methodology/<DIM frozen docs>
```
**Pass bar:** the split-vs-label rule is applied identically across all frozen dimensions; any cross-dimension
asymmetry (e.g. a per-rail-canonical reliance bar) is named and, where it could read as flattering, paired with
a neutralising secondary cut. *(This item exists because the RAPL split doctrine, frozen after finality, made
the finality single-race look contradictory — `gauntlet-r1-disposition-sheet.md` G-F1.)*

---
**Only when 1–9 pass:** run the runbook §2 freeze. Record the resulting manifest hash, then proceed to the
anchor steps (OpenTimestamps → cosign/Rekor → signed tag → OSF/DOI → arXiv). **8 and 9 are the gates added
after gauntlet round 1: break it and cross-check it BEFORE the anchor, not after.**

**Gates 8 & 9 are mechanically enforced at publish time.** Before tagging, copy
`freeze-evidence/TEMPLATE.md` to `freeze-evidence/<exact-tag-name>.md`, fill it in (`STATUS: PASS` with
`GATE8-GAUNTLET: PASS` + `GATE9-XDIM: PASS`), and **commit it in the same commit you tag**. The `freeze-guard`
pre-push hook and the `freeze-guard` CI job both refuse to publish a `paybench-*prereg*` tag without it
(`ceremony-hooks/README.md`; install once per clone with `ceremony-hooks/install-hooks.sh`). The guard forces
the attestation to exist and be anchored with the freeze — it does not run the gauntlet for you.
