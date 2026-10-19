[../PROFESSORS.md](../PROFESSORS.md)  

# Mathias Payer

<img src="https://people.epfl.ch/mathias.payer/photo" alt="Mathias Payer" width="150" align="right">

**Lab:** HexHive Laboratory (HEXHIVE)  
**EPFL profile:** [people.epfl.ch](https://people.epfl.ch/mathias.payer)  
**Web:** [hexhive.epfl.ch](https://hexhive.epfl.ch/)  
**Code:** [github.com/HexHive](https://github.com/HexHive)  
**ORCID:** [0000-0001-5054-7547](https://orcid.org/0000-0001-5054-7547)  
**OpenAlex:** [A5065116578](https://openalex.org/A5065116578)  

Mathias Payer leads the HexHive Laboratory at EPFL, conducting cutting-edge research in systems and software security spanning fuzzing, sanitization, exploit mitigations, firmware rehosting, and blockchain security, with a prolific record at top venues and multiple best-paper awards.

## Key research

- [HexHive Laboratory](https://hexhive.epfl.ch/)
- [HexHive GitHub Organization](https://github.com/HexHive)
- [HexHive Publications](https://hexhive.epfl.ch/publications/)
- [liberator – Automated Fuzz Driver Generation (FSE'25)](https://github.com/HexHive/liberator)
- [Magma – Ground-Truth Fuzzing Benchmark](https://github.com/HexHive/magma)
- [SDP – New Active Repo (C)](https://github.com/HexHive/SDP)

## Changelog

### 2026-10-19

- **New paper at CCS'26:** *"Meme Coin Factories: Uncovering Large-Scale Manipulations on pump.fun"* (Nicolas Szwajcok, Taro Tsuchiya, Enze Liu, Kyle Soska, Mathias Payer, Nicolas Christin) — large-scale study of 15 million coins on pump.fun, identifying five manipulation strategy classes including wash trading, MMaaS, and social media manipulation. Accepted at ACM CCS'26.
- **New arXiv preprint (firmware security):** *"Reactive Peripheral Modeling for Faithful Firmware Rehosting"* (Qinying Wang et al.) — introduces RPM abstraction for faithful BLE firmware rehosting; tool **Bluezz** achieves >2.6× basic-block coverage vs. prior art and uncovers 5 new vulnerabilities. Submitted to CCS'26 (noted in comments).
- **New arXiv preprints (since last update):** *"The Impact of Magma: A Ground-Truth Fuzzing Benchmark"* (self-reflective evaluation of Magma benchmark), *"CodeMechanic: Bug-Property-Guided Program Mitigation"*, *"'Operator, can you hear me?' A Faithful Line into the UNISOC Baseband"*, *"SoK: Taxonomizing the Low-Level Attack Surface of Modern Web Browsers"* — all new since 2026-08-17 profile.
- **New GitHub repo `SDP`** (C, pushed 2026-10-17) — no description yet, most recently active repo in the org; likely a new research artifact.
- **`magma` repo** active again (pushed 2026-10-11, 345★); correlates with "Impact of Magma" paper submission.
- **`taemu` gained stars:** now 16★ (up from 9★ in prior profile), reflecting growing interest in TrustZone emulation work.
- **`Grape` gained stars:** now 17★ (up from 13★); still no public description.
- **Team:** New PhD student **Shibo Ai** and MSc Research Scholar **Miloš Medić** now listed on the lab webpage — both new since the 2026-08-17 profile. Past visitor Yi Xiang (fall '25) has now rolled off.
- **No new awards or structural lab changes** beyond the above.

### 2026-08-17

- **No major structural changes** since the 2026-07-10 profile; the existing paper slate and team roster are confirmed by the current publications page and lab website.
- **New paper confirmed at SEC'26 (3rd):** *"When HTTP 402 Meets the Blockchain: Risks on Emerging x402 Payments"* (Qinying Wang et al.) — HexHive now has **three** papers at USENIX SEC'26; the `x402scope` repo is its artifact.
- **WOOT'26 Best Paper Award** confirmed: *"Squeezing Juicy Variant Bugs Out of Modern Browsers"* (Han Zheng, Flavio Toffalini, Qiang Liu, Mathias Payer) — noted as **best paper award** on the publications page, which was not previously flagged.
- **New papers now indexed:** *"Towards Path-Aware Coverage-Guided Fuzzing"* (CGO'26), *"OTABase"* (ACSAC'25), *"eBPF Misbehavior Detection"* (SOSP'25), *"Fixing 7,400 Bugs for 1$: Cheap Crash-Site Program Repair"* (arXiv preprint), *"Cuckoo Attack: Stealthy and Persistent Attacks Against AI-IDE"* (arXiv preprint) — all appeared in ORCID feed and are new since the previous profile.
- **New notable GitHub repo:** `Grape` (Python, 13★, pushed 2026-05-29) — no description yet, but relatively active and starred.
- **`artow-artifact`** repo now listed: artifact for *"Exploiting Android Apps with Counterfeit Art"* (WOOT'26).
- **`hexhive.github.io`** had a recent push (2026-08-13), suggesting homepage content updates.
- **Team:** No personnel changes beyond what was previously noted; two new post-docs (Qiang Liu and Qinying Wang, formerly visiting PhD students from Zhejiang University) are now listed as Post Docs on the lab page.
- **Routine activity:** ongoing course materials (`cs412-26-fuzzing-lab-resources`), `pubstats` tool updated.

### 2026-07-10

- **Initial profile created** — no prior profile existed.
- **2025 awards (on EPFL profile):** Distinguished Member of ACM (2024); Distinguished Paper at USENIX Security '24 (HyperPill); Best Paper at USENIX WOOT '24 ("Exploiting Android's Hardened Memory Allocator"); Best Paper at RAID '24 (Tango); Best Paper at BAR '24 (SURGEON); **Two** NDSS '25 Distinguished Paper Awards (DUMPLING; type++).
- **Recent high-impact papers (2026):**
  - *TÄMU* (Oakland'26): emulating TrustZone Trusted Applications at the GlobalPlatform-API layer — [source](https://github.com/HexHive/TAEMU).
  - *PrivacyShield* (USENIX SEC'26): relaying BLE beacons to counter unsolicited tracking — [source](https://github.com/HexHive/privacyshield).
  - *CrossFit* (FSE'26): demystifying VM callback bugs in interpreters — [source](https://github.com/HexHive/crossfit-artifact).
  - *CLower* (OOPSLA'26): detecting compiler pessimization bugs via redundant memory accesses.
  - *SYSYPHUZZ* (NDSS'26): syscall-pressure-guided OS fuzzing — [source](https://github.com/HexHive/Sysyphuzz).
  - *It's Not You, It's Me* (EuroSP'26): reevaluating concolic execution vs. fuzzing.
  - Three papers accepted at WOOT'26: browser variant bug squeezing, BLE-based Android ART exploitation, and Bluetooth host-stack fuzzing (FuzzBT).
  - *Subscription Bombing* (CACM 2026): email abuse study.
- **Active GitHub repos (2026):** `liberator` (automated fuzz driver generation, 22 ★), `Sourcerer` (LLVM-based), `taemu` (TEE emulation, 9 ★), `privacyshield` (3 ★), `crossfit-artifact` (2 ★), `x402scope` (new, undescribed).
- **ISCA'25 paper on Jord** (single-address-space FaaS) selected as **IEEE MICRO Top Picks 2026**.
- **New PhD completions:** Atri Bhattacharyya (spring '24 → Oracle Labs), Ahmad Hazimeh (spring '24 → BugScale), Nicolas Badoux (spring '25 → Swissgrid). Post-doc Marcel Busch departed fall '25.
- **New PhD students joined:** Yiwen Xu, Sofia Saltovskaia.
