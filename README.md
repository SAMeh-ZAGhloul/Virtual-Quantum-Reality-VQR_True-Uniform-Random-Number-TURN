# VQR – True Uniform Randomness

Can randomness produced in software be truly unpredictable?

**Key Points:**

Three sources of randomness:

*   Coin flip (physical randomness)
    *   Approximate probability: 50.8% vs 49.2%.
    *   Shows that even physical randomness has slight bias.
*   PRNG (Pseudorandom Number Generator)
    *   Deterministic algorithm.
    *   Provides reproducible randomness (not truly random, but statistically useful).
    *   A hidden pattern exists in code.
*   QRNG (Quantum Random Number Generator)
    *   Based on quantum uncertainty (e.g., photon detection).
    *   Provides true randomness, but the distribution is not always uniform.

**Conceptual Mechanisms for VQR / TURN**

1.  Entropy Amplification & Mixing
    *   Use many weak entropy sources (like system timing jitter, thermal noise estimates, network latency, unpredictable user inputs).
    *   Apply cryptographic mixing functions (e.g., SHA3, Keccak, or ChaCha20 stream cipher) to eliminate bias.
    *   This mimics “quantum uncertainty” by pulling entropy from uncontrollable real-world processes.
    *   👉 Difference from PRNG: It doesn’t rely on a single deterministic seed, but continuously feeds in entropy, making it non-reproducible.
2.  Virtual Quantum Simulation
    *   Quantum randomness often comes from superposition → a state collapse is unpredictable.
    *   In software, one can simulate this via:
        *   Complex dynamical systems (chaotic maps, e.g., logistic map, Arnold’s cat map).
        *   High-dimensional noise models approximating quantum measurement statistics.
    *   When carefully tuned, these systems exhibit computational unpredictability close to quantum systems.
3.  Bias Correction → “True Uniform”
    *   Even quantum processes yield non-uniform distributions.
    *   To fix bias, software applies randomness extractors (e.g., Von Neumann extractor, Trevisan extractor, universal hashing).
    *   Example: If photons favor 51% “1” vs 49% “0”, the extractor converts it into perfectly uniform bits.
    *   👉 VQR would guarantee uniformity even when raw entropy sources are skewed.
4.  Cryptographic Hardening
    *   Once entropy is collected, feed it into:
        *   CSPRNG (Cryptographically Secure PRNG) → ensures unpredictability even if part of entropy leaks.
        *   Strong primitives (AES-CTR, Fortuna, HMAC-DRBG).
    *   This provides resilience: no adversary can “reverse engineer” the randomness.
5.  Philosophical Angle
    *   True unpredictability in software is impossible if the system is closed and deterministic.
    *   VQR suggests a “Virtual” method: pull entropy from uncontrollable external micro-events (like CPU jitter, I/O noise, chaotic scheduling).
    *   By continuously injecting entropy + extractor correction, you approximate TURN (True Uniform Randomness) without quantum sensors.

🌀 **Summary**

Conceptually, VQR/TURN = Entropy harvesting (physical + chaotic) → Bias correction → Cryptographic mixing, mimicking quantum unpredictability + uniformity.

It’s a hybrid approach:

*   Not purely PRNG (deterministic).
*   Not strictly QRNG (needs quantum device).

## Quantum Privacy Preserving (QPP)

This repository contains companion Jupyter notebooks for Quantum Permutation Pad (QPP) implementations with Qiskit Runtime and Qiskit AerSimulator ranging from 2 to 9 qubits. It serves as illustrations for the paper: Chancé, A. (2024). Quantum Permutation Pad with Qiskit Runtime. In: Femmam, S., Lorenz, P. (eds). ICCNT 2022. Springer, Cham. https://doi.org/10.1007/978-3-031-59619-3_12

Alain's talk, “An Efficient 8-Qubit Quantum Permutation Pad (QPP) Implementation Running on a Laptop”, has been presented at the 2025 IEEE 14th International Conference on Communications, Circuits and Systems (ICCCAS).

The QPP implementations utilize:

*   FastAPI on the server (Remote Agent)
*   requests module on the client
*   File content encoded in Base64
*   JSON-RPC 2.0 over HTTP

The repository includes Jupyter notebooks for Alice and Bob, who exchange a text file and an image file using QPP.

## Repository Documentation

*   `vqr_turn_rng.py`: This file contains the implementation of the VQR/TURN random number generator.
*   `vqr-turn1.py`: This file contains an alternative implementation of the VQR/TURN random number generator.
*   `vqr-turn2.py`: This file contains another alternative implementation of the VQR/TURN random number generator.

