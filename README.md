# Virtual Quantum Reality (VQR) & Quantum Privacy Preserving (QPP)

This repository hosts two distinct but related projects: **Virtual Quantum Reality (VQR) – True Uniform Random Number (TURN)**, which explores methods for generating high-quality random numbers in software, and **Quantum Privacy Preserving (QPP)**, which provides implementations of a quantum cryptographic primitive using Qiskit.

---

## VQR – True Uniform Randomness (TURN)

This section focuses on the conceptual and practical aspects of generating truly unpredictable and uniform random numbers in software, aiming to mimic quantum randomness without requiring quantum hardware.

### Key Points:

Three sources of randomness:

*   **Coin flip (physical randomness)**
    *   Approximate probability: 50.8% vs 49.2%.
    *   Shows that even physical randomness has slight bias.
*   **PRNG (Pseudorandom Number Generator)**
    *   Deterministic algorithm.
    *   Provides reproducible randomness (not truly random, but statistically useful).
    *   A hidden pattern exists in code.
*   **QRNG (Quantum Random Number Generator)**
    *   Based on quantum uncertainty (e.g., photon detection).
    *   Provides true randomness, but the distribution is not always uniform.

### Conceptual Mechanisms for VQR / TURN

1.  **Entropy Amplification & Mixing**
    *   Use many weak entropy sources (like system timing jitter, thermal noise estimates, network latency, unpredictable user inputs).
    *   Apply cryptographic mixing functions (e.g., SHA3, Keccak, or ChaCha20 stream cipher) to eliminate bias.
    *   This mimics “quantum uncertainty” by pulling entropy from uncontrollable real-world processes.
    *   👉 Difference from PRNG: It doesn’t rely on a single deterministic seed, but continuously feeds in entropy, making it non-reproducible.
2.  **Virtual Quantum Simulation**
    *   Quantum randomness often comes from superposition → a state collapse is unpredictable.
    *   In software, one can simulate this via:
        *   Complex dynamical systems (chaotic maps, e.g., logistic map, Arnold’s cat map).
        *   High-dimensional noise models approximating quantum measurement statistics.
    *   When carefully tuned, these systems exhibit computational unpredictability close to quantum systems.
3.  **Bias Correction → “True Uniform”**
    *   Even quantum processes yield non-uniform distributions.
    *   To fix bias, software applies randomness extractors (e.g., Von Neumann extractor, Trevisan extractor, universal hashing).
    *   Example: If photons favor 51% “1” vs 49% “0”, the extractor converts it into perfectly uniform bits.
    *   👉 VQR would guarantee uniformity even when raw entropy sources are skewed.
4.  **Cryptographic Hardening**
    *   Once entropy is collected, feed it into:
        *   CSPRNG (Cryptographically Secure PRNG) → ensures unpredictability even if part of entropy leaks.
        *   Strong primitives (AES-CTR, Fortuna, HMAC-DRBG).
    *   This provides resilience: no adversary can “reverse engineer” the randomness.
5.  **Philosophical Angle**
    *   True unpredictability in software is impossible if the system is closed and deterministic.
    *   VQR suggests a “Virtual” method: pull entropy from uncontrollable external micro-events (like CPU jitter, I/O noise, chaotic scheduling).
    *   By continuously injecting entropy + extractor correction, you approximate TURN (True Uniform Randomness) without quantum sensors.

🌀 **Summary**

Conceptually, VQR/TURN = Entropy harvesting (physical + chaotic) → Bias correction → Cryptographic mixing, mimicking quantum unpredictability + uniformity.

It’s a hybrid approach:

*   Not purely PRNG (deterministic).
*   Not strictly QRNG (needs quantum device).

### VQR/TURN Implementations

*   `vqr_turn_rng.py`: This file contains the core implementation of the VQR/TURN random number generator, including entropy collection, mixing, and bias correction.
*   `vqr-turn1.py`: This file utilizes the `VQRTurnRNG` class from `vqr_turn_rng.py` to provide a VQR/TURN random number generator with a Gradio UI and JSON-RPC 2.0 API.
*   `vqr-turn2.py`: This file contains an alternative implementation of the VQR/TURN random number generator, focusing on generating random bits and running NIST statistical tests.

### Key Functions in `vqr_turn_rng.py`

