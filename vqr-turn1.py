# file: vqr_turn_service.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import uvicorn
import threading
import gradio as gr

from vqr_turn_rng import VQRTurnRNG

# --- RNG instance ---
rng = VQRTurnRNG(reseed_interval_bytes=1 << 20)

# --- FastAPI app ---
app = FastAPI(title="VQR/TURN RNG Service")

# Allow cross-origin for easy integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

class BytesRequest(BaseModel):
    n: int

@app.get("/random/float")
def random_float():
    return {"value": rng.random()}

@app.get("/random/u64")
def random_u64():
    return {"value": rng.random_u64()}

@app.post("/random/bytes")
def random_bytes(req: BytesRequest):
    b = rng.random_bytes(req.n)
    return {"value_b64": base64.b64encode(b).decode()}

# --- JSON-RPC endpoint ---
@app.post("/jsonrpc")
def jsonrpc(req: dict):
    method = req.get("method")
    params = req.get("params", {})
    id_ = req.get("id")
    result = None

    if method == "random_float":
        result = rng.random()
    elif method == "random_u64":
        result = rng.random_u64()
    elif method == "random_bytes":
        n = params.get("n", 32)
        result = base64.b64encode(rng.random_bytes(n)).decode()
    else:
        return {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": id_}

    return {"jsonrpc": "2.0", "result": result, "id": id_}


# --- Gradio UI ---
def get_float():
    return rng.random()

def get_u64():
    return rng.random_u64()

def get_bytes(n):
    b = rng.random_bytes(n)
    return base64.b64encode(b).decode()

def launch_gradio():
    with gr.Blocks() as demo:
        gr.Markdown("## 🎲 VQR/TURN RNG Demo")

        with gr.Tab("Random Float"):
            btn = gr.Button("Generate")
            out = gr.Number()
            btn.click(get_float, None, out)

        with gr.Tab("Random U64"):
            btn2 = gr.Button("Generate")
            out2 = gr.Textbox()
            btn2.click(get_u64, None, out2)

        with gr.Tab("Random Bytes"):
            n_in = gr.Slider(1, 256, value=32, step=1, label="Length (bytes)")
            btn3 = gr.Button("Generate")
            out3 = gr.Textbox(label="Base64")
            btn3.click(get_bytes, n_in, out3)

    # Run Gradio on a different port
    demo.launch(server_port=7860, share=False)


# --- Main entry ---
if __name__ == "__main__":
    # Run Gradio in background thread
    threading.Thread(target=launch_gradio, daemon=True).start()
    # Run FastAPI (REST + JSON-RPC)
    uvicorn.run(app, host="0.0.0.0", port=8000)

