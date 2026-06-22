**(1) FC1–FC4**

**FC1:** **yes-with-caveat.** Excluding the fused-settlement primitive removes the contamination, but the omission must be flagged in the main text — not relegated solely to an appendix — to avoid the appearance of cherry-picking the fast path.

**FC2:** **yes.** The split preserves the category-error fix by keeping A and B as separate same-kind races; x802’s dual presence is unambiguous because the two entries are functionally distinct primitives (validation vs. issuance), and RR6’s scope tags prevent reader conflation.

**FC3:** **adequate.** A pre-specified, data-triggered fallback is inferentially valid provided the trigger thresholds (transitivity violation, tie-rate, censoring-rate) are enforced mechanically without post-hoc adjustment; it defers survival modeling until domain evidence demands it.

**FC4:** **sufficient-with-caveat.** RR4–RR6 close the major confounds, but the first-byte stopwatch in RR4 is now misaligned with RR5’s expanded checkpoint scope: a rail can emit a spurious protocol byte (e.g., HTTP headers, framing whitespace) before completing the required signature verification and state read, gaming latency without technically violating RR5.

**(2) NEW fatal introduced by the refinements**

The conjunction of **RR4** (first-byte measurement) and **RR5** (mandated work scope) creates an exploitable timing gap: a fully compliant rail can satisfy the “signature verification + fresh state read” checklist while the stopwatch stops on an early wire byte, rendering the ranking gameable by protocol-framing gymnastics. The measurement event must be re-anchored to the *last byte of the authorization response payload* (or a protocol-level end-of-auth marker), not the first byte on the wire.

**(3) One-line verdict**

**NOT PRE-REGISTERABLE** until RR4 is tightened to measure completion of the checkpointed authorization payload rather than first-byte; with that single alignment fix, the dimension is coherent and fully pre-registerable.