*   `_timing_jitter_bytes(n_bytes: int = 64)`: Harvests timing jitter by tight-loop sampling of perf_counter_ns.
*   `_von_neumann(bits: bytes)`: Applies Von Neumann extractor on a bitstream given as bytes.
*   `_health_checks(raw: bytes)`: Performs basic online health checks on raw entropy.
*   `HMAC_DRBG.__init__(self, seed_material: bytes)`: Initializes the HMAC_DRBG class.
*   `HMAC_DRBG._update(self, provided_data: bytes = b"")`: Updates the HMAC_DRBG state.
*   `HMAC_DRBG.reseed(self, seed_material: bytes)`: Reseeds the HMAC_DRBG with new seed material.
*   `HMAC_DRBG.generate(self, n_bytes: int)`: Generates random bytes using the HMAC_DRBG.
*   `VQRTurnRNG.__init__(self, reseed_interval_bytes: int = 1<<20)`: Initializes the VQRTurnRNG class.
*   `VQRTurnRNG._collect_entropy(self, target_bytes: int = 64)`: Collects entropy from multiple sources.
*   `VQRTurnRNG.reseed(self)`: Reseeds the VQRTurnRNG with new entropy.
*   `VQRTurnRNG.random_bytes(self, n: int)`: Generates random bytes using the VQRTurnRNG.
*   `VQRTurnRNG.random_u64(self)`: Generates a random 64-bit unsigned integer.
*   `VQRTurnRNG.random(self)`: Generates a random float between 0 and 1.
*   `monobit_frequency_test(bits: bytes)`: Performs a monobit frequency test on a bitstring.
*   `chi_square_bytes_uniformity(bytes_seq: bytes)`: Performs a chi-square test for uniformity over bytes.

### Key Functions in `vqr-turn1.py`

*   `random_float()`: Returns a random float value.
*   `random_u64()`: Returns a random 64-bit unsigned integer value.
*   `random_bytes(req: BytesRequest)`: Returns a base64 encoded string of random bytes.
*   `jsonrpc(req: dict)`: Handles JSON-RPC requests.
*   `get_float()`: Returns a random float value for the Gradio UI.
*   `get_u64()`: Returns a random 64-bit unsigned integer value for the Gradio UI.
*   `get_bytes(n)`: Returns a base64 encoded string of random bytes for the Gradio UI.
*   `launch_gradio()`: Launches the Gradio UI.

### Key Functions in `vqr-turn2.py`

*   `generate_vqr_bits(n_bits: int = 1024)`: Simulates Virtual Quantum Reality (VQR) random number generation.
*   `run_all_tests(bits: str)`: Runs all randomness tests on a bitstring.
*   `vqr_turn_service(n_bits: int = 1024)`: Generates random bits and runs NIST tests on them.
*   `gradio_interface(n_bits)`: Generates random bits and runs NIST tests on them for the Gradio UI.
*   `generate(n_bits: int = 1024)`: Generates random bits and runs NIST tests on them for the FastAPI API.

---

## Quantum Privacy Preserving (QPP)

This project contains companion Jupyter notebooks for Quantum Permutation Pad (QPP) implementations with Qiskit Runtime and Qiskit AerSimulator, ranging from 2 to 9 qubits. It serves as illustrations for the paper: Chancé, A. (2024). Quantum Permutation Pad with Qiskit Runtime. In: Femmam, S., Lorenz, P. (eds). ICCNT 2022. Springer, Cham. https://doi.org/10.1007/978-3-031-59619-3_12

Alain's talk, “An Efficient 8-Qubit Quantum Permutation Pad (QPP) Implementation Running on a Laptop”, has been presented at the 2025 IEEE 14th International Conference on Communications, Circuits and Systems (ICCCAS).

The QPP implementations utilize:

*   FastAPI on the server (Remote Agent)
*   requests module on the client
*   File content encoded in Base64
*   JSON-RPC 2.0 over HTTP

The repository includes Jupyter notebooks for Alice and Bob, who exchange a text file and an image file using QPP.

### QPP Directory Structure

The `QPP/` folder contains the implementation of the Quantum Permutation Pad (QPP) with Qiskit Runtime.

*   `QPP/Alice`: Contains the code for Alice, the sender, including Jupyter notebooks for agent setup and QPP execution.
*   `QPP/Bob`: Contains the code for Bob, the receiver, including Jupyter notebooks for agent setup and QPP execution.
*   `QPP/QPP_2_qubits`: Contains the implementation and related files for the 2-qubit QPP.
*   `QPP/QPP_4_qubits`: Contains the implementation and related files for the 4-qubit QPP.
*   `QPP/QPP_9_qubits`: Contains the implementation and related files for the 9-qubit QPP.
*   `QPP/README.md`: Specific documentation for the QPP project.

### QPP Setup and Execution

