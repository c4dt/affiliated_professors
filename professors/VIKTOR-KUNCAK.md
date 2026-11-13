[../PROFESSORS.md](../PROFESSORS.md)  

# Viktor Kunčak

<img src="https://people.epfl.ch/viktor.kuncak/photo" alt="Viktor Kunčak" width="150" align="right">

**Lab:** Lab for Automated Reasoning and Analysis (LARA)  
**EPFL profile:** [people.epfl.ch](https://people.epfl.ch/viktor.kuncak)  
**Web:** [lara.epfl.ch](https://lara.epfl.ch/w/)  
**Code:** [github.com/epfl-lara](https://github.com/epfl-lara)  
**ORCID:** [0000-0001-7044-9522](https://orcid.org/0000-0001-7044-9522)  
**OpenAlex:** [A5008699657](https://openalex.org/A5008699657)  

Viktor Kunčak leads EPFL's LARA lab, advancing formal verification (Stainless for Scala), AI-driven Lean 4 autoformalization (LeanFlow, LeanFlow Web), and neural theorem proving — now extending into learned GPU-accelerated proof evaluators and a browser-based Lean proof environment.

## Key research

- [LARA Lab Website](https://lara.epfl.ch/w/)
- [Stainless Verifier (415 ★)](https://github.com/epfl-lara/stainless)
- [LeanFlow — Workflow-Driven Lean Autoformalization](https://github.com/epfl-lara/LeanFlow)
- [LeanFlow Web — Browser Lean Proof Environment](https://github.com/epfl-lara/leanflow-web)
- [Learning Lean Feedback for Efficient Proof-Candidate Evaluation on GPUs (NeurIPS VeriCodeGen 2026)](https://arxiv.org/abs/2610.21881)
- [First-Class Refinement Types for Scala (OOPSLA 2026)](https://arxiv.org/abs/2605.08369)

## Changelog

### 2026-11-13

- **New paper: "Learning Lean Feedback for Efficient Proof-Candidate Evaluation on GPUs" (NeurIPS 2026 VeriCodeGen Workshop, Oct 2026):** LARA trained neural evaluators on 4.84M labelled Lean 4 programs to predict proof verdicts and compiler feedback on GPUs, achieving 87.8% accuracy and 4.2× throughput vs. a 64-worker Lean baseline. A hybrid GRPO reward system cutting training steps by ~31% is demonstrated, with open models and datasets on Hugging Face. This is a significant new research output in AI for formal mathematics.
- **New repo: `leanflow-web` (October–November 2026):** A self-hosted browser workspace for writing, exploring, and improving Lean 4 proofs, with live proof feedback, Git integration, and the Lemex AI assistant. EPFL early access is live at [leanflow.epfl.ch](https://leanflow.epfl.ch/). Actively developed (last push Nov 13, 2026).
- **New repo: `learning-lean-feedback`** (companion code to the NeurIPS paper above); released October 2026.
- **New repo: `lisa-checker`** — a Lean-based checker for LISA proofs, recently active.
- **Stainless v0.10.3 released (Oct 16, 2026):** Includes Scala compiler and Inox updates, ghost-code handling improvements, and tutorial fixes. Stars now at 415 (up from 404).
- **Inox now at 102 ★** (up from 97); LISA at 71 ★.
- **"First-Class Refinement Types for Scala" confirmed published at OOPSLA 2026** (DOI 10.1145/3839541); presented at Scala Days 2026 in Berlin by Matt Bovel (Oct 13, 2026).
- **New preprint: "Orthologic for SAT Solving"** (May 2026, arXiv:2605.16421) — connects LARA's orthologic framework to SAT solving.
- **New preprint: "Are Dependent Types in Set Theory Feasible?"** (March 2026, arXiv:2603.12827) — foundational work on dependent types in set-theory-based proof systems.
- **Simon Guilloud PhD thesis "Interactive and Automated Reasoning with Orthologic"** deposited (EPFL 2026).
- Lab website updated to highlight LARA's dual focus on AI for mathematics and verified software, with new Hugging Face org ([EPFL-LARA](https://huggingface.co/EPFL-LARA)) prominent.

### 2026-09-09

- **New repo: LeanFaith (August–September 2026):** LARA launched *LeanFaith*, a calibrated learned metric that judges whether a candidate Lean 4 theorem statement faithfully expresses the same mathematical claim as a natural-language source — stricter than logical equivalence. Actively developed with 236 commits; uses a private fine-tuning dataset (`formalmathatepfl/sft_classic`) and a staged training plan (S0–S3). This is a distinct tool from LeanFlow, filling the evaluation/faithfulness gap in the autoformalization pipeline.
- **"First-Class Refinement Types in Scala" artifacts deposited (August 2026):** Multiple artifact versions uploaded to Zenodo (DOIs 10.5281/zenodo.21494568, .21737784, .21737492), indicating an associated paper accepted at a 2026 venue (likely ECOOP or PLDI); paper itself not yet indexed on ORCID.
- **Stainless now at 404 ★** (up from 401); Inox at 97 ★; both actively maintained with pushes as recently as September 8, 2026.
- **LeanFlow, AutoformalizedProjects, LeanProbe** all receiving continued pushes into September 2026 — the Lean 4 AI ecosystem is consolidating.
- No major new publications beyond those already recorded; routine activity otherwise.

### 2026-07-10

- **LeanFlow agent (July 2026):** LARA launched *LeanFlow* (rebranded from EPFLemma), an AI-driven agentic framework for autonomous Lean 4 theorem proving and mathematical formalization. The Python-based tool integrates LLM orchestration, a dedicated *LeanProbe* feedback server, and a companion *AutoformalizedProjects* repository hosting fully autonomous Lean formalizations of published math papers — reflecting a major new research direction at the intersection of formal verification and AI.
- **"Formal Autograding in a Classroom" published in ACM TOPLAS (July 2026):** Extended journal version of the classroom autograding work, using Stainless-based equivalence checking over 1700+ student submissions to 11 programming exercises — demonstrating formal verification in undergraduate CS education at scale.
- **"Formally Verified Linear-Time Invertible Lexing" accepted at CAV 2026:** Stainless-verified lexer with linear-time guarantees and invertibility property (preprint Oct 2025, artifact deposited June 2026).
- **"Orthologic Type Systems" preprint (July 2025):** New theoretical work connecting orthologic (a substructural logic LARA has been developing) with type systems.
- **"Convex and Reverse Convex Prequadratics Constraints" published in ACM TOCL (June 2026):** New decidable logic fragment for relations with cardinalities.
- **New course CS-643 "Formal Mathematics with Lean and AI":** Graduate course on Lean 4 proof assistant combining foundations, AI tools, and formalization projects — directly connected to LeanFlow research.
- **Stainless (401 ★) and Inox (96 ★) actively maintained**, with pushes as recently as July 2026; Bolts verified-examples library also active.
