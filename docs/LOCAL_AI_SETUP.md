# Phoenix SRE - Local AI Setup Guide

## 🚀 Quick Start with Ollama + Gemma

Phoenix SRE now supports **local AI inference** using Ollama with Gemma models, eliminating cloud dependencies and providing faster, private AI analysis.

---

## 📦 Installation

### Step 1: Install Ollama

**Windows:**
```bash
winget install --id=Ollama.Ollama -e
```

**macOS:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Step 2: Start Ollama Server

```bash
ollama serve
```

The server will start on `http://localhost:11434`

### Step 3: Pull AI Models

**Recommended for Phoenix SRE:**

```bash
# Small, fast model (1.4GB) - Best for quick analysis
ollama pull gemma:2b

# Larger, more capable model (4.8GB) - Better quality
ollama pull gemma:7b

# Alternative: Llama 3.2 (2GB)
ollama pull llama3.2:3b
```

### Step 4: Automated Setup

Run our automated setup script:

```bash
cd "E:/Pranav Marathon/Phoenix SRE"
python scripts/setup-local-ai.py
```

This will:
- ✅ Check if Ollama is installed
- ✅ Wait for Ollama server to start
- ✅ Download recommended models
- ✅ Test model functionality

---

## 🔧 Configuration

### Update .env File

Add local AI configuration:

```bash
# Local AI Configuration
OLLAMA_URL=http://localhost:11434
OLLAMA_DEFAULT_MODEL=gemma:2b
USE_LOCAL_AI=true

# Cloud AI (fallback)
GEMINI_API_KEY=your-gemini-api-key-here
```

### Dashboard Settings

1. Open Phoenix SRE dashboard
2. Navigate to **Settings** tab
3. Select **AI Source**: Local Ollama
4. Choose model: `gemma:2b` or `gemma:7b`

---

## 🎯 Features with Local AI

### 1. **Offline Root Cause Analysis**
- No internet required
- Sub-second response time
- Complete data privacy

### 2. **Cost Savings**
- $0 per request (vs Gemini API)
- No quota limits
- Unlimited usage

### 3. **Customizable Models**
- Fine-tune on your data
- Switch models instantly
- Run multiple models

### 4. **ADK Integration**
- Advanced agent workflows
- Tracing and debugging
- Multi-step reasoning

---

## 📊 Model Comparison

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| **gemma:2b** | 1.4GB | ⚡⚡⚡ | ⭐⭐⭐ | Quick analysis, testing |
| **gemma:7b** | 4.8GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | Production, detailed analysis |
| **llama3.2:3b** | 2GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | Alternative, good balance |
| **Gemini 2.0 Flash** | Cloud | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Cloud fallback, FREE |

---

## 🧪 Testing Local AI

### Test 1: Simple Completion

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gemma:2b",
  "prompt": "What is GPU monitoring?",
  "stream": false
}'
```

### Test 2: Chat Completion

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "gemma:2b",
  "messages": [
    {
      "role": "user",
      "content": "Explain GPU utilization spike"
    }
  ],
  "stream": false
}'
```

### Test 3: Python Integration

```python
from utils.cloud_run_api import CloudRunAPI

# Initialize client
client = CloudRunAPI()

# Check available models
models = client.get_available_models()
print(f"Available models: {models}")

# Generate completion
result = client.generate_completion(
    prompt="Analyze GPU utilization at 95%",
    model="gemma:2b"
)

print(f"Response: {result['text']}")
print(f"Latency: {result['latency_ms']}ms")
```

---

## 🔄 Hybrid AI Strategy

Phoenix SRE uses a **multi-tier AI strategy**:

```
1. Local Ollama (gemma:2b)     ← Primary (fastest, free)
   ↓ (if unavailable)
2. Local Ollama (gemma:7b)     ← Better quality
   ↓ (if unavailable)
3. Gemini 2.0 Flash (cloud)    ← Cloud fallback (FREE)
   ↓ (if unavailable)
4. Gemini 1.5 Pro (cloud)      ← Premium analysis
   ↓ (if unavailable)
5. Rules-based engine          ← Always works
```

**Benefits:**
- ✅ Never fails (graceful degradation)
- ✅ Optimizes for speed and cost
- ✅ Works offline and online
- ✅ Automatic failover

---

## 🎮 ADK Agent Workflows

### What is ADK?

**ADK (Advanced Development Kit)** provides:
- 🔍 **Tracing**: Track multi-step agent workflows
- 📊 **Debugging**: Visualize agent decision-making
- 🔄 **Orchestration**: Coordinate complex tasks
- 📝 **Logging**: Comprehensive audit trails

### Using ADK with Phoenix SRE

