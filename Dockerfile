# Use the official SGLang image as the base (2026 latest)
#FROM lmsysorg/sglang:latest
#FROM lmsysorg/sglang:latest-runtime
# ugh 36.8 or what was it GB
#bin/python no such file it's under conda, and must install sglang still, etc base is 6gb though
#FROM pytorch/pytorch:2.8.0-cuda12.9-cudnn9-runtime 
#also needs python regs but python is in a normal usr bin path
FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04

# Set environment variables for peak performance
ENV SGLANG_CUDA_GRAPH_MAX_BATCH_SIZE=16
ENV OMP_NUM_THREADS=1
ENV FLASH_ATTENTION_FORCE_BUILD=TRUE
# Force offline mode to ensure it never tries to hit the web
ENV HF_HUB_OFFLINE=1
#ENV TRANSFORMERS_CACHE=/models
ENV PORT=80
# Ensure the tool parser for Qwen3 is ready
# it's in the sglang image already
# let's add this since we seem to need it
RUN pip install --no-cache-dir uv
#RUN uv pip install --system --no-cache-dir --upgrade "sglang[all]>=0.5.8"
RUN uv pip install --system --no-cache-dir --upgrade "sglang>=0.5.8"

#RUN python3 -m sglang.launch_server
#RUN false
WORKDIR /app
COPY entrypoint.sh .
COPY entrypoint.py .
COPY validate_model.py .
COPY utils.py .

#ENTRYPOINT ["python3", "-m", "sglang.launch_server"]
#ENTRYPOINT ["bash", "-c", "./entrypoint.sh"]
ENTRYPOINT ["/app/entrypoint.sh"]
