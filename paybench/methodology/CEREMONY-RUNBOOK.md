# Pre-registration ceremony runbook (§9 execution)

**Gate status (2026-06-06): the cross-LLM adversarial review has CLEARED.** Four model families
(Gemini/DeepSeek/Kimi/Qwen) upheld D1 3–1 and D2 4/4; the zero-regen hardening is carried in v1.2 (no
fixture regen). The two Founder decisions are made (F14 de-rank, F1 prose-ack). This runbook is now
live. Anchoring commits the manifest hash permanently; if anything in the frozen set changes, re-freeze
first, regenerate the manifest, then run this.

> **⚠ Re-stamp note.** An earlier OpenTimestamps stamp was fired over the **v1.1** manifest hash
> `f0b9b079…009d99`. v1.2 (editorial Day-0 cleanup of `methodology.md`) **supersedes it** — the
> anchored value is now `a5f6feb4…d3a6f`. **Re-run `ots stamp` on the v1.2 manifest** (the v1.1 `.ots`
> is harmless but unused; no Bitcoin confirmation was lost). All anchors target v1.2.

**The anchored value** = the v1.2 manifest hash
`sha256:a5f6feb46819dc3926012a8a38ac519cd0d5df33c20734516dca4b32d30d3a6f`
(= `sha256sum paybench/methodology/prereg-manifest.sha256`). If any frozen file changes, regenerate
the manifest and this hash changes — re-anchor from scratch.

> **Scope: this runbook documents the DIMENSION-1 (settlement-finality, v1.2) pre-reg pass** (anchors +
> signed tag LANDED 2026-06-14). **Dimension-2 (RAPL / authorization-latency) is a SEPARATE, not-yet-run
> pass** reusing these same mechanics. Its frozen set = the **DR4-ratified doctrine** (`dim2-auth-latency`
> §2 + §2.5 + **§2.5.1 / DR4**, group-and-decompose), the confirmed **FR1** thresholds, the **FR4** topology
> list, and the **scored** per-rail `{median,P95,P99}` — see the dim-2 pre-registration-scope checklist in
> `dim2-auth-latency.DRAFT.md` §7. Do **not** start the dim-2 pass until topology-2 lands (numbers scored).

---

## 0. Where each step runs

| Step | Runs on | Blocker on the PVE host |
|---|---|---|
| OpenTimestamps | anywhere (headless OK) | `ots` not installed — `pipx install opentimestamps-client` |
| cosign + Rekor | **your interactive machine** (browser OIDC) | `cosign` not installed; keyless flow needs a browser |
| Signed git tag | **your interactive machine** (YubiKey plugged in) | YubiKey absent from `gpg --card-status` on this headless host |
| OSF registration | web | account/login |
| arXiv preprint | web + local LaTeX | account + (likely) endorsement; methodology not yet in paper form |

The two signing steps (cosign keyless, git tag) are deliberately human-gated — that is the point of a
trust-anchor ceremony. The PVE host is headless, so the YubiKey and browser-OIDC steps must run on
your laptop with the repo checked out at the **v1.2 freeze commit** (`aeab0640`).

## 1. Pre-flight (re-verify the frozen artefact)

```
cd paybench
sha256sum -c methodology/prereg-manifest.sha256          # 19/19 OK
sha256sum methodology/prereg-manifest.sha256             # == a5f6feb4…d3a6f
python3 -m paybench.mockbench.cli verify                 # fixtures vs provenance
python3 -m paybench.mockbench.cli run | grep run_hash    # == 895f99ed…14ee0 (mock-pipeline hash)
```

## 2. OpenTimestamps → Bitcoin anchor (do this first — non-interactive, headless OK) — DONE 2026-06-06

**Stamped over the v1.2 hash** (`ots info` confirms `a5f6feb4…`) and **CONFIRMED in Bitcoin block
952636** (2026-06-06, same-day; independently checked via the opentimestamps.org web verifier).
`ots upgrade` baked the Bitcoin attestation into the `.ots`; upgraded `.ots` committed (`7e268405`).
*(Gotchas: `ots stamp` refuses to overwrite an existing `.ots` — delete the stale one first if
re-stamping after a re-freeze. `ots upgrade` leaves a `.ots.bak` — don't commit it. `ots verify`
needs a local `bitcoind`; the web verifier or `ots info` is the no-node path.)*

```
pipx install opentimestamps-client            # or: pip install --user opentimestamps-client
cd paybench
ots stamp methodology/prereg-manifest.sha256  # writes prereg-manifest.sha256.ots immediately
# Bitcoin confirmation lands in a few hours; upgrade + verify later:
ots upgrade methodology/prereg-manifest.sha256.ots
ots verify  methodology/prereg-manifest.sha256.ots
```
Commit `prereg-manifest.sha256.ots` once stamped.

## 3. cosign signature → Rekor transparency log (your machine, browser)

