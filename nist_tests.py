# nist_tests.py
import math
from scipy.special import erfc

def frequency_test(bits: str):
    """NIST Frequency (Monobit) Test."""
    n = len(bits)
    s_n = sum(2 * int(b) - 1 for b in bits)
    s_obs = abs(s_n) / math.sqrt(n)
    p_value = erfc(s_obs / math.sqrt(2))
    return p_value

def runs_test(bits: str):
    """NIST Runs Test."""
    n = len(bits)
    pi = sum(int(b) for b in bits) / n
    if abs(pi - 0.5) >= (2 / math.sqrt(n)):
        return 0.0
    v_obs = sum(1 for i in range(n - 1) if bits[i] != bits[i+1]) + 1
    p_value = erfc(abs(v_obs - 2 * n * pi * (1 - pi)) / (2 * math.sqrt(2 * n) * pi * (1 - pi)))
    return p_value

def run_all_tests(bits: str):
    """Run all implemented randomness tests on a bitstring."""
    results = {
        "frequency_test": frequency_test(bits),
        "runs_test": runs_test(bits)
    }
    return results
