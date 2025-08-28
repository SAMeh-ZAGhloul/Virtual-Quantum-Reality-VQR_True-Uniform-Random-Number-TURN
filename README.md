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

## Repository Documentation

*   `vqr_turn_rng.py`: This file contains the implementation of the VQR/TURN random number generator.
*   `vqr-turn1.py`: This file contains an alternative implementation of the VQR/TURN random number generator.
*   `vqr-turn2.py`: This file contains another alternative implementation of the VQR/TURN random number generator.
*   `NIST-80022-Statistical Test Suite.pdf`: This file contains the NIST 800-22 Statistical Test Suite, which can be used to test the randomness of the VQR/TURN random number generator.
*   `README.md`: This file contains the documentation for the VQR/TURN project.