**DONE 2026-06-06** — Rekor **logIndex `1740328355`**; bundle committed (`b6188941`). Modern cosign
(≥ 2.x) deprecated `--output-signature/--output-certificate` and defaults to a single bundle, so the
working command is `--bundle` (one JSON file = signature + cert + tlog entry):
```
# install: see https://docs.sigstore.dev/cosign/installation
cosign sign-blob --yes \
  --bundle paybench/methodology/prereg-manifest.sha256.cosign.bundle \
  paybench/methodology/prereg-manifest.sha256
# keyless: opens a browser for OIDC; signature + cert + Rekor entry land in the bundle.
# Rekor logIndex:  jq -r '.verificationMaterial.tlogEntries[0].logIndex' …cosign.bundle
# verify:          cosign verify-blob --bundle …cosign.bundle \
#                    --certificate-identity-regexp '.*' --certificate-oidc-issuer-regexp '.*' …sha256
```
Bundle committed (replaces the old `.sig`/`.pem` artefacts).

## 4. Signed git tag (your machine, YubiKey plugged in) — LANDED 2026-06-14

> **Landed 2026-06-14.** Signed `paybench-prereg-v1.2` (tag obj `225c26a8…`) on `aeab0640` with the
> YubiKey OpenPGP ed25519 signing subkey `B61635C9…286042AC` (master `887BEAFA…`) and pushed to origin.
> Signer identity `Michael Blake <mblake@everydayai.link>` — the key's UID was changed from the
> as-provisioned `michael@everydayai.link` to the canonical address *before* publishing (see the agentpay
> ceremony checklist §9). Public key uploaded + verified on keys.openpgp.org. The tag is *supplementary*
> defence-in-depth, **not part of the trust-anchor triad** (OSF DOI + Bitcoin + Rekor); it points at the
> immutable commit `aeab0640`. (Issuance + dual-card + UID-change procedure: the YubiKey issuance
> ceremony checklist §§5,9 in the agentpay repo.)

```
gpg --card-status                              # confirm the YubiKey OpenPGP key is present
git config user.signingkey <YUBIKEY_KEYID>     # if not already
git tag -s paybench-prereg-v1.2 aeab0640 \
  -m "PayBench settlement-finality pre-registration — methodology v1.2; manifest a5f6feb4…d3a6f"
git tag -v paybench-prereg-v1.2                # verify the signature
git push origin paybench-prereg-v1.2           # requires the commit to be pushed (step 6)
```
Per the project signing-key posture, this load-bearing anchor is **hardware-signed** (YubiKey
OpenPGP), not a software dev key.

## 5. OSF pre-registration → DOI (web)

Create an OSF registration; paste `PRE-REGISTRATION.md` as the registration narrative; attach (or
link to the tagged commit of) `prereg-manifest.sha256` + `methodology.md`. Record the resulting DOI
into `PRE-REGISTRATION.md`. The DOI is the human-readable leg of the trust-anchor triad.

- **Watermark (cross-LLM review).** The OSF abstract's first sentence must state: *"This
  pre-registration covers a simulated harness and calibrated mock fixtures; no real-rail funds are
  moved and no production rankings are derived."* If a "simulation / no real-world subjects" field
  exists, set it.
- **Anchor robustness (cross-LLM F16).** The OSF DOI resolves to a URL = a single point of failure.
  Independently archive `PRE-REGISTRATION.md` + `prereg-manifest.sha256` (Internet Archive / IPFS),
  and note in `PRE-REGISTRATION.md` that the **Rekor entry + OpenTimestamps proof are independently
  sufficient** to establish the freeze date even if OSF is unavailable.
  - **Part 1 — DONE 2026-06-17.** Internet Archive item
    <https://archive.org/details/methodology_202606> (IA-stamped 17 Jun 2026). Archived all 5 OSF
    attachments — `PRE-REGISTRATION.md`, `methodology.md`, `prereg-manifest.sha256`, plus the `.ots`
    and `.cosign.bundle` proof files — so the item is self-verifying (re-check Bitcoin + Rekor
    against hash `a5f6feb4…` without OSF or the repo). IA satisfies the "/" requirement; IPFS not
    needed. (Snapshot is the pre-DOI version, which is correct as a freeze-time record.)
  - **Part 2 — pending:** add the explicit "Rekor + OpenTimestamps independently sufficient even if
    OSF unavailable" sentence to `PRE-REGISTRATION.md`; bundle it with the post-submission DOI
    write-back (one edit, then re-attach + optionally re-archive).
- **Embargo.** Register under an OSF embargo to **2026-07-17 (POC Day-0)**, early-release permitted
  (OSF supports ending an embargo before its date). The embargo gates only the OSF-hosted narrative
  + attachments; the OpenTimestamps (Bitcoin block 952636) and Rekor (logIndex 1740328355) anchors
  are already public from 2026-06-06, so the freeze date itself is *not* embargoed. Rationale:
  syncs the OSF registration's public visibility with the rest of the Day-0 ship bundle. **Set this
  in the OSF UI at registration time — it is a platform setting, not recorded in the frozen
  artefacts** (`PRE-REGISTRATION.md` and the 19-file manifest are immutable / uploaded; do not edit
  them to carry process decisions).

