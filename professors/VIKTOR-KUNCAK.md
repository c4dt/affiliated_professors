[../PROFESSORS.md](../PROFESSORS.md)  

# Viktor Kunčak

**Lab:** Lab for Automated Reasoning and Analysis (LARA)  
**EPFL profile:** [people.epfl.ch](https://people.epfl.ch/viktor.kuncak)  
**Web:** [lara.epfl.ch](https://lara.epfl.ch/w/)  
**Code:** [github.com/epfl-lara](https://github.com/epfl-lara)  
**ORCID:** [0000-0001-7044-9522](https://orcid.org/0000-0001-7044-9522)  
**OpenAlex:** [A5008699657](https://openalex.org/A5008699657)  

Viktor Kunčak leads EPFL's LARA lab, developing automated reasoning, formal verification, and program synthesis tools — notably the Stainless verifier for Scala — and is now building an expanding AI-driven Lean 4 ecosystem including LeanFlow (proof generation), LeanFaith (autoformalization faithfulness metric), and LeanProbe (fast feedback server).

## Key research

- [LARA Lab Website](https://lara.epfl.ch/w/)
- [Stainless Verifier](https://stainless.epfl.ch/)
- [Stainless GitHub (404 ★)](https://github.com/epfl-lara/stainless)
- [LeanFlow — AI agent for Lean 4 proof generation](https://github.com/epfl-lara/LeanFlow)
- [LeanFaith — calibrated faithfulness metric for autoformalization](https://github.com/epfl-lara/LeanFaith)
- [First-Class Refinement Types in Scala (ECOOP 2026 artifact)](https://doi.org/10.5281/zenodo.21494568)

## Changelog

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
