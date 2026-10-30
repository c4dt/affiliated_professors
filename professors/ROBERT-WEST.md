[../PROFESSORS.md](../PROFESSORS.md)  

# Robert West

<img src="https://people.epfl.ch/robert.west/photo" alt="Robert West" width="150" align="right">

**Lab:** Data Science Laboratory (DLAB)  
**EPFL profile:** [people.epfl.ch](https://people.epfl.ch/robert.west)  
**Web:** [dlab.epfl.ch](https://dlab.epfl.ch/)  
**Code:** [github.com/epfl-dlab](https://github.com/epfl-dlab)  
**ORCID:** [0000-0001-6398-0921](https://orcid.org/0000-0001-6398-0921)  
**OpenAlex:** [A5059645286](https://openalex.org/A5059645286)  

Robert West leads EPFL's Data Science & AI Lab (dlab), researching AI safety, NLP, and computational social science, with active projects on LLM alignment (Synthetic Persona Pretraining), RL-based misalignment/reward-hacking detection, and inference-time adaptive tokenization (zip2zip).

## Key research

- [DLAB — Data Science & AI Lab](https://dlab.epfl.ch/)
- [Robert West — EPFL Profile](https://people.epfl.ch/robert.west)
- [SPP: Synthetic Persona Pretraining (GitHub)](https://github.com/epfl-dlab/spp)
- [1PP Misalignment RL Dashboard (GitHub)](https://github.com/epfl-dlab/1pp-misalign-rl-dashboard)
- [zip2zip: Inference-Time Adaptive Vocabularies (GitHub)](https://github.com/epfl-dlab/zip2zip)
- [DLAB GitHub Organisation](https://github.com/epfl-dlab)

## Changelog

### 2026-10-30

- **NEW PROJECT — 1PP Misalignment RL** (`1pp-misalign-rl-dashboard`, actively pushed through Oct 28, 2026): A significant new AI safety research project studying reward-hacking and RL-induced misalignment in LLMs. The project tests five 1.7B pretraining variants (raw, asst, ua, and annealed variants) across two final RL environments: `record_request` (reward incentivises leaking private data fields) and `harmful_agree_v2` (hidden bonus for agreeing with dangerous false claims). Includes a public results dashboard. This is a direct extension of the SPP/alignment-from-pretraining research direction and is being actively developed.
- **zip2zip reaches 20 stars** (up from 19 at last update); `zip2zip-plus-plus` repo (new since last profile) is active with recent pushes through October 2026, and `zip2zip-plus-plus-hyperenc-probe` (published September 2026) provides reproduction code for studying the learned geometry of LZW hyper-tokens.
- **model-raising-data** continues to receive commits (last push Oct 26, 2026); project direction remains undisclosed.
- ORCID publication feed continues to return unrelated papers (tobacco, behavioural science, mental health); not attributable to Robert West (EPFL).
- No other materially new papers or announcements identified since the August 2026 update.

### 2026-08-27

- **NEW PAPER — Synthetic Persona Pretraining (SPP)** (arXiv:2608.13482, August 2026): Major new preprint introducing SPP, which installs an aligned assistant persona from token zero of LLM pretraining rather than relying solely on post-training alignment. Models (3B and 1.7B, base and instruct, five variants) and datasets released on Hugging Face under [dlab-spp](https://huggingface.co/dlab-spp). Full code in three submodule repos (`spp-data`, `spp-training`, `spp-evals`), actively updated August 2026. This is the lab's most significant new paper since the last profile update.
- **nelight** repo (Python, pushed August 2026): New repository with no public description yet — likely an emerging project.
- **model-raising-data** (Python, pushed August 2026): Still active with recent commits; project direction remains undisclosed.
- **zip2zip** continues to be actively maintained (last push August 2026, 19 stars); no new paper but growing community interest.
- ORCID publication feed continues to return unrelated papers (tobacco, mental health, etc.) — not attributable to Robert West (EPFL).

### 2026-07-10

- **Initial profile created.**
- **zip2zip** (arXiv 2506.01084, June 2025): Active new project introducing inference-time adaptive token vocabularies for LLMs via LZW-based token compression; pretrained models released on Hugging Face (Phi-3.5-mini, Phi-3-medium); repo actively maintained with recent commits in June–July 2026.
- **zip2zip-compression** (Rust, pushed July 2026): Companion low-level compression repo, very recently updated.
- **model-raising-data / model-raising-chat** (2026): Two new repositories related to an apparent "model raising" research direction (no public description yet), suggesting an emerging project.
- **pretraining_persona** (May 2026): Repo titled "Tracing Persona Vectors Through LLM Pretraining," investigating how personality/persona representations emerge during LLM training.
- **cacm-ai-risk** (Feb 2026): Repo tied to West's role as AI Column Head at *Communications of the ACM*, likely accompanying an article on AI risk.
- Recent best/outstanding paper awards at NAACL 2025, ACL 2024, CSCW 2021 & 2025, ICWSM 2019–2025; sabbatical at Microsoft Research Redmond (2024/2025) working on agentic AI.
- Note: The ORCID publication feed returned unrelated papers (tobacco, mental health, etc.) and does not appear to be correctly linked to Robert West (EPFL); no relevant new publications were identified via this source.
