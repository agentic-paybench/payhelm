# OSF pre-registration → DOI (anchor ceremony, the OSF leg)

The human-readable leg of the trust-anchor triad (the other two — Bitcoin via OpenTimestamps, Rekor via
cosign — are cryptographic). OSF mints a **DOI** over a frozen snapshot + your narrative. Reusable across
dimensions; **worked example = dim-2 (RAPL)** in call-outs. Companion to `*-CEREMONY-RUNBOOK.md` §5/§6 and the
"GPG-signed git tags" cheat sheet (the tag leg).

## Prerequisites (all already true for dim-2)
- The freeze is done: `<DIM>-prereg-manifest.sha256` exists; its sha256 is the **anchored hash**.
  - *dim-2:* `46a19eab516ef3214270513f718bd07a846e18a4f42d9916fcb829da71dcd388`, freeze commit `3dd74caa`.
- The narrative exists: `<DIM>-PRE-REGISTRATION.md` (this is what you paste into OSF).
  - *dim-2:* `paybench/methodology/dim2-PRE-REGISTRATION.md`.
- Ideally the Bitcoin + Rekor anchors are already public (they are for dim-2: Rekor logIndex `2012836917`;
  OTS stamped, Bitcoin confirming) — so the freeze date is provable **independently of OSF** (F16).

## Key facts about OSF registrations (so you set it up right)
- An OSF **Registration** is an **immutable, time-stamped, frozen snapshot** of an OSF *Project*, with its own
  **DOI** — but for an **embargoed** registration the DOI is **issued at release**, not at submission (Step 4).
  You cannot edit a registration after it's submitted (only withdraw → leaves a tombstone).
- **Embargo** delays *public visibility* (and DOI issuance) up to 4 years; the **registration is time-stamped
  now** (and you can end the embargo early). So an embargo does **not** hide the freeze date — and for us the
  freeze date is independently anchored anyway (Bitcoin + Rekor).
- A registration snapshots the **Project's files + a registration form**. So: create a Project, upload the
  artefacts to it, fill the form, then register.

## Step 1 — account + project (ONE PayBench project across all dimensions)
1. Sign in at **osf.io** (canonical identity `mblake@everydayai.link`; keep the persona consistent with the
   signed tag + arXiv). Create the account if first time.
2. **Do NOT create a separate top-level project per dimension.** dim-1 (settlement-finality) and dim-2 (RAPL)
   are two dimensions of the **same** benchmark → they share one **PayBench** project (one coherent,
   discoverable body of work). Each *Registration* is its own immutable, separately-DOI'd snapshot, so the
   **per-dimension DOI is preserved regardless** of sharing the project.
