FROM ollama/ollama:latest

# Metadata
LABEL maintainer="phoenix-sre@example.com"
LABEL description="Ollama with Gemma 3 270M on NVIDIA L4 GPU"
LABEL version="1.0.0"

# Environment Configuration
ENV OLLAMA_HOST=0.0.0.0:8080
ENV OLLAMA_MODELS=/models
ENV OLLAMA_DEBUG=false
ENV OLLAMA_KEEP_ALIVE=-1
ENV OLLAMA_NUM_PARALLEL=4
ENV OLLAMA_MAX_LOADED_MODELS=1
ENV OLLAMA_FLASH_ATTENTION=1
ENV OLLAMA_MAX_QUEUE=100

# GPU Optimization Flags
ENV CUDA_VISIBLE_DEVICES=0
ENV CUDA_LAUNCH_BLOCKING=0
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

# Model Configuration
ENV MODEL=gemma3:270m

# Install dependencies (if needed)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Pre-pull model during build (faster cold starts)
# This adds ~1GB to image but eliminates 30s cold start
RUN ollama serve & \
    sleep 5 && \
    ollama pull $MODEL && \
    pkill ollama

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/api/tags || exit 1

# Expose port
EXPOSE 8080

# Start Ollama server
ENTRYPOINT ["ollama", "serve"]
