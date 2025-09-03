# nist_tests.py
import subprocess
import tempfile
import os
import re

import subprocess
import tempfile
import os
import re

def _run_assessment(bits: str, tool: str):
    """
    Helper function to run a specific NIST SP 800-90B assessment tool.
    """
     # The C++ tool expects raw bytes, not a string of '0's and '1's.
    # We need to convert the bitstring into a byte array.
    if len(bits) % 8 != 0:
        # Pad with zeros if not a multiple of 8
        bits += '0' * (8 - len(bits) % 8)
    
    byte_array = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        byte_array.append(int(byte, 2))

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(byte_array)
        tmp_path = tmp.name

    results = {}
    # Path to the compiled test executable
    executable_path = os.path.join("NIST.SP800-90B_Entropy-Assessment", "cpp", tool)
    try:
        # Run the test
        # The tool takes the file path and bits per symbol (8 for bytes)
        command = [executable_path, "-v", tmp_path, "8"]
        process = subprocess.run(command, capture_output=True, text=True, check=True)
        
        output = process.stdout
        
        # Parse the output to get the entropy estimate
        entropy_match = re.search(r"min\(H_original, 8 X H_bitstring\): (\d+\.\d+)", output)
        if entropy_match:
            results["min_entropy"] = float(entropy_match.group(1))
        else:
            # Fallback for IID, which has a different output format
            entropy_match = re.search(r"H_bitstring: (\d+\.\d+)", output)
            if entropy_match:
                results["min_entropy"] = float(entropy_match.group(1))
            else:
                results["min_entropy"] = "Could not parse entropy estimate from output."
            
        results["raw_output"] = output

    except FileNotFoundError:
        results["error"] = f"Executable not found at {executable_path}. Please compile the SP 800-90B assessment tool."
    except subprocess.CalledProcessError as e:
        results["error"] = f"Error running SP 800-90B assessment tool: {e.stderr}"
    except Exception as e:
        results["error"] = f"An unexpected error occurred: {e}"
    finally:
        # Clean up the temporary file
        os.remove(tmp_path)
        
    return results

def run_sp800_90b_assessments(bits: str):
    """
    Runs the NIST SP 800-90B IID and non-IID assessments on a bitstring.
    """
    results = {
        "iid": _run_assessment(bits, "ea_iid"),
        "non_iid": _run_assessment(bits, "ea_non_iid")
    }
    return results

def run_ent_test(file_path: str):
    """
    Runs the 'ent' (entropy) test on a given file.
    """
    results = {}
    try:
        command = ["ent", "-t", file_path]
        process = subprocess.run(command, capture_output=True, text=True, check=True)
        output_lines = process.stdout.strip().splitlines()
        if len(output_lines) < 2:
            results["error"] = "Unexpected 'ent -t' output format: not enough lines."
            results["raw_output"] = process.stdout.strip()
            return results

        headers = [h.strip().replace('-', '_').lower() for h in output_lines[0].split(',')]
        values = output_lines[1].split(',')

        # Skip the first column (index) and file-bytes
        for i in range(2, len(headers)):
            key = headers[i]
            try:
                results[key] = float(values[i].strip())
            except (ValueError, IndexError):
                results[key] = values[i].strip()
        results["raw_output"] = process.stdout.strip()

    except FileNotFoundError:
        results["error"] = "The 'ent' command was not found. Please ensure it is installed and in your PATH."
    except subprocess.CalledProcessError as e:
        results["error"] = f"Error running 'ent' command: {e.stderr}"
    except Exception as e:
        results["error"] = f"An unexpected error occurred with 'ent': {e}"
    return results

