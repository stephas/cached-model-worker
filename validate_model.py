import os
import json
from pathlib import Path

def validate_qwen3(model_path):
    path = Path(model_path)
    files = [f.name for f in path.iterdir() if f.is_file()]
    
    # Core Requirements
    has_config = "config.json" in files
    has_tokenizer = "tokenizer.json" in files or "tokenizer_config.json" in files
    safetensors = [f for f in files if f.endswith(".safetensors")]
    ggufs = [f for f in files if f.endswith(".gguf")]
    has_index = "model.safetensors.index.json" in files
    
    print(f"--- Qwen3-Coder-Next Validation Report ---")
    print(f"Path: {path.absolute()}\n")

    # 1. vLLM & SGLang (Hugging Face Format)
    vllm_ready = has_config and has_tokenizer and (len(safetensors) > 0 or has_index)
    status_vllm = "✅ READY" if vllm_ready else "❌ MISSING FILES"
    print(f"[vLLM / SGLang] {status_vllm}")
    if not has_config: print("   - Missing: config.json")
    if not has_tokenizer: print("   - Missing: tokenizer.json")
    if not (safetensors or has_index): print("   - Missing: .safetensors weights")

    # 2. Ollama
    # Ollama is 'ready' if it has GGUF OR if it's a valid HF folder for 'ollama create'
    ollama_ready = len(ggufs) > 0 or vllm_ready
    status_ollama = "✅ READY" if ollama_ready else "❌ NOT READY"
    print(f"[Ollama] {status_ollama}")
    if len(ggufs) > 0:
        print(f"   - Found GGUF: {ggufs[0]} (Direct Run)")
    elif vllm_ready:
        print("   - Found HF weights (Can be imported via Modelfile)")

    # 3. Llama.cpp
    llama_cpp_ready = len(ggufs) > 0
    status_llama = "✅ READY" if llama_cpp_ready else "⚠️ NEEDS CONVERSION"
    print(f"[Llama.cpp] {status_llama}")
    if not llama_cpp_ready:
        print("   - No .gguf found. You must convert safetensors to GGUF first.")

    # 4. Architecture Check
    if has_config:
        with open(path / "config.json", "r") as f:
            cfg = json.load(f)
            arch = cfg.get("architectures", ["Unknown"])[0]
            model_type = cfg.get("model_type", "unknown")
            print(f"\nArchitecture: {arch} ({model_type})")
            if "qwen2" not in model_type.lower() and "qwen3" not in model_type.lower():
                print("🚨 WARNING: This doesn't look like a Qwen model.")

if __name__ == "__main__":
    validate_qwen3(".")
