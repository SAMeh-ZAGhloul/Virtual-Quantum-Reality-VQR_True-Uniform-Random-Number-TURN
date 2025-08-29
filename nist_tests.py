# nist_tests.py
import math
from scipy.special import erfc
import sp80022suite

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
        "custom_frequency_test": frequency_test(bits),
        "custom_runs_test": runs_test(bits)
    }

    clean_bits = "".join(c for c in bits if c in "01")
    bit_list = [int(b) for b in clean_bits]

    for test in dir(sp80022suite):
        if not test.startswith("_"):
            func = getattr(sp80022suite, test)
            if callable(func):
                try:
                    # Handle different test signatures
                    if test in ["block_frequency", "linear_complexity"]:
                        results[test] = func(bit_list, 128)  # block size
                    elif test in ["approximate_entropy", "serial"]:
                        results[test] = func(bit_list, 10)   # m = 10
                    elif test in ["overlapping_template_matchings", "non_overlapping_template_matchings"]:
                        results[test] = func(bit_list, [1,1,1,1])  # template "1111"
                    else:
                        results[test] = func(bit_list)
                except Exception as e:
                    results[test] = f"Error: {e}"
    return results
