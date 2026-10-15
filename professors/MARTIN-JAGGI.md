[../PROFESSORS.md](../PROFESSORS.md)  

# Martin Jaggi

<img src="https://people.epfl.ch/martin.jaggi/photo" alt="Martin Jaggi" width="150" align="right">

**Lab:** Machine Learning and Optimization Laboratory (MLO)  
**EPFL profile:** [people.epfl.ch](https://people.epfl.ch/martin.jaggi)  
**Web:** [mlo.epfl.ch](https://mlo.epfl.ch/)  
**Code:** [github.com/epfml](https://github.com/epfml)  
**ORCID:** [0000-0003-1579-5558](https://orcid.org/0000-0003-1579-5558)  
**OpenAlex:** [A5073756389](https://openalex.org/A5073756389)  

Martin Jaggi leads EPFL's MLO lab, focusing on scalable ML optimization, federated/distributed learning, and open LLM training — including the Apertus multilingual LLM family, hallucination benchmarking, and LLM pretraining data selection.

## Key research

- [MLO Lab Website](https://mlo.epfl.ch/)
- [epfml GitHub Organization](https://github.com/epfml)
- [Apertus — Fully Open LLM (Swiss AI)](https://www.swiss-ai.org/apertus)
- [HalluHard: Hard Multi-Turn Hallucination Benchmark](https://github.com/epfml/halluhard)
- [Apertus at ACL 2026 (cited 16×)](https://doi.org/10.18653/v1/2026.acl-long.2172)
- [Benchmarking Optimizers for LLM Pretraining (arXiv)](https://arxiv.org/abs/2509.01440)

## Changelog

### 2026-10-15

- **Apertus at ACL 2026 (16 citations):** The Apertus paper "Democratizing Open and Compliant LLMs for Global Language Environments" was published at ACL 2026 and has already accumulated 16 citations — the most-cited recent output from the lab.
- **Apertus family expansion (May 2026):** New arXiv paper on "Apertus LLM Family Expansion via Distillation and Quantization" (arXiv:2605.29128), extending the model family with smaller/quantized variants.
- **Apertus engineering report (Apr 2026):** "An Engineering Journey Training Large Language Models at Scale on Alps: The Apertus Experience" (arXiv:2604.12973) details the large-scale training infrastructure on the Alps supercomputer.
- **MXSens (Jul 2026):** New preprint on sensitivity-aware mixed-precision quantization for efficient LLM inference (arXiv:2607.17733).
- **Use of LLMs in peer review — ICML 2026 study (Sep 2026):** MLO co-authored a randomized experiment and survey on LLM use in peer review at ICML 2026 (arXiv:2609.19420) — a notably broad-interest methodological contribution.
- **New optimization preprints (Oct 2026):** Three new arXiv preprints posted Oct 9: "Randomized Momentum Transport with Cheap Predictors," "Partially Informed Stochastic Optimization via Zeroth-Order Residual Tracking," and "Geometry-Aware Multi-Objective Optimization: Norm-Constrained Oracles with Entropic Weight Updates."
- **Multilingual data selection preprints (Oct 2026):** "Adapting English Quality Classifiers for Multilingual LLM Pretraining Data Selection" (arXiv:2610.11585) and "OptiSelect: How does the Optimizer Shape Data Curriculum?" continue the lab's multilingual pretraining data thread.
- **Self-Repulsive Sampling for Diffusion LMs (Sep 2026):** New preprint extending the lab's LLM generation research to diffusion-based language models.
- **Local MixVR (May 2026):** New preprint on breaking communication-sample dependence in distributed learning (arXiv:2606.01128).
- **Looped Transformers stabilization (Jun 2026):** "Stabilizing Extrapolation in Looped Transformers via Learned Stochastic Stopping" (arXiv:2606.29983).
- **Weight vector decoupling (Jun 2026):** "Improving Neural Network Training by Decoupling the Magnitude and Direction of Weight Vectors" (arXiv:2606.25971).
- **HalluHard (previously noted):** Now at 36 stars (up from 34); last push Sep 2026.
- **DISCO repo:** Now at 190 stars (up from 186); last push Oct 2026 — still actively maintained.
- **ML_course:** Updated to Fall 2026 edition, now at 2088 stars.
- **Vinko Sabolcec** appears as a new PhD student not listed in prior profiles.
- No new lab news items on the MLO website beyond what was already captured in the 2026-08-13 changelog.

### 2026-08-13

- **HalluHard benchmark (2026, actively developed):** MLO released [HalluHard](https://github.com/epfml/halluhard), a hard multi-turn hallucination benchmark covering research questions, legal cases, medical guidelines, and coding tasks. The repo is actively maintained (last push Aug 2026), has 34 stars, and already evaluates frontier models including GPT-5, Claude 4.x, Gemini, Grok-4, Kimi-K2, and GLM-5. A companion paper is on arXiv (arXiv:2602.01031). A live leaderboard is at [halluhard.com](https://halluhard.com/).
- **looped-moe repo (Jun 2026):** New GitHub repo for "Tying the Loop — Tied Expert Layers in Mixture-of-Experts Language Models", extending MoE LLM research.
- **grad-norm-smooth (ICLR 2026):** Official implementation released for "Gradient-Normalized Smoothness for Optimization with Approximate Hessians" (accepted at ICLR 2026).
- **New preprints since last update:** "Beyond URLs: Metadata Diversity and Position for Efficient LLM Pretraining" (Nov 2025); "NeuralGrok: Accelerate Grokking by Neural Gradient Transformation" (Apr 2025); "Leveraging the true depth of LLMs" (Feb 2025); "Mitigating Unintended Memorization with LoRA in Federated Learning for LLMs" (Feb 2025).
- **PhD students updated:** Simla Burcu Harma (2026) and Vinitra Swamy (2025) listed as completed co-directed PhDs; Atli Kosson and Matteo Pagliardini (2026) expected to complete soon.
- No major new lab news items on the MLO website beyond what was already captured in the previous changelog.

### 2026-07-10

- **Apertus LLM released (Sep 2025):** MLO released Apertus 8B & 70B, a fully open-data/open-weights LLM with >1000-language support and EU AI Act compliance; surpassed 1M downloads on HuggingFace by Nov 2025 and was mentioned in the UN Security Council.
- **DISCO platform paper (Nov 2025):** Published arXiv paper for DISCO, a browser-based, no-code, privacy-preserving federated/decentralized ML platform supporting LLM fine-tuning; actively maintained TypeScript repo with 186 stars.
- **Best paper award (Oct 2025):** Multilingual training data quality selection work won Best Paper at the CoLM Workshop on Multilingual Data Quality Signals.
- **FineWeb2 dataset (Jun 2025 / Dec 2024):** Released in collaboration with HuggingFace; leading multilingual pre-training dataset covering 2000+ languages; full pipeline paper on arXiv.
- **LLM Optimizer Benchmark (Sep 2025):** New benchmark paper and codebase for comparing optimizers in LLM pretraining; to be presented at EurIPS Dec 2025.
- **Papers at NeurIPS/CoLM 2025:** Multiple papers including GRAPE (data mixture), FP8 LLM training, multilingual data selection, and FineWeb2.
- **Papers at ICLR/AIStats 2025:** AdEMAMix optimizer, CoTFormer, sparsity-quantization interplay (spotlight), and others.
- **ICML 2025:** Paper on on-device collaborative LM via mixture of generalists and specialists.
- **New arXiv preprints (Oct–Nov 2025):** Weight decay vs. muP for LR transfer; stochastic difference-of-convex optimization with momentum; stochastic optimization with random search; split-client second-order optimization; metadata diversity for LLM pretraining.
- **TiMoE (Aug 2025):** Time-aware Mixture-of-Experts language modeling framework released on GitHub.
- **ELLIS PhD Award (Dec 2024):** Former PhD student Anastasiia Koloskova won the European AI PhD Award for her thesis on decentralized/collaborative ML optimization.
- **Grad student Atli Kosson & Matteo Pagliardini** listed as completing theses (2026 expected).
