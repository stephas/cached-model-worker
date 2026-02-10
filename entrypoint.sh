#!/bin/bash

# Check if we have a GPU
nvidia-smi

# Spin up the latest sglang runtime
sglang --version

## Analyze the model_name if it is available for sglang to run
#if sglang --model-name $MODEL_NAME; then
#    # Take default arguments to sglang given the model_name
#    sglang --model-name $MODEL_NAME --default-args
#else
#    echo "Model $MODEL_NAME is not available for sglang to run."
#    exit 1
#fi
p=$(which python)
echo python path $p
$p --version

$p -m pip freeze | grep sg
$p -m sglang.launch_server --help

$p -u entrypoint.py
