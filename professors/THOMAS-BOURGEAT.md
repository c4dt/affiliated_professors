[../PROFESSORS.md](../PROFESSORS.md)  

# Thomas Bourgeat

<img src="https://people.epfl.ch/thomas.bourgeat/photo" alt="Thomas Bourgeat" width="150" align="right">

**Lab:** Verification and Computer Architecture Lab (VCA)  
**EPFL profile:** [people.epfl.ch](https://people.epfl.ch/thomas.bourgeat)  
**Web:** [vca.epfl.ch](https://vca.epfl.ch/)  
**ORCID:** [0000-0002-8468-8409](https://orcid.org/0000-0002-8468-8409)  
**OpenAlex:** [A5031573662](https://openalex.org/A5031573662)  

Thomas Bourgeat leads the VCA lab at EPFL, researching formal verification of hardware (processors, dataflow circuits, cache coherence protocols), hardware–software interface specifications, and security verification at the RTL level.

## Key research

- [VCA Lab Website](https://vca.epfl.ch/)
- [EPFL People Page](https://people.epfl.ch/thomas.bourgeat)
- [PLDI '25 – Making Concurrent Hardware Verification Sequential](https://doi.org/10.1145/3729331)
- [ASPLOS '26 – Graphiti: Formally Verified Out-of-Order Execution in Dataflow Circuits](https://doi.org/10.1145/3779212.3790166)
- [ASPLOS '27 – Flashpoint: Privileged-Software Isolation on RISC-V for Dynamic Root of Trust](https://doi.org/10.1145/3845814.3850073)
- [OOPSLA '26 – HyperTest (A Language Approach to Fine-Grained Microarchitectural Observation)](https://doi.org/10.1145/3839486)

## Changelog

### 2026-11-10

### 2026-11-XX

- **ASPLOS '27 – Flashpoint:** New paper (Alexandre Pinazza et al., with Bourgeat) on privileged-software isolation on RISC-V for dynamic root of trust. Extends the open-source XiangShan processor with a minimal ISA extension, uses Sail formal specification + Kani model checker to verify isolation, and demonstrates end-to-end dynamic root of trust with a TPM emulator. Artifact released on Zenodo (doi: 10.5281/zenodo.22688439). This is a genuinely new venue/paper not in the previous profile.
- **OOPSLA '26 – HyperTest (full paper):** The *HyperTest* paper is now confirmed as *"A Language Approach to Fine-Grained Microarchitectural Observation"* (Guokai Chen, Sergi Soler Arrufat, Clément Pit-Claudel, Thomas Bourgeat), published in PACMPL OOPSLA2 2026. It introduces a DSL + SMT-based framework (HT) for constructing and observing microarchitectural tests on XiangShan RISC-V; covers performance analysis, side-channel attack reproduction, and branch predictor characterisation. Previously only the artifact was noted; full title/DOI now confirmed.
- **New preprints (Sep 2026):** Two new arXiv preprints attributed to the lab appeared: *"Efficient Hardware Information-Flow Tracking for Pre-Silicon Security Testing"* (arXiv:2609.06791) and *"AI as a Compiler: Compiling Triton kernels without the Triton compiler"* (arXiv:2609.36800). The first is directly in the lab's security verification theme; the second is more peripheral.
- **PLOS '26 workshop paper:** *"All Your Assembly Belongs to Rust: Automated Lifting for Uniform Testing and Verification"* (Castes, Debaussart, Bourgeat) — automated lifting of assembly to Rust for uniform testing/verification. New venue not in prior profile.
- **PhD student count increased:** Now 9 PhD students listed (Martina Camaioni, Guokai Chen, Gurvan Debaussart, Neelu Kalani, Jiawei Lin, Jiacheng Ma, Alexandre Pinazza, Mohammadarman Soleimani, Tz-Ching Yu), up from 7 previously noted.

### 2026-09-04

- **OOPSLA '26 – HyperTest:** A new paper (Guokai Chen, Sergi Soler, Clément Pit-Claudel, Thomas Bourgeat) with a full artifact released on Zenodo (v1, Nov 30 2026). HyperTest is a framework for microarchitectural testing on the XiangShan RISC-V processor, validating performance bugs, side-channel attacks (Flush+Reload, Prime+Probe, Spectre, Phantom, Load Predictor), and mitigations at the RTL simulation level. This is a notable new venue/paper not in the previous profile.
- **New course added:** *Hardware-software co-design* (CS-463) now listed among Bourgeat's teaching duties (was not in previous profile).
- **CADE '25** (*Interoperability of Proof Systems with SC-TPTP*) now appears in the publication list — confirms acceptance; not explicitly noted in prior changelog.
- No other materially new publications or repos beyond those already captured in the 2026-07-10 profile entry.

### 2026-07-10

- **Initial profile created** for Thomas Bourgeat (VCA Lab, EPFL IC).
- **ASPLOS '26 (×2):** *Compass* (taint schemes for RTL security verification) and *Graphiti* (formally verified out-of-order execution in dataflow circuits) accepted; Graphiti artefact released on GitHub.
- **CPP '26:** *Towards Composable Proofs of Cache Coherence Protocols* (with artefact on Zenodo).
- **PLDI '25:** *Making Concurrent Hardware Verification Sequential* — core lab result on simplifying concurrent HW proofs.
- **SOSP '25 (×3):** fast accelerator performance simulation, virtual firmware monitor, and eBPF misbehavior detection via specification-based fuzzing.
- **USENIX Security '25:** *Sailor* — secure context switching paper.
- **HotOS '25:** Lightweight hypervisor verification paper.
- **IEEE S&P '26:** *Interplay of Efficient Model Checking and Secure Processor Design* (secure speculation).
- **Preprint (July 2025):** *SystolicAttention* — fusing FlashAttention within a single systolic array (arXiv:2507.11331).
- Lab has 7 active PhD students; teaches *Constructive Computer Architecture* (CS-629) and *Computer Security and Privacy* (COM-301).
