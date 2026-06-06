# Pre-registration ceremony runbook (§9 execution)

**Gate status (2026-06-06): the cross-LLM adversarial review has CLEARED.** Four model families
(Gemini/DeepSeek/Kimi/Qwen) upheld D1 3–1 and D2 4/4; v1.1 applied their zero-regen hardening (no
fixture regen). The two Founder decisions are made (F14 de-rank, F1 prose-ack). This runbook is now
live. Anchoring commits the manifest hash permanently; if anything in the frozen set changes, re-freeze
first, regenerate the manifest, then run this.

**The anchored value** = the v1.1 manifest hash
`sha256:f0b9b079e72fcfdadde976be9ee5cdcd5ac893e86e86e875b440ac13e3009d99`
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
your laptop with the repo checked out at the **v1.1 freeze commit** (`dfbb93b3`).

## 1. Pre-flight (re-verify the frozen artefact)

```
cd paybench
sha256sum -c methodology/prereg-manifest.sha256          # 19/19 OK
sha256sum methodology/prereg-manifest.sha256             # == f0b9b079…009d99
python3 -m paybench.mockbench.cli verify                 # fixtures vs provenance
python3 -m paybench.mockbench.cli run | grep run_hash    # == 895f99ed…14ee0 (mock-pipeline hash)
```

## 2. OpenTimestamps → Bitcoin anchor (do this first — non-interactive, headless OK)

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

```
# install: see https://docs.sigstore.dev/cosign/installation
cosign sign-blob \
  --yes \
  --output-signature  paybench/methodology/prereg-manifest.sha256.sig \
  --output-certificate paybench/methodology/prereg-manifest.sha256.pem \
  paybench/methodology/prereg-manifest.sha256
# keyless: opens a browser for OIDC; the signature + cert are logged to Rekor automatically.
# Record the Rekor log index/UUID printed to stderr into PRE-REGISTRATION.md.
```
Commit the `.sig` and `.pem`.

## 4. Signed git tag (your machine, YubiKey plugged in)

```
gpg --card-status                              # confirm the YubiKey OpenPGP key is present
git config user.signingkey <YUBIKEY_KEYID>     # if not already
git tag -s paybench-prereg-v1.1 dfbb93b3 \
  -m "PayBench settlement-finality pre-registration — methodology v1.1; manifest f0b9b079…009d99"
git tag -v paybench-prereg-v1.1                # verify the signature
git push origin paybench-prereg-v1.1           # requires the commit to be pushed (step 6)
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

## 6. Push the frozen commit (prerequisite for the tag in step 4)

Branch `paybench/methodology-rough-draft` is local-only. Decide topology first (see the session
hand-off): push the branch as-is, rename it (the "rough-draft" name is now stale), or merge to the
fork's `main` so the tag lands on canonical history. Whichever — the tag in step 4 must reference a
**pushed** commit.

## 7. arXiv preprint (longest lead — start the account/endorsement early)

The methodology is not yet in paper form. Render `methodology.md` → a short methods paper (LaTeX),
then submit to arXiv (cs.CR / cs.DC). A first-time submitter may need an endorsement — begin that
process before the rest, as it gates the timeline.

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
| OpenTimestamps (Bitcoin) | pending | `prereg-manifest.sha256.ots` |
| cosign → Rekor | pending | Rekor UUID: — |
| Signed git tag | pending | `paybench-prereg-v1.1` |
| OSF DOI | pending | DOI: — |
| arXiv | pending | arXiv id: — |
