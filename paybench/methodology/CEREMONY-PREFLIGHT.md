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

---
**Only when 1–7 pass:** run the runbook §2 freeze. Record the resulting manifest hash, then proceed to the
anchor steps (OpenTimestamps → cosign/Rekor → signed tag → OSF/DOI → arXiv).
