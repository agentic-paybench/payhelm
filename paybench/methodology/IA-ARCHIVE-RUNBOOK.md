# Internet Archive (F16) — independent, self-verifying archive of a pre-registration freeze

The **robustness leg** (cross-LLM F16). The OSF DOI resolves to a single URL = a single point of failure;
the git repo can move or go private. This step puts the **self-verifying minimum** on a third, independent,
date-stamped public host (the Internet Archive) so the freeze can be checked **without OSF and without the
repo**. Reusable across dimensions; **worked example = dim-2 (RAPL)**.

## Why it's self-verifying without OSF or the repo
The manifest's SHA-256 is anchored in **Bitcoin** (OpenTimestamps) and **Rekor** (cosign) — both public,
permanent, and independent of OSF/GitHub. So a third party only needs: the **manifest** + the **two proof
files** + the **narrative** (which states the block + logIndex). From those they can: `sha256sum` the manifest
→ compare to the `.ots`/`.cosign.bundle` → confirm the Bitcoin block + Rekor entry. The Internet Archive
preserves that bundle publicly and stamps the upload date.

## What to upload (the self-verifying set — 4 files)
- `<DIM>-PRE-REGISTRATION.md` — the narrative (states the hash, block, logIndex, tag)
- `<DIM>-prereg-manifest.sha256` — the anchored byte-set manifest
- `<DIM>-prereg-manifest.sha256.ots` — Bitcoin (OpenTimestamps) proof
- `<DIM>-prereg-manifest.sha256.cosign.bundle` — Rekor (cosign) proof
*(Optional, for completeness: the doctrine + scored-results, or the whole `<DIM>-frozen-set.zip`. The IA item
has no 5-file cap, unlike OSF — so you can add the doctrine + scored-results directly here if you bundled them
on OSF.)*

## Step 1 — choose the IA mechanism
Two independent, complementary archives — **do both**:
- **(a) An archive.org ITEM** (upload the files above). This is the durable, self-verifying bundle. *(dim-1
  used this: `archive.org/details/methodology_202606`.)*
- **(b) Wayback snapshots of the PUBLIC anchor URLs** via `web.archive.org/save` — snapshots the *evidence
  that already lives elsewhere*, so it survives those hosts moving. (You cannot snapshot the embargoed OSF
  page — it's private — so the ITEM in (a) carries the narrative instead.)

## Step 2 — the archive.org ITEM (a)
1. Sign in at **archive.org** (create an account if first time).
2. **Upload → Upload files** → create a new item.
3. **Title:** e.g. `PayBench <DIM> pre-registration freeze — <topic> (frozen <date>)`.
   - *dim-2:* `PayBench dim-2 (RAPL) authorization-latency pre-registration freeze — frozen 2026-06-29`.
4. Add the 4 self-verifying files (+ any optional extras).
5. **Description** (paste; plain text is fine here): a short verifier's note —
   > Frozen pre-registration byte-set for PayBench <DIM>. Manifest SHA-256
   > `sha256:<hash>`, independently anchored in Bitcoin via OpenTimestamps (block <block>) and in the Rekor
   > transparency log via cosign (logIndex <idx>), and signed-tagged `<tag>` on commit `<commit>`. To verify
   > without OSF or the repo: `sha256sum <DIM>-prereg-manifest.sha256` must equal the hash above; check the
   > `.ots` (e.g. `ots verify` / opentimestamps.org) for the Bitcoin block and the `.cosign.bundle` /
   > `search.sigstore.dev` for the Rekor entry.
   - *dim-2:* hash `46a19eab…1dcd388`, block 955977, logIndex 2012836917, tag `paybench-rapl-prereg-v1`,
     commit `3dd74caa`.
6. **Subject/keywords:** pre-registration, benchmark, agent-to-agent payments, OpenTimestamps, Rekor, <topic>.
7. Save → note the **`archive.org/details/<id>` URL**.

## Step 3 — Wayback snapshots of the public anchor URLs (b)
At `web.archive.org/save`, snapshot each (paste URL, "Save Page Now"):
- the **GitHub tag/commit** page (the immutable frozen commit) — e.g.
  `github.com/agentic-paybench/payhelm/releases/tag/<tag>` or `…/commit/<commit>`.
- the **Rekor entry** — `search.sigstore.dev/?logIndex=<idx>` (and/or the rekor.sigstore.dev API URL).
- *(OpenTimestamps proof is in the IA item already; the Bitcoin block itself is on every Bitcoin explorer.)*
Note each resulting Wayback URL.

## Step 4 — record + write-back
1. Add the **IA item URL** (+ key Wayback URLs) to the `*-CEREMONY-RUNBOOK.md` disposition (IA row).
2. The narrative/manifest are immutable — do NOT edit them to carry the IA URL (it breaks the anchored hash).
   The IA URL is process metadata; it lives in the runbook + the OSF page, not the frozen byte-set.
3. Tell me the IA item URL and I'll do the disposition write-back from devbox.

---
**After this:** the freeze is preserved on **three independent public substrates** — Bitcoin, Rekor, and the
Internet Archive — plus OSF (DOI on release) and the signed git tag. No single host's disappearance can erase
the freeze date or the byte-set.
