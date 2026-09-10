# PayBench

**A pre-registered, rail-neutral measurement methodology for agent-to-agent payment rails, built as a fork of HELM.** Everything below this section is the upstream HELM README, kept intact; this section is the only change to `main`, which otherwise mirrors upstream so the fork stays mergeable.

What is here:

- **Methodology** (frozen v1.2): `paybench/methodology/methodology.md`. Settlement-finality measurement across rails, with per-rail finality defined at each rail's own canonical reliance level, Bradley-Terry maximum-likelihood scoring, pass@k, and Wilson lower-bound confidence intervals.
- **Pre-registrations**, anchored before any measurement: settlement finality, OSF DOI [10.17605/OSF.IO/XGFUJ](https://doi.org/10.17605/OSF.IO/XGFUJ), signed tag `paybench-prereg-v1.2`; authorization-primitive latency, OSF DOI [10.17605/OSF.IO/UFQG5](https://doi.org/10.17605/OSF.IO/UFQG5), signed tag `paybench-rapl-prereg-v1`. The anchors prove precedence, integrity, and signer identity; they claim no authorship of the underlying cryptographic primitives.
- **Harness and calibrated fixtures**: the unified Python harness and content-addressed mock fixtures with provenance, reproducible bit-for-bit in CI.

What is published about named rails: the **authorization-primitive latency (DIM-02) findings for six named rails**, published as a measurement on the companion oracle site at [oracle.agentic-paybench.dev/results/](https://oracle.agentic-paybench.dev/results/). There is one canonical copy and it lives there; this repository points at it and holds no results file of its own. Rails on that page are listed alphabetically by rail name; that ordering is fixed and carries no performance meaning. The figures are a measurement and not a recommendation: no rail is endorsed, no ordering implies a best buy, and no rail is being suggested for use.

What is deliberately not here: **no rail-by-rail settlement-finality results and no ranking of named rails.** Settlement-finality results are withheld by choice, not omission, and no merit ordering of named rails is published anywhere. Nothing in this repository or on that page recommends a rail or routes a payment.

The published measurement follows the frozen and anchored DIM-02 pre-registration (OSF DOI 10.17605/OSF.IO/UFQG5; Bitcoin block 955977; Rekor 2012836917). The frozen text of that record includes a finding ordering three rails on this dimension. That statement is part of the frozen methodology and was fixed before the published results page existed. The published results page does not assert any ordering: the table is listed alphabetically, the order carries no performance meaning, and nothing there is a recommendation to use any rail.

Branches: you are on `main`, the upstream mirror plus this banner. The methodology, harness and fixtures live on `paybench/poc` (the working branch; the paths above are relative to it). `paybench/dim1-frozen` and `paybench/dim2-frozen` are append-only frozen lines carrying the anchored pre-registrations.

Companion repository: [oracle](https://github.com/agentic-paybench/oracle), the capability oracle (schema, ingestion, methodology, static read surface), live at [oracle.agentic-paybench.dev](https://oracle.agentic-paybench.dev/).

Research context and contact: [everydayai.link](https://everydayai.link/), mblake@everydayai.link. Corrections to anything published here are welcome by email.

---
# Holistic Evaluation of Language Models (HELM)

[comment]: <> (When using the img tag, which allows us to specify size, src has to be a URL.)
<img src="https://github.com/stanford-crfm/helm/raw/v0.5.4/helm-frontend/src/assets/helm-logo.png" alt="HELM logo"  width="480"/>

<a href="https://github.com/stanford-crfm/helm">
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/stanford-crfm/helm">
</a>
<a href="https://github.com/stanford-crfm/helm/graphs/contributors">
    <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/stanford-crfm/helm">
</a>
<a href="https://github.com/stanford-crfm/helm/actions/workflows/test.yml?query=branch%3Amain">
    <img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/stanford-crfm/helm/test-python.yml">
</a>
<a href="https://crfm-helm.readthedocs.io/en/latest/">
    <img alt="Documentation Status" src="https://readthedocs.org/projects/helm/badge/?version=latest">
</a>
<a href="https://github.com/stanford-crfm/helm/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/stanford-crfm/helm?color=blue" />
</a>
<a href="https://pypi.org/project/crfm-helm/">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/crfm-helm?color=blue" />
</a>

> HELM will enter maintenance mode on June 1, 2026. After this date, [Maintenace Mode Policy](https://crfm-helm.readthedocs.io/en/latest/maintenance_mode/) will take effect.

**Holistic Evaluation of Language Models (HELM)** is an open source Python framework created by the [Center for Research on Foundation Models (CRFM) at Stanford](https://crfm.stanford.edu/) for holistic, reproducible and transparent evaluation of foundation models, including large language models (LLMs) and multimodal models. This framework includes the following features:

- Datasets and benchmarks in a standardized format (e.g. MMLU-Pro, GPQA, IFEval, WildBench)
- Models from various providers accessible through a unified interface (e.g. OpenAI models, Anthropic Claude, Google Gemini)
- Metrics for measuring various aspects beyond accuracy (e.g. efficiency, bias, toxicity)
- Web UI for inspecting individual prompts and responses
- Web leaderboard for comparing results across models and benchmarks

## Documentation

Please refer to [the documentation on Read the Docs](https://crfm-helm.readthedocs.io/) for instructions on how to install and run HELM.

## Quick Start

<!--quick-start-begin-->

Install the package from PyPI:

```sh
pip install crfm-helm
```

Run the following in your shell:

```sh
# Run benchmark
helm-run --run-entries mmlu:subject=philosophy,model=openai/gpt2 --suite my-suite --max-eval-instances 10

# Summarize benchmark results
helm-summarize --suite my-suite

# Start a web server to display benchmark results
helm-server --suite my-suite
```

Then go to http://localhost:8000/ in your browser.

<!--quick-start-end-->

## Leaderboards

We maintain offical leaderboards with results from evaluating recent models on notable benchmarks using this framework. Our current flagship leaderboards are:

- [HELM Capabilities](https://crfm.stanford.edu/helm/capabilities/latest/)
- [HELM Safety](https://crfm.stanford.edu/helm/safety/latest/)
- [Holistic Evaluation of Vision-Language Models (VHELM)](https://crfm.stanford.edu/helm/vhelm/latest/)

We also maintain leaderboards for a diverse range of domains (e.g. medicine, finance) and aspects (e.g. multi-linguality, world knowledge, regulation compliance). Refer to the [HELM website](https://crfm.stanford.edu/helm/) for a full list of leaderboards.

## Papers

The HELM framework was used in the following papers for evaluating models.

- **Holistic Evaluation of Language Models** - [paper](https://openreview.net/forum?id=iO4LZibEqW), [leaderboard](https://crfm.stanford.edu/helm/classic/latest/)
- **Holistic Evaluation of Vision-Language Models (VHELM)** - [paper](https://arxiv.org/abs/2410.07112), [leaderboard](https://crfm.stanford.edu/helm/vhelm/latest/), [documentation](https://crfm-helm.readthedocs.io/en/latest/vhelm/)
- **Holistic Evaluation of Text-To-Image Models (HEIM)** - [paper](https://arxiv.org/abs/2311.04287), [leaderboard](https://crfm.stanford.edu/helm/heim/latest/), [documentation](https://crfm-helm.readthedocs.io/en/latest/heim/)
- **Image2Struct: Benchmarking Structure Extraction for Vision-Language Models** - [paper](https://arxiv.org/abs/2410.22456)
- **Enterprise Benchmarks for Large Language Model Evaluation** - [paper](https://arxiv.org/abs/2410.12857), [documentation](https://crfm-helm.readthedocs.io/en/latest/enterprise_benchmark/)
- **The Mighty ToRR: A Benchmark for Table Reasoning and Robustness** - [paper](https://arxiv.org/abs/2502.19412), [leaderboard](https://crfm.stanford.edu/helm/torr/latest/)
- **Efficient Benchmarking of Language Models** - [paper](https://arxiv.org/abs/2308.11696), [documentation](https://crfm-helm.readthedocs.io/en/latest/efficient_benchmarking/)
- **Reliable and Efficient Amortized Model-based Evaluation** - [paper](https://arxiv.org/abs/2503.13335), [documentation](https://crfm-helm.readthedocs.io/en/latest/reeval/)
- **Holistic evaluation of large language models for medical tasks with MedHELM** - [paper](https://www.nature.com/articles/s41591-025-04151-2), [leaderboard](https://crfm.stanford.edu/helm/medhelm/latest/)
- **Holistic Evaluation of Audio-Language Models** - [paper](https://arxiv.org/abs/2508.21376), [leaderboard](https://crfm.stanford.edu/helm/audio/latest/)

The HELM framework can be used to reproduce the published model evaluation results from these papers. To get started, refer to the documentation links above for the corresponding paper, or the [main Reproducing Leaderboards documentation](https://crfm-helm.readthedocs.io/en/latest/reproducing_leaderboards/).

## Citation

If you use this software in your research, please cite the [Holistic Evaluation of Language Models paper](https://openreview.net/forum?id=iO4LZibEqW) as below.

```bibtex
@article{
liang2023holistic,
title={Holistic Evaluation of Language Models},
author={Percy Liang and Rishi Bommasani and Tony Lee and Dimitris Tsipras and Dilara Soylu and Michihiro Yasunaga and Yian Zhang and Deepak Narayanan and Yuhuai Wu and Ananya Kumar and Benjamin Newman and Binhang Yuan and Bobby Yan and Ce Zhang and Christian Alexander Cosgrove and Christopher D Manning and Christopher Re and Diana Acosta-Navas and Drew Arad Hudson and Eric Zelikman and Esin Durmus and Faisal Ladhak and Frieda Rong and Hongyu Ren and Huaxiu Yao and Jue WANG and Keshav Santhanam and Laurel Orr and Lucia Zheng and Mert Yuksekgonul and Mirac Suzgun and Nathan Kim and Neel Guha and Niladri S. Chatterji and Omar Khattab and Peter Henderson and Qian Huang and Ryan Andrew Chi and Sang Michael Xie and Shibani Santurkar and Surya Ganguli and Tatsunori Hashimoto and Thomas Icard and Tianyi Zhang and Vishrav Chaudhary and William Wang and Xuechen Li and Yifan Mai and Yuhui Zhang and Yuta Koreeda},
journal={Transactions on Machine Learning Research},
issn={2835-8856},
year={2023},
url={https://openreview.net/forum?id=iO4LZibEqW},
note={Featured Certification, Expert Certification}
}
```
