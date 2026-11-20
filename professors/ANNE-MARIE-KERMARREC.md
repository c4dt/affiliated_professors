[../PROFESSORS.md](../PROFESSORS.md)  

# Anne-Marie Kermarrec

<img src="https://people.epfl.ch/anne-marie.kermarrec/photo" alt="Anne-Marie Kermarrec" width="150" align="right">

**Lab:** Scalable Computing Systems Laboratory (SaCS)  
**EPFL profile:** [people.epfl.ch](https://people.epfl.ch/anne-marie.kermarrec)  
**Web:** [epfl.ch](https://www.epfl.ch/labs/sacs/)  
**Code:** [github.com/sacs-epfl](https://github.com/sacs-epfl)  
**ORCID:** [0000-0001-8187-724X](https://orcid.org/0000-0001-8187-724X)  
**OpenAlex:** [A5031849486](https://openalex.org/A5031849486)  

Anne-Marie Kermarrec leads the SACS lab at EPFL, researching large-scale distributed systems with a focus on decentralized/federated machine learning, scalable LLM and MoE inference, agentic AI, privacy-preserving vector search, and now fully decentralized RAG.

## Key research

- [SACS Lab Website](https://www.epfl.ch/labs/sacs/)
- [EPFL People Profile](https://people.epfl.ch/anne-marie.kermarrec)
- [GitHub: sacs-epfl](https://github.com/sacs-epfl)
- [ZeroRAG – Decentralized RAG (arXiv:2611.07928)](https://arxiv.org/abs/2611.07928)
- [CESAR – Communication-Efficient Secure Aggregation in Decentralized Learning](https://github.com/sacs-epfl/cesar)
- [RAGRoute – Efficient Federated Search for RAG](https://github.com/sacs-epfl/ragroute)

## Changelog

### 2026-11-20

- **New paper: ZeroRAG** (arXiv:2611.07928, Nov 2026) — *"Adaptive Semantic Peer Routing for Decentralized Retrieval-Augmented Generation"*. Introduces a fully decentralized routing layer for document retrieval in RAG that works without global data structures or centralized orchestration; documents stay with their owners and the network self-organises via a best-first semantic walk. Evaluated at up to 100,000 peers, it approaches centralized recall. This is a significant extension of the RAGRoute line of work.
- **New paper: "The End of Consensus Research?"** (arXiv:2610.30114, Oct 2026) — a position/opinion paper questioning the future of classical consensus research; already has 1 citation.
- **New paper: AgentWeave** (arXiv:2610.14804, Oct 2026) — *"Efficient Distributed Agent Serving via Flow Decomposition"*; continues the lab's agentic AI thrust.
- **New paper: "Robust Decentralized Fairness Auditing"** (arXiv:2610.10199, Oct 2026) — extends the ML auditing / decentralized fairness theme.
- **New paper: "Backdoor Mitigation in Decentralized LLM Fine-Tuning"** (arXiv:2609.37367, Sep 2026) — addresses backdoor attacks specifically in decentralised LLM fine-tuning settings.
- **New repos (GitHub activity since last profile):**
  - `Argus` (Python, pushed Oct 2026) — no public description; likely related to auditing/monitoring work.
  - `peerswap` (Lean, pushed Oct 2026) — formally verified peer-swap protocol; notable use of Lean proof assistant.
  - `SAFHIRE` (Julia, pushed Oct 2026) — no public description yet.
- **Third PhD completion (2026):** Diana Andreea Petrescu defended (doi:10.5075/epfl-thesis-11716), now listed among past students.
- **`decentralized-learning-simulator`** continues to be the most recently active repo (pushed Nov 2026), reflecting ongoing decentralised ML experiments.
- **New PhD student listed:** Ramya Narasimha Prabhu (newly appearing in current student list).
- No new institutional role changes or awards beyond those already recorded.

### 2026-09-16

- **New repo: `secure-vector-search`** (Rust, pushed August 2026) — code for the new paper *"A Unified Benchmark for Privacy-preserving Vector Search"* (arXiv:2608.01192, Aug 2026). The repo implements and benchmarks five privacy-preserving vector similarity search backends (Plaintext, SAP/DCPE, EMVP, Tiptoe, Braverman–Newman), representing a significant new research direction combining secure computation with vector search/RAG infrastructure.
- **New repo: `fl-freeriding`** (pushed August 2026) — suggests active work on free-rider detection in federated learning; no public description yet.
- **New repo: `cesar`** (Python, pushed July 2026) — code for *"Communication-Efficient Secure Aggregation in Decentralized Learning"*; extends privacy-preserving decentralized ML work.
- **Second PhD completion:** Rishi Sharma defended his PhD in 2026 (thesis published, doi:10.5075/epfl-thesis-11369), joining Akash Dhasade (2026) as recently completed students.
- **Robust ML Auditing paper** (arXiv May 2026): *"Robust ML Auditing using Prior Knowledge"* — new preprint not in prior profile.
- **Robust Fingerprinting of Graphs with Fing** — published at SRDS 2025 (September 2025), not previously recorded.
- No new awards or institutional role changes since the last update.

### 2026-07-14

- **New publications (2026):** Several new papers have appeared since the last profile:
  - *HarMoEny: Efficient Inference of MoE Models* — published at IPDPS 2026 (May 2026); extends prior MoE inference work to multi-GPU settings.
  - *The Evaluation Game: Beyond Static LLM Benchmarking* — arXiv preprint (May 2026), questioning static benchmarking paradigms for LLMs.
  - *Orbit: Efficient Agentic Inference using Priority Scheduling* — published at a workshop/venue (April 2026); introduces priority scheduling for agentic inference pipelines.
  - *RIVA: Leveraging LLM Agents for Reliable Configuration Drift Detection* — published (April 2026); applies LLM agents to system reliability.
  - *The Cost of Expertise: Understanding MoE Decode Performance* — published (April 2026).
  - *Optimizing Agentic Workflows using Meta-tools* — arXiv (January 2026).
  - *Position: Collaborative Agentic AI Needs Interoperability Across Ecosystems* — arXiv (May 2025, newly indexed).
- **New research direction — Agentic AI:** A clear new thrust toward agentic AI systems (Orbit, RIVA, web-of-agents repo, meta-tools paper) has emerged since the last profile, complementing the existing federated/decentralized ML and RAG themes.
- **New repo activity:** `catapult-db-experiments` was pushed as recently as June 2026; `web-of-agents` updated May 2026 — both suggest active ongoing experiments.
- **PhD:** Akash Balasaheb Dhasade completed his PhD in 2026 (thesis published).
- No major new awards or institutional role changes beyond what was already recorded.

### 2026-07-10

- **Initial profile created** (no prior profile existed).
- **Awards (2025):** Received the ACM EuroSys Lifetime Achievement Award, the Jean-Claude Laprie Test-of-Time Award (DSN 2025), and a Best Paper Award at the Symposium on Reliable and Distributed Systems.
- **Elected ELLIS Fellow (2024)** and **Elected Member of the French Academy of Science (2024)**.
- **ICLR 2026 papers:** Two papers accepted — *FlexMerge* (flexible model merging, accuracy-size trade-off) and *Robust Federated Inference*; code released on GitHub.
- **RAGRoute (2026):** Active repo for "Efficient Federated Search for Retrieval-Augmented Generation using Lightweight Routing" — intelligent routing across federated data sources for RAG pipelines.
- **Other active repos (2025–2026):** `catapult-db-experiments` (vector DB experiments), `web-of-agents`, `HarMoEny` (MoE inference), `proximity` (Rust-based approximate nearest neighbor search), `decentralized-learning-simulator`, and several EuroMLSys '25 papers (Plexus, CPFL, cohort-parallel federated learning).
- **Also serves as EPFL Associate Vice-President for Doctoral and Lifelong Education** and President of CDOCT.
