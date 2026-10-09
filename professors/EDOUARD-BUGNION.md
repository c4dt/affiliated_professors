[../PROFESSORS.md](../PROFESSORS.md)  

# Edouard Bugnion

<img src="https://people.epfl.ch/edouard.bugnion/photo" alt="Edouard Bugnion" width="150" align="right">

**Lab:** Data Center Systems Laboratory (DCSL)  
**EPFL profile:** [people.epfl.ch](https://people.epfl.ch/edouard.bugnion)  
**Web:** [epfl.ch](https://www.epfl.ch/labs/dcsl/)  
**Code:** [github.com/epfl-dcsl](https://github.com/epfl-dcsl)  
**ORCID:** [0000-0001-7237-6929](https://orcid.org/0000-0001-7237-6929)  
**OpenAlex:** [A5049034675](https://openalex.org/A5049034675)  

Edouard Bugnion leads EPFL's DCSL, researching datacenter efficiency (low-latency networking, in-kernel scheduling) and system security (Trusted Execution Environments, virtual firmware monitors, hardware-software isolation), while serving as EPFL's Vice President for Innovation and Impact.

## Key research

- [DCSL Lab Website](https://www.epfl.ch/labs/dcsl/)
- [EPFL People Page](https://people.epfl.ch/edouard.bugnion)
- [DCSL GitHub Organisation](https://github.com/epfl-dcsl)
- [Flashpoint ASPLOS'27 Artifact – Privileged-Software Isolation on RISC-V](https://github.com/epfl-dcsl/flashpoint)
- [Rakaia OSDI'26 Artifact – In-Kernel Message-Oriented Scheduling](https://github.com/epfl-dcsl/rakaia-osdi26-artifact)
- [Tyche: Composable Isolation (EuroS&P 2026)](https://doi.org/10.1109/eurosp68448.2026.00055)

## Changelog

### 2026-10-01

- **New ASPLOS'27 paper — "Flashpoint":** A new artifact repo [`epfl-dcsl/flashpoint`](https://github.com/epfl-dcsl/flashpoint) appeared (first commit Aug 11, 2026; actively updated through Sep 30, 2026). The paper, titled "Flashpoint: Privileged-Software Isolation on RISC-V", describes a hardware-software co-design that combines a lightweight ISA extension with **Anchor** (a small Rust mediator) to establish a dynamic root of trust for the Tyche security monitor, isolating it from OpenSBI and recording measurements in a TPM. Two Zenodo DOIs published Sep 10, 2026 ([10.5281/zenodo.22688440](https://doi.org/10.5281/zenodo.22688440), [10.5281/zenodo.22688439](https://doi.org/10.5281/zenodo.22688439)) confirm it is in the ASPLOS'27 artifact pipeline. This is the lab's third major systems-security paper in quick succession (after Miralis/SOSP'25 and Tyche/EuroS&P'26).
- **Tyche published at EuroS&P 2026:** The previously tracked ArXiv preprint "Tyche: Composable Isolation as a Foundation to Manage Trust in the Cloud" has now been formally published at IEEE EuroS&P 2026 ([doi:10.1109/eurosp68448.2026.00055](https://doi.org/10.1109/eurosp68448.2026.00055)).
- **`tyche-devel` and `linux-kvm-tyche` actively updated** through Aug 27, 2026, consistent with ongoing Flashpoint / Tyche integration work.
- **No other materially new repos or papers** beyond the above since the last profile update.

### 2026-07-30

- **OSDI'26 paper renamed:** The previously tracked paper "Koma: Achieving Low Tail Latency with In-Kernel Message-Oriented Scheduling" has been **renamed to "Rakaia"** — the artifact repo [`koma-osdi26-artifact`](https://github.com/epfl-dcsl/koma-osdi26-artifact) is now [`rakaia-osdi26-artifact`](https://github.com/epfl-dcsl/rakaia-osdi26-artifact), with the rename reflected in all source files (commit "koma->rakaia", Jul 13 2026). The system (in-kernel message-oriented TCP scheduling for microsecond tail latency) is otherwise unchanged.
- **Miralis SOSP'25 artifact formally published on Zenodo (Jul 20 2026):** Two Zenodo DOIs issued for "The Design and Implementation of a Virtual Firmware Monitor" artifact ([10.5281/zenodo.21452407](https://doi.org/10.5281/zenodo.21452407), [10.5281/zenodo.21452408](https://doi.org/10.5281/zenodo.21452408)), signalling the paper is in final SOSP'25 proceedings pipeline.
- **No other materially new papers or repos** since the last profile update.

### 2026-07-10

- **New role (Jan 2025):** Bugnion became EPFL Vice President for Innovation and Impact.
- **SOSP'25 paper:** "The Design and Implementation of a Virtual Firmware Monitor" (Miralis) — artifact published at [`miralis-sosp25-artifact`](https://github.com/epfl-dcsl/miralis-sosp25-artifact); the paper removes firmware from the TCB using a RISC-V virtual firmware monitor written in Rust.
- **OSDI'26 paper (accepted):** "Koma: Achieving Low Tail Latency with In-Kernel Message-Oriented Scheduling" — artifact published at [`koma-osdi26-artifact`](https://github.com/epfl-dcsl/koma-osdi26-artifact); Koma introduces kernel-level message-oriented TCP scheduling for microsecond-scale tail latency reduction.
- **Recent ArXiv preprint (Jul 2025):** "Tyche: Composable Isolation as a Foundation to Manage Trust in the Cloud" — full treatment of the Tyche trust-management system; the [`tyche-devel`](https://github.com/epfl-dcsl/tyche-devel) repo remains actively updated (last push Jul 2025).
- **NSDI'25 paper:** "SIRD: A Sender-Informed, Receiver-Driven Datacenter Transport Protocol" — simulator and Caladan implementation repos published.
- **PhD completions:** Konstantinos Prasopoulos (2025) and Charly Castes (2026) graduated or are graduating under Bugnion's supervision.
- **Student award:** PhD student Neelu Kalani won the Qualcomm Innovation Fellowship Europe 2024.
- **Active repos:** `tyche-devel` (Rust, TEE framework), `linux-ktls` (kernel TLS), `fold` (Rust), `schedsim` (Go) all saw recent commits in 2026.
