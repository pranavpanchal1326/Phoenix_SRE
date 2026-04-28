#!/bin/bash

# Phoenix SRE - Quick Start Script
# Sets up local AI and runs the dashboard

echo "🔥 Phoenix SRE - Quick Start"
echo "=============================="
echo ""

# Check if Ollama is installed
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed"
    
    # Check if Ollama server is running
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✅ Ollama server is running"
    else
        echo "⚠️  Starting Ollama server..."
        ollama serve &
        sleep 3
    fi
    
    # Check if gemma:2b is available
    if ollama list | grep -q "gemma:2b"; then
        echo "✅ gemma:2b model is available"
    else
        echo "📥 Downloading gemma:2b model (this may take a few minutes)..."
        ollama pull gemma:2b
    fi
else
    echo "⚠️  Ollama not installed. Install with:"
    echo "   winget install --id=Ollama.Ollama -e"
    echo ""
    echo "Continuing without local AI (will use cloud Gemini)..."
fi

echo ""
echo "🚀 Starting Phoenix SRE Dashboard..."
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
else
    echo "📦 Creating virtual environment..."
    python -m venv venv
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
    
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Run Streamlit
streamlit run dashboard.py

echo ""
echo "👋 Phoenix SRE stopped"
