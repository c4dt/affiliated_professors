[../PROFESSORS.md](../PROFESSORS.md)  

# Caglar Gulcehre

<img src="https://people.epfl.ch/caglar.gulcehre/photo" alt="Caglar Gulcehre" width="150" align="right">

**Lab:** Caglar Gulcehre Lab for AI Research (CLAIRE)  
**EPFL profile:** [people.epfl.ch](https://people.epfl.ch/caglar.gulcehre)  
**Web:** [epfl.ch](https://www.epfl.ch/labs/claire/)  
**ORCID:** [0009-0003-4124-1687](https://orcid.org/0009-0003-4124-1687)  
**OpenAlex:** [A5041145688](https://openalex.org/A5041145688)  

Caglar Gulcehre leads CLAIRE at EPFL, researching efficient deep learning spanning reinforcement learning, large language model training, sequence modeling architectures (RNNs/Transformers/SSMs/diffusion), AI safety/alignment, and system-2 reasoning.

## Key research

- [CLAIRE Lab Website](https://www.epfl.ch/labs/claire/)
- [Caglar Gulcehre Personal Website](https://www.caglar.ai)
- [RAT+: Train Dense, Infer Sparse (ICML 2026)](https://arxiv.org/abs/2602.18196)
- [Loopholing All the Way: Language Modeling with Pure Self-Conditioning (arXiv Oct 2026)](https://arxiv.org/abs/2610.30068)
- [Language Modeling with Hyperspherical Flows (TMLR Oct 2026)](https://arxiv.org/abs/2605.11125)
- [Google Scholar Profile](https://scholar.google.com/citations?user=7hwJ2ckAAAAJ&hl=en)

## Changelog

### 2026-11-27

- **RAT+ accepted at ICML 2026:** "RAT+: Train Dense, Infer Sparse — Recurrence Augmented Attention for Dilated Inference" (Xiuying Wei & Gulcehre) was accepted at ICML 2026. The paper extends the RAT architecture with full-sequence recurrence so a single densely pre-trained model can be flexibly switched at inference to dilated attention (up to 64× reduction in attention FLOPs and KV cache size), demonstrated at scales up to 7.6B parameters.
- **New arXiv preprint — LAW (Oct 2026):** "Loopholing All the Way: Language Modeling with Pure Self-Conditioning" presents the LAW model, a continuous generative LM that relies entirely on self-conditioning/loopholing across diffusion steps (no mask tokens, no discrete sampling). It outperforms prior diffusion LMs on Sudoku, Maze, and GSM8K, and approaches autoregressive models on OpenWebText at 64 NFE.
- **Language Modeling with Hyperspherical Flows published in TMLR (Oct 2026):** Paper tracking 37 citations, now formally published in *Transactions on Machine Learning Research*.
- **Benchmarking Non-Invasive Speech BCIs (Nov 2026):** A proceedings paper in *PMLR* extending the 2025 PNPL Competition work on the LibriBrain dataset — peripheral to core CLAIRE research.
- **Mikhail Terekhov completed EPFL PhD (2026):** Listed as past EPFL PhD student (co-director), thesis at http://dx.doi.org/10.5075/epfl-thesis-12434.
- **New preprints since last update (not previously tracked):**
  - "Diffuse AI Control on Fuzzy Tasks" (arXiv, Jun 2026) — AI safety/control extension.
  - "BlockGen: Flexible Blockwise Sequence Modeling with Hybrid Samplers" (arXiv, Jun 2026) — generative modeling preprint.
  - "Augmenting Attention with Exponentially Decaying Memory Improves Query-Aware KV Sparsity" (arXiv, May 2026).
  - "The Future of Facts: Tracing the Factual Generation-Verification Gap" (arXiv, May 2026).
  - "The Diffusion Duality, Chapter II: Ψ-Samplers" (ICLR 2026) — previously untracked.

### 2026-09-23

- **No materially new developments** since the 2026-07-22 profile update. Publication list, lab structure, PhD student roster, and course offerings remain unchanged.
- One previously untracked paper now visible in the feed: **"The 2025 PNPL Competition: Speech Detection and Phoneme Classification in the LibriBrain Dataset"** (arXiv, June 2025) — a peripheral competition/dataset paper, not a core CLAIRE research contribution.
- **"Partition Generative Modeling: Masked Modeling Without Masks"** (arXiv, May 2025) also appears in the feed but was not previously highlighted; this is a generative modeling preprint from a CLAIRE PhD student, representing routine lab activity.
- No new preprints, accepted papers, news posts, or significant events since last update.

### 2026-07-22

- **No major new developments** since last profile update (2026-07-10). Publication list and lab structure remain consistent.
- **New published article confirmed:** "Sequence Modeling Architectures: Foundations" appeared in *IEEE Signal Processing Magazine* (Vol. 43, No. 3, May 2026, pp. 115–129), co-authored with Sarnthein, Afzal, Pascanu, Orvieto, and Geiping. This is a survey/tutorial for the special issue on the Mathematics of Deep Learning, unifying RNNs, Transformers, and SSMs under a general linear sequence mixer framework.
- **New published article confirmed:** "Context-Aware Toxicity Detection in Game Chat: Domain-Adaptive Pretraining with Match Metadata under Limited Labels" appeared in *ACM Games Research and Practice* (July 2026) — a peripheral application paper on game chat moderation using RoBERTa with contextual domain-adaptive pretraining (C-DAP).
- No new preprints or research directions beyond what was already tracked.

### 2026-07-10

- **Initial profile created** — first scrape of CLAIRE lab and publications.
- **Apertus (ACL 2026):** Co-author on a major Swiss-wide collaborative paper releasing fully open, regulation-compliant LLMs (8B & 70B) trained on ~15T tokens across ~1800 languages, respecting robots.txt and using the Goldfish anti-memorization objective; published at ACL 2026 (San Diego).
- **RAT architecture (July 2025):** New preprint introducing a chunk-based sequence model bridging RNN efficiency with Transformer attention accuracy.
- **AI Safety / Control Tax (June 2025):** Preprint analyzing the performance cost of keeping AI systems under human control ("Control Tax"), alongside a companion paper on adaptive attacks that can subvert AI control protocols using trusted monitors.
- **Algorithm Discovery with LLMs (April 2025):** Preprint combining evolutionary search and RL for automated algorithm discovery.
- **Discrete diffusion (Oct 2025):** Preprint "Loopholing Discrete Diffusion" presenting a deterministic bypass of the diffusion sampling wall.
- **Upcoming lectures:** Gulcehre is scheduled to give three lectures on RL for foundation models at the 8th Advanced Course on Data Science & Machine Learning (Tuscany, Italy).
- **PhD course:** Teaching EE-628 "Training Large Language Models" at EPFL (PhD level).
