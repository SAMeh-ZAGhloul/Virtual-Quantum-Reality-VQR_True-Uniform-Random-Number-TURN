# test_nist_module.py
from nist_tests import run_all_tests
from vqr_turn import generate_vqr_bits

def test_nist_module():
    """
    Tests the NIST module by generating a random bitstring and running the
    statistical tests on it.
    """
    # Generate a random bitstring of 1000000 bits
    bit_string = generate_vqr_bits(1000000)

    # Run the NIST statistical tests
    results = run_all_tests(bit_string)

    # Print the results
    print("NIST Statistical Test Suite Results:")
    for test_name, result in results.items():
        print(f"- {test_name}: {result}")

if __name__ == "__main__":
    test_nist_module()
