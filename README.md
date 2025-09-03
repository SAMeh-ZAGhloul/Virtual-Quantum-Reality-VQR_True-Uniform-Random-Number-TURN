# Virtual Quantum Reality (VQR) & Quantum Privacy Preserving (QPP)

This repository hosts two distinct but related projects: **Virtual Quantum Reality (VQR) – True Uniform Random Number (TURN)**, which explores methods for generating high-quality random numbers in software, and **Quantum Privacy Preserving (QPP)**, which provides implementations of a quantum cryptographic primitive using Qiskit.

---

## Table of Contents

- [VQR – True Uniform Randomness (TURN)](#vqr--true-uniform-randomness-turn)
  - [Overview](#overview)
  - [Architecture Diagram](#architecture-diagram)
  - [Core RNG Engine: `vqr_turn_rng` Analysis](#core-rng-engine-vqr_turn_rngpy-analysis)
  - [Implementations](#implementations)
  - [Installation](#installation)
  - [Usage](#usage)
- [Quantum Privacy Preserving (QPP)](#quantum-privacy-preserving-qpp)
  - [Overview](#qpp-overview)
  - [QPP Directory Structure](#qpp-directory-structure)
  - [QPP Setup and Execution](#qpp-setup-and-execution)
  - [References](#references)
- [Additional Files](#additional-files)

---

## VQR – True Uniform Randomness (TURN)

### Overview

This project explores the conceptual and practical aspects of generating truly unpredictable and uniform random numbers in software, aiming to mimic quantum randomness without requiring quantum hardware. It leverages techniques like entropy amplification, bias correction, and cryptographic hardening to produce high-quality randomness.

### Architecture Diagram

The following diagram illustrates the architecture of the VQR/TURN project, its components, and its potential integration with the QPP project.

```mermaid
graph TD
    subgraph VQR_TURN [VQR - True Uniform Random Number]
        A[vqr_turn_rng.py <br> Core RNG Engine] --> B{HMAC-DRBG};
        C[Entropy Sources <br> os.urandom, Timing Jitter] --> D[Health Checks & Von Neumann Extractor];
        D --> A;

        E[vqr-turn1.py <br> Web Service] -- "Imports & Uses" --> A;
        F[FastAPI <br> REST & JSON-RPC] --> E;
        G[Gradio <br> Web UI] --> E;

        H[vqr-turn2.py <br> Alternative RNG & Tester];
        I[NIST SP 800-90B Assessments] --> H;
        J[Gradio <br> Web UI] --> H;
    end

    subgraph QPP [Quantum Permutation Pad]
        K[QPP Project <br> Qiskit Implementation];
    end

    subgraph Integrations
        A -- "Provides High-Quality Randomness For" --> K;
    end

    style VQR_TURN fill:#6cb7f0,stroke:#333,stroke-width:2px
    style QPP fill:#ccf,stroke:#333,stroke-width:2px
    style Integrations fill:#cfc,stroke:#333,stroke-width:2px
```

### Core RNG Engine: `vqr_turn_rng.py` Analysis

The `vqr_turn_rng.py` script implements a conceptual **Virtual Quantum Reality / True Uniform Random Number (VQR/TURN)** generator. It is designed as a teaching and demonstration tool, not as a cryptographically secure generator for production use.

The architecture follows a sophisticated multi-stage pipeline to produce high-quality random numbers:

1. **Entropy Collection:**

   * It gathers initial randomness (entropy) from two distinct sources:
     * `os.urandom`: A cryptographically strong source of randomness provided by the operating system.
     * **Timing Jitter:** A custom function (`_timing_jitter_bytes`) that measures the tiny, unpredictable variations in CPU execution time from a tight loop. This mimics a physical entropy source.
2. **Health Checks & Conditioning:**

   * Before use, the raw entropy undergoes online **health checks** to detect potential failures or biases. These include:
     * A **Repetition Count Test** to ensure no long runs of identical bits.
     * An **Adaptive Proportion Test** to verify that the number of 0s and 1s is balanced.
   * The raw data is then passed through a **Von Neumann extractor** (`_von_neumann`), a classic algorithm that removes statistical bias from a bitstream.
   * Finally, the debiased entropy is mixed and condensed into a fixed-size seed using the **SHA3-256** hash function.
3. **Random Number Generation:**

   * The processed seed is used to initialize a **HMAC-DRBG** (Deterministic Random Bit Generator), which is implemented following the style of NIST SP 800-90A, a widely recognized standard.
   * This DRBG is the core engine that expands the initial seed into a long stream of pseudo-random bytes.
4. **Reseeding:**

   * To ensure long-term security and prevent the internal state from becoming stale, the generator automatically **reseeds** itself with fresh entropy after generating a certain amount of data (1 MB by default).
5. **Statistical Validation:**

   * The file also includes utility functions for basic statistical analysis of the output, such as a **Monobit Frequency Test** and a **Chi-Square Uniformity Test**, to provide a sanity check on the quality of the generated random numbers.

### Implementations

There are three Python scripts in this project:

* `vqr_turn_rng.py`: This file contains the core implementation of the VQR/TURN random number generator. For a detailed breakdown, see the [Core RNG Engine Analysis](#core-rng-engine-vqr_turn_rngpy-analysis) section above.
* `vqr-turn1.py`: This script exposes the `VQRTurnRNG` from `vqr_turn_rng.py` as a web service. It uses FastAPI to create REST and JSON-RPC 2.0 endpoints for generating random floats, 64-bit unsigned integers, and bytes. It also provides a simple web interface using Gradio for easy demonstration.
* `vqr-turn2.py`: This file presents an alternative implementation that focuses on generating random bits and testing their quality using the NIST SP 800-90B entropy assessment suite. It also provides a Gradio UI and a FastAPI REST API. This implementation uses Python's standard `random` module for bit generation, which is not cryptographically secure, and is intended for demonstration and testing purposes.

### Installation

To run these scripts, you need to install the required Python packages. You can install them using pip:

```bash
pip install fastapi uvicorn gradio
```

You will also need to compile the C++ NIST SP 800-90B assessment tool. Please see the `NIST.SP800-90B_Entropy-Assessment/README.md` for instructions.

### Usage

You can run each of the `vqr-turn` scripts as follows:

* **`vqr-turn1.py`**: This will start a web server with the Gradio UI and the API.

  ```bash
  python vqr-turn1.py
  ```

  - The FastAPI service will be available at `http://localhost:8000`.
  - The Gradio UI will be available at `http://localhost:7860`.
* **`vqr-turn2.py`**: This script can be run in two modes.

  - To launch the Gradio UI:
    ```bash
    python vqr-turn2.py
    ```
  - To launch the FastAPI API:
    ```bash
    python vqr-turn2.py api
    ```

---

# Entroby Test (ent)

## Statistical Randomness (what ent tested)

### Your file passes basic statistical tests:

1- Entropy ~ 8 bits/byte
2- Balanced distribution across all 256 byte values
3- No correlation between bytes
4- Monte Carlo π estimate close to the real value

### This means the data is indistinguishable from random to simple statistical tools.

1- **Entropy = 7.999994 bits per byte**  The maximum entropy possible for 8-bit data is **8 bits per byte**.  Your file is essentially perfectly random, or at least indistinguishable from random by this test.  Practical meaning: No lossless compression can shrink it further.

2- **Optimum compression = 0%**  Since entropy is already maximal, compression algorithms like gzip or bzip2 would not reduce the size.  The file is already “**incompressible**.”

3- **Chi-square distribution = 222.90 (p ≈ 92.73%)**  The chi-square test checks uniformity of byte distribution **(0–255)**.  A value in the middle range is expected for random data.  Here, the probability that a truly random sequence would produce a higher chi-square is 92.73%, which is still within acceptable randomness expectations.  In short: looks random.

4- **Arithmetic mean = 127.4907 (ideal = 127.5)**  Perfectly balanced between 0–255.  Suggests no bias toward high or low byte values.

5- **Monte Carlo value for Pi = 3.142776116 (error 0.04%)**  ent estimates π by randomly sampling coordinate pairs from the data.  Your result is very close to **true π** (3.14159…), which again indicates strong randomness.

6- **Serial correlation coefficient = 0.000303 (ideal = 0.0)**  Measures how much each byte is correlated with the previous one.  A value near 0 indicates no correlation; your file is essentially uncorrelated.

# Cryptographic Randomness

## Cryptographic randomness is about unpredictability, not just passing statistical tests.

### A weak pseudo-random number generator (PRNG) might pass ent but still be predictable if you know the algorithm/seed.

To call it cryptographically secure, you’d need properties like:
1- Non-determinism (can’t reconstruct the sequence from a partial output)
2- Resistance to backtracking (knowing previous outputs doesn’t reveal future ones)
3- Resistance to prediction (no feasible shortcut better than brute force)

### dieharder-Robert G. Brown

https://webhome.phy.duke.edu/~rgb/General/dieharder.php
https://github.com/seehuhn/dieharder

### Sample Test Results

dieharder -a -f samples.bin
#=============================================================================#
### dieharder version 3.31.1 Copyright 2003 Robert G. Brown
#=============================================================================#
   rng_name    |           filename             |rands/second|
        mt19937|                     samples.bin|  2.14e+08  |
#=============================================================================#
        test_name   |ntup| tsamples |psamples|  p-value |Assessment

| Test Name               | ntup  | tsamples | psamples | p-value       | Assessment |
| ----------------------- | ----- | -------- | -------- | ------------- | ---------- |
| diehard_birthdays       | 0     | 100      | 100      | 0.92921659    | 🟢 PASSED  |
| diehard_operm5          | 0     | 1000000  | 100      | 0.85979285    | 🟢 PASSED  |
| diehard_rank_32x32      | 0     | 40000    | 100      | 0.86845104    | 🟢 PASSED  |
| diehard_rank_6x8        | 0     | 100000   | 100      | 0.47508380    | 🟢 PASSED  |
| diehard_bitstream       | 0     | 2097152  | 100      | 0.20007870    | 🟢 PASSED  |
| diehard_opso            | 0     | 2097152  | 100      | 0.92720025    | 🟢 PASSED  |
| diehard_oqso            | 0     | 2097152  | 100      | 0.97339456    | 🟢 PASSED  |
| diehard_dna             | 0     | 2097152  | 100      | 0.25053825    | 🟢 PASSED  |
| diehard_count_1s_str    | 0     | 256000   | 100      | 0.22948193    | 🟢 PASSED  |
| diehard_count_1s_byt    | 0     | 256000   | 100      | 0.23258425    | 🟢 PASSED  |
| diehard_parking_lot     | 0     | 12000    | 100      | 0.30644186    | 🟢 PASSED  |
| diehard_2dsphere        | 2     | 8000     | 100      | 0.97238648    | 🟢 PASSED  |
| diehard_3dsphere        | 3     | 4000     | 100      | 0.60172815    | 🟢 PASSED  |
| diehard_squeeze         | 0     | 100000   | 100      | 0.10737538    | 🟢 PASSED  |
| diehard_sums            | 0     | 100      | 100      | 0.04916443    | 🟢 PASSED  |
| diehard_runs            | 0     | 100000   | 100      | 0.86049149    | 🟢 PASSED  |
| diehard_runs            | 0     | 100000   | 100      | 0.73462738    | 🟢 PASSED  |
| diehard_craps           | 0     | 200000   | 100      | 0.99974607    | 🟡 WEAK    |
| diehard_craps           | 0     | 200000   | 100      | 0.65448055    | 🟢 PASSED  |
| marsaglia_tsang_gcd     | 0     | 10000000 | 100      | 0.21899736    | 🟢 PASSED  |
| marsaglia_tsang_gcd     | 0     | 10000000 | 100      | 0.99331908    | 🟢 PASSED  |
| sts_monobit             | 1     | 100000   | 100      | 0.52185888    | 🟢 PASSED  |
| sts_runs                | 2     | 100000   | 100      | 0.37388690    | 🟢 PASSED  |
| sts_serial (1–16 runs) | …    | 100000   | 100      | various       | 🟢 PASSED  |
| rgb_bitdist (1–12)     | …    | 100000   | 100      | various       | 🟢 PASSED  |
| rgb_minimum_distance    | 2–5  | 10000    | 1000     | various       | 🟢 PASSED  |
| rgb_permutations        | 2–5  | 100000   | 100      | various       | 🟢 PASSED  |
| rgb_lagged_sum (0–32)  | 0–32 | 1000000  | 100      | various       | 🟢 PASSED  |
| rgb_kstest_test         | 0     | 10000    | 1000     | 0.02450848    | 🟢 PASSED  |
| dab_bytedistrib         | 0     | 51200000 | 1        | 0.67906192    | 🟢 PASSED  |
| dab_dct                 | 256   | 50000    | 1        | 0.04672474    | 🟢 PASSED  |
| dab_filltree (2 runs)   | 32    | 15000000 | 1        | 0.1545/0.3505 | 🟢 PASSED  |
| dab_filltree2 (2 runs)  | 0–1  | 5000000  | 1        | 0.6399/0.5067 | 🟢 PASSED  |
| dab_monobit2            | 12    | 65000000 | 1        | 0.88319991    | 🟢 PASSED  |

## Quantum Privacy Preserving (QPP)

### QPP Overview

This project is forked from: https://github.com/AlainChance/QPP-Alain, and contains companion Jupyter notebooks for Quantum Permutation Pad (QPP) implementations with Qiskit Runtime and Qiskit AerSimulator, ranging from 2 to 9 qubits. It serves as illustrations for the paper: Chancé, A. (2024). Quantum Permutation Pad with Qiskit Runtime. In: Femmam, S., Lorenz, P. (eds). ICCNT 2022. Springer, Cham. https://doi.org/10.1007/978-3-031-59619-3_12

### QPP Directory Structure

The `QPP/` folder contains the implementation of the Quantum Permutation Pad (QPP) with Qiskit Runtime.

* `QPP/Alice`: Contains the code for Alice, the sender, including Jupyter notebooks for agent setup and QPP execution.
* `QPP/Bob`: Contains the code for Bob, the receiver, including Jupyter notebooks for agent setup and QPP execution.
* `QPP/QPP_2_qubits`: Contains the implementation and related files for the 2-qubit QPP.
* `QPP/QPP_4_qubits`: Contains the implementation and related files for the 4-qubit QPP.
* `QPP/QPP_9_qubits`: Contains the implementation and related files for the 9-qubit QPP.
* `QPP/README.md`: Specific documentation for the QPP project.

### QPP Setup and Execution

1. **Set up IBM Cloud account (optional)**: Refer to [this guide](https://quantum.cloud.ibm.com/docs/en/guides/cloud-setup) for details on how to set up your IBM Cloud account on the upgraded IBM Quantum Platform.
2. **Run `Bob_agent.ipynb`**: This notebook starts a receiver agent (uvicorn server) to receive files.
3. **Run `QPP_Alice.ipynb`**: This notebook guides Alice through the QPP setup.
4. **Run `QPP_Bob.ipynb`**: This notebook guides Bob through the decryption process.

For more detailed instructions, please refer to the `QPP/README.md` file.

### References

[1] Kuang, Randy. Quantum Permutation Pad for Quantum Secure Symmetric and Asymmetric Cryptography. Vol. 2, no. 1, Academia Quantum, 2025. https://doi.org/10.20935/AcadQuant7457

[2] I. Burge, M. T. Mai and M. Barbeau, "A Permutation Dispatch Circuit Design for Quantum Permutation Pad Symmetric Encryption," 2024 13th International Conference on Communications, Circuits and Systems (ICCCAS), Xiamen, China, 2024, pp. 35-40, doi: 10.1109/ICCCAS62034.2024.10652827.

[3] Chancé, A. (2024). Quantum Permutation Pad with Qiskit Runtime. In: Femmam, S., Lorenz, P. (eds) Recent Advances in Communication Networks and Embedded Systems. ICCNT 2022. Lecture Notes on Data Engineering and Communications Technologies, vol 205. Springer, Cham. https://doi.org/10.1007/978-3-031-59619-3_12

---

## Additional Files

* `NIST.SP.800-90B.pdf`: This document contains the NIST SP 800-90B Recommendation for the Entropy Sources Used for Random Bit Generation.
* `Quantum Permutation Pad.pdf`: This PDF provides foundational information about the Quantum Permutation Pad (QPP) concept.
