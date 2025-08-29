# vqr_turn.py
import random

# -------------------------------
# VQR: True Uniform Random Number Generator
# -------------------------------
def generate_vqr_bits(n_bits: int = 1024) -> str:
    """Simulates Virtual Quantum Reality (VQR) random number generation."""
    return "".join(random.choice("01") for _ in range(n_bits))