def run_dieharder_test(file_path: str):
    """
    Runs the 'dieharder' test suite on a given file.
    """
    results = {}
    try:
        # -a runs all tests, -f specifies input file
        command = ["dieharder", "-a", "-f", file_path]
        process = subprocess.run(command, capture_output=True, text=True, check=True)
        output = process.stdout
        
        # Parse dieharder output - this can be extensive, so we'll capture key summaries
        # Look for lines indicating test results (e.g., PASSED, FAILED)
        test_results = []
        for line in output.splitlines():
            if "PASSED" in line or "FAILED" in line or "WEAK" in line:
                test_results.append(line.strip())
        
        results["summary"] = test_results
        results["raw_output"] = output

    except FileNotFoundError:
        results["error"] = "The 'dieharder' command was not found. Please ensure it is installed and in your PATH."
    except subprocess.CalledProcessError as e:
        results["error"] = f"Error running 'dieharder' command: {e.stderr}"
    except Exception as e:
        results["error"] = f"An unexpected error occurred with 'dieharder': {e}"
    return results

def generate_report(all_results: dict):
    """
    Generates a summary report from the test results.
    """
    report = "--- Randomness Test Report ---\n\n"

    if "nist_800_90b" in all_results:
        report += "NIST SP 800-90B Assessments:\n"
        nist_results = all_results["nist_800_90b"]
        if "iid" in nist_results:
            report += "  IID Assessment:\n"
            if "error" in nist_results["iid"]:
                report += f"    Error: {nist_results['iid']['error']}\n"
            else:
                report += f"    Min-Entropy: {nist_results['iid'].get('min_entropy', 'N/A')}\n"
        if "non_iid" in nist_results:
            report += "  Non-IID Assessment:\n"
            if "error" in nist_results["non_iid"]:
                report += f"    Error: {nist_results['non_iid']['error']}\n"
            else:
                report += f"    Min-Entropy: {nist_results['non_iid'].get('min_entropy', 'N/A')}\n"
        report += "\n"

    if "ent_test" in all_results:
        report += "ENT (Entropy) Test:\n"
        ent_results = all_results["ent_test"]
        if "error" in ent_results:
            report += f"  Error: {ent_results['error']}\n"
        else:
            report += f"  Entropy: {ent_results.get('entropy', 'N/A')}\n"
            report += f"  Chi-square: {ent_results.get('chi-square', 'N/A')}\n"
            report += f"  Mean: {ent_results.get('mean', 'N/A')}\n"
            report += f"  Monte Carlo Pi: {ent_results.get('monte_carlo_pi', 'N/A')}\n"
            report += f"  Serial Correlation: {ent_results.get('serial_correlation', 'N/A')}\n"
        report += "\n"

    if "dieharder_test" in all_results:
        report += "Dieharder Test Suite:\n"
        dieharder_results = all_results["dieharder_test"]
        if "error" in dieharder_results:
            report += f"  Error: {dieharder_results['error']}\n"
        else:
            if dieharder_results.get("summary"):
                for line in dieharder_results["summary"]:
                    report += f"  - {line}\n"
            else:
                report += "  No summary results parsed. Check raw output for details.\n"
        report += "\n"
    
    return report

if __name__ == "__main__":
    target_file = "samples.bin" # Corrected from sample.bin to samples.bin based on file list
    all_test_results = {}

    # Read the binary file
    try:
        with open(target_file, "rb") as f:
            binary_data = f.read()
        
        # Convert binary data to bitstring for NIST 800-90B tests
        bits = ''.join(format(byte, '08b') for byte in binary_data)

        print(f"Running NIST SP 800-90B assessments on {target_file}...")
        nist_90b_results = run_sp800_90b_assessments(bits)
        all_test_results["nist_800_90b"] = nist_90b_results
        print("NIST SP 800-90B assessments completed.\n")

        print(f"Running ENT test on {target_file}...")
        ent_results = run_ent_test(target_file)
        all_test_results["ent_test"] = ent_results
        print("ENT test completed.\n")

        print(f"Running Dieharder test suite on {target_file}...")
        dieharder_results = run_dieharder_test(target_file)
        all_test_results["dieharder_test"] = dieharder_results
        print("Dieharder test suite completed.\n")

        final_report = generate_report(all_test_results)
        print(final_report)

        # Optionally, save the report to a file
        with open("randomness_report.txt", "w") as report_file:
            report_file.write(final_report)
        print("\nReport saved to randomness_report.txt")

    except FileNotFoundError:
        print(f"Error: The file '{target_file}' was not found.")
    except Exception as e:
        print(f"An error occurred during the testing process: {e}")
