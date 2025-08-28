# vqr_turn_service.py
# pip install fastapi uvicorn gradio sp80022suite

import random
import sp80022suite
import gradio as gr
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

# -------------------------------
# VQR: True Uniform Random Number Generator
# -------------------------------
def generate_vqr_bits(n_bits: int = 1024) -> str:
    """Simulates Virtual Quantum Reality (VQR) random number generation."""
    return "".join(random.choice("01") for _ in range(n_bits))


# -------------------------------
# Randomness Test Runner (NIST SP800-22)
# -------------------------------
def run_all_tests(bits: str):
    """Run all randomness tests on a bitstring."""
    clean_bits = "".join(c for c in bits if c in "01")
    bit_list = [int(b) for b in clean_bits]   # ✅ correct input type
    
    results = {}
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


# -------------------------------
# Unified Service Function
# -------------------------------
def vqr_turn_service(n_bits: int = 1024):
    bits = generate_vqr_bits(n_bits)
    results = run_all_tests(bits)
    return bits, results


# -------------------------------
# Gradio UI
# -------------------------------
def gradio_interface(n_bits):
    bits, results = vqr_turn_service(n_bits)
    return bits, results

with gr.Blocks() as demo:
    gr.Markdown("# 🌌 Virtual Quantum Reality (VQR) - True Uniform Random Number (TURN) Service")

    with gr.Row():
        n_bits = gr.Number(value=1024, label="Number of bits", precision=0)
        run_btn = gr.Button("Generate & Test")

    bits_output = gr.Textbox(label="Generated Bits")
    results_output = gr.JSON(label="NIST Test Results")

    run_btn.click(gradio_interface, inputs=n_bits, outputs=[bits_output, results_output])


# -------------------------------
# FastAPI REST API
# -------------------------------
app = FastAPI()

@app.get("/generate")
def generate(n_bits: int = 1024):
    bits, results = vqr_turn_service(n_bits)
    return JSONResponse({"bits": bits, "results": results})


# -------------------------------
# Entrypoint
# -------------------------------
if __name__ == "__main__":
    import sys
    if "api" in sys.argv:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        demo.launch()
