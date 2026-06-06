"""PayBench — a benchmark for agent-to-agent payment rails.

This package sits deliberately *outside* the upstream HELM ``src/`` tree (HELM's
setuptools config discovers only ``src/``), keeping the fork-first / upstream-second
boundary clean. Subpackages:

* ``paybench.mockbench`` — the N16 MockBench settlement-finality harness.

Non-code siblings (data / docs, not Python subpackages): ``calibration/``,
``methodology/``, ``fixtures/``, ``runs/``.
"""