```python
from utils.cloud_run_api import ADKAgentClient

# Initialize ADK client
adk = ADKAgentClient()

# Create session
session_id = adk.create_session(metadata={
    "user": "sre-team",
    "environment": "production"
})

# Trace workflow
adk.trace_workflow(
    workflow_name="incident_analysis",
    steps=[
        {"step": "detect_anomaly", "status": "complete"},
        {"step": "ai_diagnosis", "status": "complete"},
        {"step": "human_approval", "status": "pending"}
    ]
)
```

### ADK Dashboard Integration

1. Navigate to **AI Diagnosis** tab
2. Enable **ADK Tracing**
3. View workflow history
4. Export traces for analysis

---

## 💡 Advanced Usage

### Custom Model Fine-Tuning

```bash
# Create Modelfile
cat > Modelfile << EOF
FROM gemma:2b
SYSTEM You are an expert SRE analyzing GPU workloads.
PARAMETER temperature 0.7
PARAMETER top_p 0.9
EOF

# Create custom model
ollama create phoenix-sre-gemma -f Modelfile

# Use in dashboard
# Settings → AI Source → Custom Model → phoenix-sre-gemma
```

### Multi-Model Ensemble

```python
# Use multiple models for consensus
models = ["gemma:2b", "gemma:7b", "llama3.2:3b"]
results = []

for model in models:
    result = client.generate_completion(
        prompt="Analyze GPU spike",
        model=model
    )
    results.append(result)

# Aggregate results
consensus = aggregate_ai_responses(results)
```

### Streaming Responses

```python
import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "gemma:2b",
        "prompt": "Explain GPU monitoring",
        "stream": True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        data = json.loads(line)
        print(data.get('response', ''), end='', flush=True)
```

---

## 🐛 Troubleshooting

### Issue: Ollama server not starting

**Solution:**
```bash
# Check if already running
ps aux | grep ollama

# Kill existing process
pkill ollama

# Restart
ollama serve
```

### Issue: Model download fails

**Solution:**
```bash
# Check disk space
df -h

# Clear Ollama cache
rm -rf ~/.ollama/models/*

# Re-pull model
ollama pull gemma:2b
```

### Issue: Slow inference

**Solutions:**
1. Use smaller model (`gemma:2b` instead of `gemma:7b`)
2. Reduce `max_tokens` parameter
3. Enable GPU acceleration (if available)
4. Increase system RAM allocation

### Issue: Out of memory

**Solution:**
```bash
# Unload models
ollama rm gemma:7b

# Use smaller model
ollama pull gemma:2b

# Check loaded models
ollama ps
```

---

## 📈 Performance Benchmarks

### Local Ollama (gemma:2b)
- **Latency**: 200-500ms
- **Throughput**: 20-50 tokens/sec
- **Cost**: $0
- **Privacy**: 100% local

### Local Ollama (gemma:7b)
- **Latency**: 500-1500ms
- **Throughput**: 10-30 tokens/sec
- **Cost**: $0
- **Quality**: ⭐⭐⭐⭐⭐

### Gemini 2.0 Flash (cloud)
- **Latency**: 800-1200ms
- **Throughput**: 50-100 tokens/sec
- **Cost**: $0 (FREE)
- **Quality**: ⭐⭐⭐⭐⭐

---

## 🎯 Best Practices

### 1. **Model Selection**
- Use `gemma:2b` for real-time analysis (<500ms)
- Use `gemma:7b` for detailed reports
- Use Gemini Flash for cloud fallback

### 2. **Prompt Engineering**
- Be specific and concise
- Include context (metrics, thresholds)
- Request structured output

### 3. **Resource Management**
- Unload unused models
- Monitor system RAM
- Use streaming for long responses

### 4. **Hybrid Strategy**
- Always configure cloud fallback
- Test failover scenarios
- Monitor AI source metrics

---

## 🚀 Next Steps

1. **Install Ollama**: `winget install Ollama.Ollama`
2. **Download Models**: `ollama pull gemma:2b`
3. **Run Setup**: `python scripts/setup-local-ai.py`
4. **Test Integration**: Open dashboard → AI Diagnosis
5. **Configure Hybrid**: Enable both local and cloud AI

---

## 📚 Resources

- **Ollama Docs**: https://ollama.com/docs
- **Gemma Models**: https://ollama.com/library/gemma
- **ADK Guide**: https://github.com/google/adk
- **Phoenix SRE**: See `docs/ARCHITECTURE.md`

---

**Built with ❤️ for BNB Marathon 2025**

**Status**: ✅ Local AI Ready  
**Models**: Ollama + Gemma + Llama  
**Cost**: $0 per request