## 6. Push the frozen commit (prerequisite for the tag in step 4) — DONE 2026-06-06

Branch renamed `paybench/methodology-rough-draft` → **`paybench/poc`** and pushed to `origin`
(tracking). The **v1.2 freeze commit** (`aeab0640`) is on the remote, so the step-4 tag can
reference it. (Fork `main` stays pristine HELM until the Day-0 cutover; the tag lands on
`paybench/poc`.)

## 7. arXiv preprint (longest lead — start the account/endorsement early)

**Draft ready:** `paybench/methodology/paper/payhelm-methods.tex` — a self-contained methods paper
rendered from `methodology.md` v1.2 (standard `article` + amsmath/booktabs/hyperref/geometry; compiles
on arXiv's TeX Live). It honours F14 (no per-rail finality numbers / no ranking in the public preprint),
carries the watermarked title, the mock-harness abstract disclaimer, the manifest hash, and the
v1-only-canonical note. **Identity resolved 2026-06-06:** author = **Michael Blake**, affiliation =
**Independent researcher**, contact = everydayai.link (the platform brand stays invisible; the paper
uses "PayBench"). **One thing left before submission:** pick the category (**cs.CR** crypto & security, or
cs.DC distributed computing — cs.CR fits the pre-registration / trust-anchor framing best). Then
submit to arXiv. A first-time submitter may need an endorsement — begin that early, as it gates the
timeline.

- **Watermark (cross-LLM review).** The title must contain "Mock Harness" or "Simulated Fixtures" —
  e.g. *"PayBench: A Pre-Registered Methodology and Calibrated Mock Harness for Agent-to-Agent
  Payment Rails"* — so the mock parameters can't be screenshotted as a real ranking.
- **v1-only canonical (cross-LLM F17).** arXiv allows post-submission revisions under the same id;
  embed the manifest hash in the PDF and state in `PRE-REGISTRATION.md` that only arXiv **v1** is the
  canonical frozen version (later revisions are post-freeze errata).

---

## Record dispositions here as anchors land

| Anchor | Status | Reference |
|---|---|---|
| OpenTimestamps (Bitcoin) | **DONE — confirmed Bitcoin block 952636** | `prereg-manifest.sha256.ots` over `a5f6feb4…`; upgraded + committed `7e268405` |
| cosign → Rekor | **DONE** | Rekor logIndex `1740328355`; `prereg-manifest.sha256.cosign.bundle`, committed `b6188941` |
| Signed git tag | **DONE — landed 2026-06-14** | `paybench-prereg-v1.2` (tag obj `225c26a8…`) on `aeab0640`; signer `mblake@everydayai.link`, key `887BEAFA…` on keys.openpgp.org |
| OSF DOI | in progress | DOI: — (register under embargo to 2026-07-17, early-release permitted) |
| arXiv | pending | paper drafted (`paper/payhelm-methods.tex`); category cs.CR; needs endorsement |

## Provenance posture (what the anchors prove — and what they do not)

The anchors above (OpenTimestamps / cosign→Rekor / signed tag / OSF DOI / arXiv) prove **precedence,
integrity, and signer-identity** — **not authorship or originality** of the cryptographic primitives.
Concede the commodity ground explicitly and point the precedence at the real moat:

> JCS (RFC 8785), SHA-256 (FIPS 180-4), cosign, and OpenTimestamps are commodity public standards used
> here as-is and claimed by no one; PayBench's original contribution is the per-rail-canonical
> reliance-level finality doctrine (D1) and the calibrated mock-fixture methodology (BT-MLE with a
> symmetric smoothing prior + pass@k as P(finality ≤ k) + Wilson lower-bound CIs), for which this
> pre-registration establishes precedence.

This inoculates against an AlgoVoi-style ownership claim over the JCS/SHA-256 primitives (fails on its
face) and names what the anchors *do* defend. **Never** frame the canonicalisation / content-addressing
technique as the contribution. *Residual caveat:* precedence loses to an earlier timestamp — if the
contribution were ever (wrongly) framed as the *JCS-over-finality-fixtures technique* and the
`draft-hopley-x402-canonicalisation-jcs` / `-settlement-attestation` drafts predate the v1.2 hash
(`a5f6feb4…`, 2026-06-06), PayBench would be the later filer; mitigation is the framing above (optionally
check the datatracker first-revision dates). Mirrored into the arXiv methods paper
(`paper/payhelm-methods.tex`, Pre-registration §). Source: Session-5 VCX deep-read; ADR-005; Decisions
DB 2026-06-22. **The frozen v1.2 manifest set is untouched** (editing it would break the `a5f6feb4…` anchors).
