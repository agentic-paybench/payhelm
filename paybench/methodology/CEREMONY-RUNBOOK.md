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

## 4. Signed git tag (your machine, YubiKey plugged in) — DEFERRED 2026-06-06

> **Deferred, by design — not a blocker.** The signed tag is *supplementary* defence-in-depth, **not
> part of the trust-anchor triad** (OSF DOI + Bitcoin + Rekor). It points at the immutable commit
> `aeab0640`, so it can be added any time later and is exactly as valid. Deferred because the YubiKey
> is factory-fresh (`gpg --card-status` → `Signature key: [none]`); hardware-signing requires the
> OpenPGP key to be provisioned first. Per the closed decision (primary + backup, cold storage),
> provisioning is its own airgapped issuance ceremony — see the YubiKey issuance ceremony checklist in
> the agentpay working repo. **Run that ceremony, then create this tag on `aeab0640` before Day-0.**
> (`gpg --card-status` access on this host needed `disable-ccid` in `~/.gnupg/scdaemon.conf` to get
> past a pcscd/scdaemon turf war.)

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
| Signed git tag | **DEFERRED** (YubiKey provisioning) | `paybench-prereg-v1.2` on `aeab0640` — after the issuance ceremony, before Day-0 |
| OSF DOI | in progress | DOI: — |
| arXiv | pending | paper drafted (`paper/payhelm-methods.tex`); category cs.CR; needs endorsement |