### Implementations

*   `vqr-turn1.py`: This file utilizes the `VQRTurnRNG` class from `vqr_turn_rng.py` to provide a VQR/TURN random number generator.
*   `vqr_turn_rng.py`: This file contains the `VQRTurnRNG` class, which implements the core logic for the VQR/TURN random number generator.
*   `vqr-turn2.py`: This file contains another alternative implementation of the VQR/TURN random number generator.

### Functions in `vqr_turn_rng.py`

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

### Functions in `vqr-turn1.py`

*   `random_float()`: Returns a random float value.
*   `random_u64()`: Returns a random 64-bit unsigned integer value.
*   `random_bytes(req: BytesRequest)`: Returns a base64 encoded string of random bytes.
*   `jsonrpc(req: dict)`: Handles JSON-RPC requests.
*   `get_float()`: Returns a random float value for the Gradio UI.
*   `get_u64()`: Returns a random 64-bit unsigned integer value for the Gradio UI.
*   `get_bytes(n)`: Returns a base64 encoded string of random bytes for the Gradio UI.
*   `launch_gradio()`: Launches the Gradio UI.

### Functions in `vqr-turn2.py`

*   `generate_vqr_bits(n_bits: int = 1024)`: Simulates Virtual Quantum Reality (VQR) random number generation.
*   `run_all_tests(bits: str)`: Runs all randomness tests on a bitstring.
*   `vqr_turn_service(n_bits: int = 1024)`: Generates random bits and runs NIST tests on them.
*   `gradio_interface(n_bits)`: Generates random bits and runs NIST tests on them for the Gradio UI.
*   `generate(n_bits: int = 1024)`: Generates random bits and runs NIST tests on them for the FastAPI API.

*   `NIST-80022-Statistical Test Suite.pdf`: This file contains the NIST 800-22 Statistical Test Suite, which can be used to test the randomness of the VQR/TURN random number generator.
*   `README.md`: This file contains the documentation for the VQR/TURN project.

## Quantum Privacy Preserving (QPP)

This repository contains companion Jupyter notebooks for Quantum Permutation Pad (QPP) implementations with Qiskit Runtime and Qiskit AerSimulator ranging from 2 to 9 qubits. It serves as illustrations for the paper: Chancé, A. (2024). Quantum Permutation Pad with Qiskit Runtime. In: Femmam, S., Lorenz, P. (eds). ICCNT 2022. Springer, Cham. https://doi.org/10.1007/978-3-031-59619-3_12

Alain's talk, “An Efficient 8-Qubit Quantum Permutation Pad (QPP) Implementation Running on a Laptop”, has been presented at the 2025 IEEE 14th International Conference on Communications, Circuits and Systems (ICCCAS).

The QPP implementations utilize:

*   FastAPI on the server (Remote Agent)
*   requests module on the client
*   File content encoded in Base64
*   JSON-RPC 2.0 over HTTP

The repository includes Jupyter notebooks for Alice and Bob, who exchange a text file and an image file using QPP.

The QPP folder contains the implementation of the Quantum Permutation Pad (QPP) with Qiskit Runtime. It includes the code for Alice and Bob, who exchange a text file and an image file using QPP. It also includes the Gradio UI for configuring and running the QPP simulation.
*   QPP/Alice: Contains the code for Alice, the sender.
*   QPP/Bob: Contains the code for Bob, the receiver.
*   QPP/QPP_2_qubits: Contains the code for the 2-qubit QPP implementation.
*   QPP/QPP_4_qubits: Contains the code for the 4-qubit QPP implementation.
*   QPP/QPP_9_qubits: Contains the code for the 9-qubit QPP implementation.

QPP/README.md: This file contains the documentation for the QPP folder.
</final_file_content>

IMPORTANT: For any future changes to this file, use the final_file_content shown above as your reference. This content reflects the current state of the file, including any auto-formatting (e.g., if you used single quotes but the formatter converted them to double quotes). Always base your SEARCH/REPLACE operations on this final version to ensure accuracy.

<environment_details>
# VSCode Visible Files
README.md

# VSCode Open Tabs
README.md
vqr-turn2.py
vqr-turn1.py
vqr_turn_rng.py

# Current Time
8/28/2025, 11:13:11 PM (Africa/Cairo, UTC+3:00)

# Context Window Usage
217,398 / 1,048.576K tokens used (21%)

# Current Mode
ACT MODE
