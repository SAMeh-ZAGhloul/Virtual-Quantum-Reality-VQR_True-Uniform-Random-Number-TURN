# nist_tests.py
import subprocess
import tempfile
import os
import re

def run_sp800_90b_assessments(bits: str):
    """
    Runs the NIST SP 800-90B IID and non-IID assessments on a bitstring.
    """
    results = {
        "iid": _run_assessment(bits, "ea_iid"),
        "non_iid": _run_assessment(bits, "ea_non_iid")
    }
    return results

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
