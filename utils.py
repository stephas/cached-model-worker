print(f"utils begin")
import os

print(f"[ModelStore] Start")

MODEL_NAME = os.environ.get("MODEL_NAME", "microsoft/Phi-3-medium-128k-instruct")
HF_CACHE_ROOT = "/runpod-volume/huggingface-cache/hub"
CACHE_DIR = "/runpod-volume/huggingface-cache/hub"

# Force offline mode to use only cached models
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import os

# ugh runpod, list operations are slow...
#cached_models = os.listdir(CACHE_DIR)
#for c in cached_models:
#    print(f"[ModelStore] cached model available: {c}")

def find_model_path(model_name):
    """
    Find the path to a cached model.
    
    Args:
        model_name: The model name from Hugging Face
        (e.g., 'Qwen/Qwen2.5-0.5B-Instruct')
    
    Returns:
        The full path to the cached model, or None if not found
    """
    # Convert model name format: "Org/Model" -> "models--Org--Model"
    cache_name = model_name.replace("/", "--")
    snapshots_dir = os.path.join(CACHE_DIR, f"models--{cache_name}", "snapshots")
    
    # Check if the model exists in cache
    if os.path.exists(snapshots_dir):
        snapshots = os.listdir(snapshots_dir)
        for s in snapshots:
            print(f"[ModelStore] available: {s}")
        if snapshots:
            # Return the path to the first (usually only) snapshot
            return os.path.join(snapshots_dir, snapshots[0])
    
    return None

## Example usage
#model_path = find_model_path(MODEL_NAME) #$"Qwen/Qwen2.5-0.5B-Instruct")
#if model_path:
#    print(f"Model found at: {model_path}")
#else:
#    print("Model not found in cache")


def resolve_snapshot_path(model_id: str) -> str:
    """
    Resolve the local snapshot path for a cached model.

    Args:
        model_id: The model name from Hugging Face (e.g., 'microsoft/Phi-3-mini-4k-instruct')

    Returns:
        The full path to the cached model snapshot
    """
    if "/" not in model_id:
        raise ValueError(f"MODEL_NAME '{model_id}' is not in 'org/name' format")

    org, name = model_id.split("/", 1)
    model_root = os.path.join(HF_CACHE_ROOT, f"models--{org}--{name}")
    refs_main = os.path.join(model_root, "refs", "main")
    snapshots_dir = os.path.join(model_root, "snapshots")

    print(f"[ModelStore] MODEL_ID: {model_id}")
    print(f"[ModelStore] Model root: {model_root}")

    # Try to read the snapshot hash from refs/main
    if os.path.isfile(refs_main):
        with open(refs_main, "r") as f:
            snapshot_hash = f.read().strip()
        candidate = os.path.join(snapshots_dir, snapshot_hash)
        if os.path.isdir(candidate):
            print(f"[ModelStore] Using snapshot from refs/main: {candidate}")
            return candidate

    # Fall back to first available snapshot
    if not os.path.isdir(snapshots_dir):
        raise RuntimeError(f"[ModelStore] snapshots directory not found: {snapshots_dir}")

    versions = [
        d for d in os.listdir(snapshots_dir) if os.path.isdir(os.path.join(snapshots_dir, d))
    ]

    if not versions:
        raise RuntimeError(f"[ModelStore] No snapshot subdirectories found under {snapshots_dir}")

    versions.sort()
    chosen = os.path.join(snapshots_dir, versions[0])
    print(f"[ModelStore] Using first available snapshot: {chosen}")
    return chosen