3. **Recommended — a Component per dimension.** In the PayBench project, add a **Component** ("Authorization
   latency — RAPL") and **register that component** (Step 3). Its snapshot then contains only this dimension's
   files → a clean per-dimension DOI. *(Simpler alternative: register the whole project a second time for
   dim-2 — also fine, but the snapshot then includes dim-1's files too; the narrative scopes the claim.)*
4. **If dim-1's OSF is already a standalone project:** either add dim-2 as a component/registration there, or
   leave dim-2 alongside it — the cryptographic anchoring (Bitcoin + Rekor + signed tag) is the *real* freeze;
   OSF is the human-readable leg, so project structure affects **discoverability, not correctness**.
5. Keep the project **private**; the registration's **embargo** controls public release.

## Step 2 — upload the frozen artefacts to the project
Upload to the project's OSF Storage (these become part of the immutable snapshot):
- `<DIM>-PRE-REGISTRATION.md` (the narrative)
- `<DIM>-prereg-manifest.sha256` (the byte-set manifest — the anchored value)
- the doctrine (`<DIM>-auth-latency.md`) + `<DIM>-scored-results.md`
- the proof files so the item is **self-verifying**: `<DIM>-prereg-manifest.sha256.ots` and
  `…​.cosign.bundle`
- a one-line pointer to the immutable git tag (the full byte-set lives there).
  - *dim-2 tag:* `paybench-rapl-prereg-v1` → commit `3dd74caa` (`github.com/agentic-paybench/payhelm`).

## Step 3 — create the registration
1. In the project: **Registrations → New registration → "Open-Ended Registration"** (free-form; lets you paste
   the narrative + keep the attached files. The structured "OSF Preregistration"/"AsPredicted" templates are
   hypothesis-test oriented and a poor fit for a methodology freeze.)
2. **Summary / narrative:** paste `<DIM>-PRE-REGISTRATION.md`.
3. **⚠ Watermark — first sentence of the summary/abstract MUST read** (cross-LLM hardening; non-negotiable):
   > *"This pre-registration covers a simulated harness and calibrated mock fixtures; no real-rail funds are
   > moved and no production rankings are derived."*
   If OSF exposes a "simulation / no human subjects / no real-world data" field, set it.
4. **State the anchored hash in the body** so the DOI ties to the exact byte-set:
   > *"The frozen byte-set is the file set in `<DIM>-prereg-manifest.sha256`, whose SHA-256 is `<hash>`,
   > independently anchored in Bitcoin (OpenTimestamps) and Rekor (logIndex `<idx>`), and signed-tagged
   > `<tag>` on commit `<commit>`."*
   - *dim-2:* hash `46a19eab…1dcd388`, Rekor `2012836917`, tag `paybench-rapl-prereg-v1`, commit `3dd74caa`.

## Step 4 — embargo, then submit
1. Set **Embargo end date = POC Day-0 `2026-07-17`** (early release permitted). This syncs the OSF page's
   public visibility with the Day-0 ship bundle; the anchors are already public so the freeze date isn't hidden.
2. **Submit.** OSF **time-stamps the registration immediately** (the freeze date is recorded now), BUT for an
   **embargoed** registration the **DOI is only issued / becomes resolvable when the embargo is released** —
   *not at submission*. So the dim-2 DOI does not exist until the **2026-07-17 release** (or an early release).
   Nothing is gated on it: the freeze date is already independently anchored by Bitcoin + Rekor.
3. **At embargo release**, copy the **DOI** (form `10.17605/OSF.IO/XXXXX`). Until then the OSF disposition
   reads "registered + embargoed; **DOI on release**".

## Step 5 — F16 independent archive (don't skip)
The DOI is a single URL = a single point of failure. Independently archive so the freeze is self-verifying
without OSF:
- **Internet Archive:** submit `<DIM>-PRE-REGISTRATION.md` + `<DIM>-prereg-manifest.sha256` (+ `.ots` +
  `.cosign.bundle`) at **web.archive.org/save** (or upload an item at archive.org). Note the IA URL.
- Confirm the narrative already states "Rekor + OpenTimestamps independently sufficient even if OSF
  unavailable" (it does for dim-2 — the F16 clause in `dim2-PRE-REGISTRATION.md`).

## Step 6 — write the DOI back + record dispositions (at embargo release)
The DOI only arrives at **embargo release** (Step 4) — so this step happens on **2026-07-17** (or early
release), not at registration. Until then, the disposition reads "registered + embargoed; DOI on release."
The narrative + manifest are **immutable / uploaded** — do NOT edit them to carry the DOI (it would break the
anchored hash). Record the DOI in the **process** docs only:
1. Add the DOI to the `*-CEREMONY-RUNBOOK.md` disposition table (OSF row).
2. (Optional) note it in the project README / Notion. Tell me the DOI + IA URL and I'll do the disposition
   write-back from devbox.

## Note on the existing OSF project metadata (the umbrella)
The PayBench OSF **project** (id `Gv8j7`) currently has **dim-1-specific** title/description ("settlement-finality
methodology v1.2"). To host dim-2 under the same project (Step 1), **generalize the project metadata to the
umbrella** — title/description covering *both* dimensions. This is safe: the project is mutable and editing it
does **not** alter any already-created registration (registrations are immutable snapshots). Put the
dimension-specific wording in the per-dimension **component/registration**, not the umbrella project.

---
**Triad after this step:** OSF DOI ✅ + Bitcoin ✅ + Rekor ✅ = the full three-anchor triad, no single point of
trust. The signed git tag + arXiv are additional defence-in-depth. **Never** edit the frozen byte-set to carry
process metadata (DOI, dates) — that breaks the anchored hash; process lives here, in git, and in Notion.

---

## Worked example — dim-2 ready-to-paste OSF text

### Umbrella PROJECT (Gv8j7) — generalize to cover both dimensions
**Title:** `PayBench: pre-registration of an agent-to-agent payment-rail benchmark methodology`

**Description:**
> Pre-registrations of the PayBench agent-to-agent payment-rail benchmark methodology. Each dimension's full
> measurement design and analysis plan is frozen and independently anchored before any scored run, so no
> element can be accused of having been chosen to flatter a rail. This covers a simulated harness and
> calibrated mock fixtures; no real-rail funds are moved and no production rankings are derived.
>
> Dimension 1 — settlement-finality (methodology v1.2, frozen 2026-06-06): manifest sha256 a5f6feb4…d3a6f,
> anchored via OpenTimestamps (Bitcoin block 952636) + cosign/Rekor (logIndex 1740328355).
>
> Dimension 2 — authorization-latency (RAPL) (frozen 2026-06-29): manifest sha256 46a19eab…1dcd388, anchored
> via OpenTimestamps (Bitcoin block 955977) + cosign/Rekor (logIndex 2012836917), signed tag
> paybench-rapl-prereg-v1.
>
> Each dimension is a separate registration with its own DOI. Frozen methods + cryptographic manifests are in
> the attached files / per-dimension registrations.

### dim-2 COMPONENT — "Authorization latency (RAPL)"
**Title:** `PayBench: pre-registration of an authorization-latency (RAPL) benchmark methodology (dim-2)`

**Description:**
> Pre-registration of the PayBench authorization-latency benchmark methodology — Rail Authorization-Primitive
> Latency (RAPL), dimension 2, frozen 2026-06-29. It fixes the full measurement design and analysis plan
> before any scored run, so no element can be accused of having been chosen to flatter a rail: the SPLIT design
> (two never-cross-raced sub-rankings — A Payment-Validation and B Challenge-Issuance, C(5,2)=10 pairs each),
> the t=0 / last-byte stopwatch with same-path RTT subtraction, the millisecond P(auth≤k) ladder, a hardened
> Bradley-Terry model (Davidson ties + censoring/competing-risks) with a pre-specified FR1-triggered Cox-PH
> survival fallback, Wilson lower-bound intervals and Kaplan-Meier curves, the DR4 group-and-decompose
> work-class analysis, the FR4 ≥2-topology requirement, the RNG seed-namespace, and the calibrated
> mock-fixture hashes. This covers a simulated harness and calibrated mock fixtures; no real-rail funds are
> moved and no production rankings are derived. The frozen method and a cryptographic content manifest are in
> the attached files; the manifest hash
> (sha256:46a19eab516ef3214270513f718bd07a846e18a4f42d9916fcb829da71dcd388) is independently anchored via
> OpenTimestamps (Bitcoin block 955977) and a cosign signature in the Rekor transparency log
> (logIndex 2012836917), and signed-tagged paybench-rapl-prereg-v1 on commit 3dd74caa. Full detail is in the
> Summary field and the attached dim2-PRE-REGISTRATION.md.
