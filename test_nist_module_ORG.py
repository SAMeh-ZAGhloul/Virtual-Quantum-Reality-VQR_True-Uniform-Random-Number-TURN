# test_nist_module.py
from nist_tests import run_sp800_90b_assessments
from vqr_turn import generate_vqr_bits

def test_nist_module():
    """
    Tests the NIST module by generating a random bitstring and running the
    SP 800-90B entropy assessments on it.
    """
    # Generate a random bitstring of 1,000,000 bits
    bit_string = generate_vqr_bits(1000000)

    # Run the NIST SP 800-90B assessments
    all_results = run_sp800_90b_assessments(bit_string)

    # Print the results
    for test_type, results in all_results.items():
        print(f"\n--- NIST SP 800-90B {test_type.upper()} Assessment Results ---")
        if "error" in results:
            print(f"An error occurred: {results['error']}")
        else:
            print(f"  Minimum Entropy: {results.get('min_entropy', 'N/A')}")
            print("\n--- Raw Output ---")
            print(results.get('raw_output', ''))

if __name__ == "__main__":
    test_nist_module()