1.  **Set up IBM Cloud account (optional)**: Refer to [this guide](https://quantum.cloud.ibm.com/docs/en/guides/cloud-setup) for details on how to set up your IBM Cloud account on the upgraded IBM Quantum Platform. Credentials can be saved or provided via `Token.txt` and `CRN.txt` files.
2.  **Run `Bob_agent.ipynb`**: This notebook starts a receiver agent (uvicorn server) to receive files.
3.  **Run `QPP_Alice.ipynb`**: This notebook guides Alice through the QPP setup.
    *   **Gradio UI**: An optional Gradio UI can be launched at `http://127.0.0.1:7860` for configuration.
    *   **Prompt-based setup**: Alternatively, configuration can be done via prompts for plaintext filename, number of qubits, version, trace level, and backend.
    *   **QPP Simulation**: The secret key, QPP parameters, and ciphertext files are sent to Bob's receiver agent.
    *   **Saving Alice's directory**: Option to save the content of Alice's directory after simulation.
4.  **Run `QPP_Bob.ipynb`**: This notebook guides Bob through the decryption process.
    *   Prompts for version.
    *   Decrypts the text or image file received from Alice using the JSON parameter file and secret key.
    *   Option to save the content of Bob's directory after decryption.

### Compatible Qiskit Versions

These Jupyter notebooks work with Python 3.13 and the following Qiskit versions:
*   Qiskit v2.1
*   Qiskit runtime 0.40
*   Qiskit Aer 0.17

Open Plan users cannot submit session jobs; workloads must be run in job mode or batch mode.

### License, Abstract, Credits, Rights and Permissions

The first cell of `QPP_Alice.ipynb` and `QPP_Bob.ipynb` notebooks contains:
*   MIT license
*   Abstract
*   Credit: Kuang, R., Perepechaenko
*   Rights and permissions
*   Adaptations made by Alain Chancé

Updates are presented in the following cells at the end of these notebooks:
*   Summary of updates V6, V5, V4, V3, V2, V1

### References

[1] Kuang, Randy. Quantum Permutation Pad for Quantum Secure Symmetric and Asymmetric Cryptography. Vol. 2, no. 1, Academia Quantum, 2025. https://doi.org/10.20935/AcadQuant7457

[2] I. Burge, M. T. Mai and M. Barbeau, "A Permutation Dispatch Circuit Design for Quantum Permutation Pad Symmetric Encryption," 2024 13th International Conference on Communications, Circuits and Systems (ICCCAS), Xiamen, China, 2024, pp. 35-40, doi: 10.1109/ICCCAS62034.2024.10652827.

[3] Chancé, A. (2024). Quantum Permutation Pad with Qiskit Runtime. In: Femmam, S., Lorenz, P. (eds) Recent Advances in Communication Networks and Embedded Systems. ICCNT 2022. Lecture Notes on Data Engineering and Communications Technologies, vol 205. Springer, Cham. https://doi.org/10.1007/978-3-031-59619-3_12

[4] Kuang, R., Barbeau, M. Quantum permutation pad for universal quantum-safe cryptography. Quantum Inf Process 21, 211 (2022). https://doi.org/10.1007/s11128-022-03557-y

[5] R. Kuang and N. Bettenburg, 'Shannon perfect secrecy in a discrete Hilbert space', in Proc. IEEE Int. Conf. Quantum Comput. Eng. (QCE), Oct. 2020, pp. 249-255, doi: 10.1109/QCE49297.2020.00039

[6] Kuang, R., Perepechaenko, M. Quantum encryption with quantum permutation pad in IBMQ systems. EPJ Quantum Technol. 9, 26 (2022). https://doi.org/10.1140/epjqt/s40507-022-00145-y

[7] Qiskit Runtime overview, IBM Quantum, https://cloud.ibm.com/docs/quantum-computing?topic=quantum-computing-overview

[8] QiskitRuntimeService, https://docs.quantum.ibm.com/api/qiskit-ibm-runtime/qiskit_ibm_runtime.QiskitRuntimeService#qiskitruntimeservice

[9] Qiskit v2.0 migration guide, https://docs.quantum.ibm.com/migration-guides/qiskit-2.0

[10] Qiskit Aer documentation, https://qiskit.github.io/qiskit-aer/

[11] Qiskit Aer 0.16.1, Getting started, https://qiskit.github.io/qiskit-aer/getting_started.html

[12] Qiskit Aer 0.16.1, Simulators, https://qiskit.github.io/qiskit-aer/tutorials/1_aersimulator.html

[13] Migrate from cloud simulators to local simulators, https://docs.quantum.ibm.com/migration-guides/local-simulators#aersimulator

---

## Additional Files

*   `NIST-80022-Statistical Test Suite.pdf`: This document contains the NIST 800-22 Statistical Test Suite, which is relevant for evaluating the randomness of the VQR/TURN generator.
*   `Quantum Permutation Pad.pdf`: This PDF provides foundational information about the Quantum Permutation Pad (QPP) concept.
