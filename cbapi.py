from flask import Flask, request
from llama_cpp import Llama
import os

ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]


# Model inference

llm = Llama(
    model_path="./models/cbdetector_q4_k.gguf",
)

def infer_is_bait(s: str) -> bool:
    output = llm( # todo: limit prompt
        prompt=f"{s} ---",
        max_tokens=2,
        top_k=1
    )

    text = output["choices"][0]["text"]

    return text.startswith(" bait")


# Web API

app = Flask(__name__)

@app.get("/detect")
def detect():
    if "t" not in request.args or request.args.get("t") != ACCESS_TOKEN:
        return "Invalid access token t", 401

    if "q" not in request.args:
        return "Query q is required", 400
    
    query = request.args.get("q")
    if len(query) > 128:
        return "Query length must be <= 128", 400

    is_bait = infer_is_bait(query)

    return {"is_bait": is_bait}

