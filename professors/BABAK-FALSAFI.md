[../PROFESSORS.md](../PROFESSORS.md)  

# Babak Falsafi

**Lab:** Parallel Systems Architecture Laboratory (PARSA)  
**EPFL profile:** [people.epfl.ch](https://people.epfl.ch/babak.falsafi)  
**Web:** [parsa.epfl.ch](https://parsa.epfl.ch/)  
**ORCID:** [0000-0001-5916-8068](https://orcid.org/0000-0001-5916-8068)  
**OpenAlex:** [A5057697787](https://openalex.org/A5057697787)  

Babak Falsafi leads PARSA at EPFL, researching post-Moore server architecture, datacenter systems, GPU microarchitecture, and AI hardware efficiency — most recently focusing on mixed-precision quantization for efficient LLM inference using microscaling (MX) formats.

## Key research

- [PARSA Lab](https://parsa.epfl.ch/)
- [EPFL Profile](https://people.epfl.ch/babak.falsafi)
- [MXSens: Sensitivity-Aware Mixed-Precision Quantization for LLM Inference (arXiv 2026)](https://arxiv.org/abs/2607.17733)
- [Avant-Garde: Empowering GPUs with Scaled Numeric Formats (ISCA 2025)](https://doi.org/10.1145/3695053.3731100)
- [CloudSuite Benchmark Suite](https://www.cloudsuite.ch/)
- [QFlex: Full-System Server Simulation](https://qflex.epfl.ch/)

## Changelog

### 2026-09-21

- **New preprint — MXSens (July 2026):** "MXSens: Sensitivity-Aware Mixed-Precision Quantization for Efficient LLM Inference" (arXiv:2607.17733), co-authored by Falsafi, recently-graduated Simla Burcu Harma, and collaborators including Google's Amir Yazdanbakhsh and EPFL's Martin Jaggi. The method assigns mixed mantissa bitwidths (4/6/8-bit MXINT) to LLM layers and columns based on quantization sensitivity, training-free, achieving state-of-the-art accuracy under W4A4KV4 settings (e.g., perplexity 3.77 on LLaMA-2-70B). This directly extends the Avant-Garde/MX-format line of work into LLM inference efficiency.
- No other materially new papers or lab news since the 2026-07-17 update.

### 2026-07-17

- **New ISCA 2025 paper — Avant-Garde:** A GPU microarchitecture that natively supports scaled numeric formats (FP8, MX, HBFP) by flattening multi-level representations in hardware, achieving 74% higher throughput and 44% lower inference time vs. baseline GPUs. Published June 2025.
- **New ISCA 2025 paper — Jord:** Single-address-space FaaS (Function-as-a-Service) architecture, also presented at ISCA 2025.
- **New journal paper (Aug 2025):** "A Low-latency On-chip Cache Hierarchy for Load-to-use Stall Reduction in GPUs" published in ACM TACO.
- **Recent PhD completion:** Simla Burcu Harma defended in 2026 (thesis listed).
- Previous update (2026-07-10) failed due to LLM error; no substantive prior changelog existed.

### 2026-07-10

- Update failed (LLM error); sources fetched but not summarized.
