import os
import sys

from utils import find_model_path, resolve_snapshot_path
from validate_model import validate_qwen3

print("start")

PORT = os.environ.get("PORT", "80")
model_name = os.environ.get("MODEL_NAME", "model_name_not_set")
if model_name is None:
    print("Error: MODEL_NAME environment variable not set", file=sys.stderr)
    sys.exit(1)

def start_server(model_name):
    from sglang.srt.server_args import prepare_server_args
    from sglang.launch_server import run_server
    #args = "--model Qwen/Qwen3-Coder-Next-FP8 --port 30000 --tp-size 2 --tool-call-parser qwen3_coder".split()
    args = f"--model {model_name} --host 0.0.0.0 --port {PORT} --tp-size 2 --tool-call-parser qwen3_coder".split()
    #args = f"--model {model_name} --host 0.0.0.0 --port 80 --tp-size 2 --tool-call-parser qwen3_coder --device cpu --mem-fraction-static 0.8".split()
    print(args)
    run_server(prepare_server_args(args))
    

if __name__ == "__main__":
    print(model_name)
    
    p = "unknown_path"
    try:
        print(f"{find_model_path(model_name)=}")
        p = find_model_path(model_name)
        print(validate_qwen3(p))

        p = resolve_snapshot_path(model_name)
        print(f"resolve_snapshot_path(model_name)={p}")
        print(validate_qwen3(p))
    except Exception as ex:
        print("cache model not found")
        print(ex)
#    print(f"{find_model_path(model_name)=} {resolve_snapshot_path(model_name)=}")
    start_server(model_name)


