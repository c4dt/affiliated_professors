[../PROFESSORS.md](../PROFESSORS.md)  

# Martin Odersky

**Lab:** Programming Methods Laboratory (LAMP)  
**EPFL profile:** [people.epfl.ch](https://people.epfl.ch/martin.odersky)  
**Web:** [lamp.epfl.ch](https://lamp.epfl.ch/)  
**Code:** [github.com/lampepfl](https://github.com/lampepfl)  
**ORCID:** [0009-0005-3923-8993](https://orcid.org/0009-0005-3923-8993)  
**OpenAlex:** [A5085410724](https://openalex.org/A5085410724)  

Martin Odersky leads EPFL's LAMP group, designing the Scala programming language with a focus on advanced type systems including capture checking, capability classifiers, first-class refinement types, and safe concurrency for AI agent security.

## Key research

- [LAMP Lab website](https://lamp.epfl.ch/)
- [Martin Odersky's EPFL profile](https://people.epfl.ch/martin.odersky)
- [TACIT — Tracked Agent Capabilities In Types (GitHub)](https://github.com/lampepfl/tacit)
- [Classifying Capabilities — OOPSLA 2026 (artifact)](https://doi.org/10.1145/3839474)
- [First-Class Refinement Types in Scala (artifact, Aug 2026)](https://doi.org/10.5281/zenodo.21737492)
- [gears — async library for Scala 3 (GitHub)](https://github.com/lampepfl/gears)

## Changelog

### 2026-08-14

- **New paper — "Classifying Capabilities" (OOPSLA 2026)**: Extends Scala 3 capture checking with *capability classifiers* — a user-extensible, tree-structured hierarchy of tags with `.only`/`.except` projections on capture sets. Artifact published 2026-08-10 (Zenodo). This is a significant advance over the flat capture-set model.
- **New paper — "First-Class Refinement Types in Scala"**: Co-authored with Matthieu Bovel and Viktor Kunčak; artifact published 2026-08-01 on Zenodo (multiple versions). Adds first-class refinement types to Scala 3, integrating with the existing type system.
- **New course — "Agentic-Systems Security" (CS-620)**: Odersky is now teaching a graduate seminar at EPFL covering AI agent security research, directly complementing the TACIT/capybaraclaw research strand.
- **TACIT repo** now at 69 stars (up from 58 in July 2026); **gears** at 304 stars (up from 302).
- **scala3-benchmarks-data** is a new repo (Python, pushed 2026-08-14), supporting Scala 3 benchmarking infrastructure.
- No other materially new developments since the 2026-07-10 profile update.

### 2026-07-10

- **TACIT (Tracked Agent Capabilities In Types)**: New actively developed project applying Scala 3 capture checking to AI agent safety; the associated paper "Securing Agents With Tracked Capabilities" (CAIS 2026) won **Best Paper Award**. The repo has 58 stars and received active commits through late June 2026.
- **New publication — "Modular Substructural Constraints for Embedded DSLs"** (GPCE 2026, June 2026): presents a technique for expressing modular substructural constraints in embedded DSLs via Scala 3 type-level programming, illustrated with a Linear Datalog case study.
- **New publication — "What's in the Box: Ergonomic and Expressive Capture Tracking over Generic Data Structures"** (PACMPL, Oct 2025): advances Scala 3's capture-checking type system for generic data structures.
- **Language-integrated recursive queries** strand: two related papers appeared — "Language-Integrated Recursive Queries" (ECOOP 2026, preprint Apr 2025) and "Static Typing Meets Adaptive Optimization: A Unified Approach to Recursive Queries" (DBPL 2025, June 2025), bridging PL type systems with database query optimization.
- Active GitHub repos: **scala3-benchmarks** (updated Jul 2026), **steps** (LAMP library collection, Jul 2026), **gears** (async Scala 3 library, 302 stars, Jun 2026), **capybaraclaw** (trustworthy secure agent, Jun 2026).
- Scala 3 / capture-checking remains the central research and engineering thread, with multiple 2024–2026 papers formalizing and extending the system.
