FROM pytorch/pytorch:2.10.0-cuda13.0-cudnn9-runtime 
# hire me runpod 6gb vs 13gb
#FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04

WORKDIR /app

#RUN pip install --break-system-packages --no-cache-dir uv
COPY requirements.txt .
RUN uv pip install --break-system-packages --system --no-cache-dir -r requirements.txt

COPY handler.py .
ENV MODEL_NAME=need_model
#CMD ["python", "-u", "handler.py" , "--rp_serve_api", "--rp_api_host", "0.0.0.0"]
CMD ["bash", "-c", "/bin/python -u handler.py"]
