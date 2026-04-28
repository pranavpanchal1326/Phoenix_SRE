"""
Setup script for local AI infrastructure
Installs Ollama and downloads recommended models
"""

import subprocess
import sys
import time
import requests


def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def install_ollama():
    """Install Ollama on Windows"""
    print("📦 Installing Ollama...")
    print("Please run: winget install --id=Ollama.Ollama -e")
    print("Or download from: https://ollama.com/download")
    

def wait_for_ollama():
    """Wait for Ollama server to start"""
    print("⏳ Waiting for Ollama server to start...")
    max_attempts = 30
    
    for i in range(max_attempts):
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                print("✅ Ollama server is running!")
                return True
        except:
            pass
        
        time.sleep(1)
        if i % 5 == 0:
            print(f"  Still waiting... ({i}/{max_attempts})")
    
    print("❌ Ollama server did not start. Please start it manually:")
    print("   Run: ollama serve")
    return False


def pull_model(model_name):
    """Pull a model from Ollama registry"""
    print(f"📥 Pulling model: {model_name}")
    
    try:
        result = subprocess.run(
            ['ollama', 'pull', model_name],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ Successfully pulled {model_name}")
            return True
        else:
            print(f"❌ Failed to pull {model_name}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error pulling {model_name}: {e}")
        return False


def test_model(model_name):
    """Test a model with a simple prompt"""
    print(f"🧪 Testing {model_name}...")
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": "What is GPU monitoring? Answer in one sentence.",
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get('response', '')
            print(f"✅ Model works! Response: {answer[:100]}...")
            return True
        else:
            print(f"❌ Model test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing model: {e}")
        return False


def main():
    """Main setup routine"""
    print("=" * 60)
    print("🔥 Phoenix SRE - Local AI Infrastructure Setup")
    print("=" * 60)
    print()
    
    # Check if Ollama is installed
    if not check_ollama_installed():
        print("❌ Ollama is not installed")
        install_ollama()
        print("\n⚠️ Please install Ollama and run this script again")
        return
    
    print("✅ Ollama is installed")
    print()
    
    # Wait for Ollama server
    if not wait_for_ollama():
        print("\n⚠️ Please start Ollama server manually:")
        print("   Run: ollama serve")
        print("   Then run this script again")
        return
    
    print()
    
    # Recommended models
    models = [
        ("gemma:2b", "Small, fast model (1.4GB) - Recommended for testing"),
        ("gemma:7b", "Larger, more capable model (4.8GB)"),
        ("llama3.2:3b", "Alternative small model (2GB)"),
    ]
    
    print("📋 Recommended Models:")
    for i, (model, desc) in enumerate(models, 1):
        print(f"  {i}. {model} - {desc}")
    
    print()
    print("Select models to install (comma-separated, e.g., 1,2 or 'all'):")
    selection = input("> ").strip().lower()
    
    if selection == 'all':
        selected_models = [m[0] for m in models]
    else:
        try:
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            selected_models = [models[i][0] for i in indices if 0 <= i < len(models)]
        except:
            print("❌ Invalid selection. Installing default model (gemma:2b)")
            selected_models = ["gemma:2b"]
    
    print()
    print(f"📥 Installing {len(selected_models)} model(s)...")
    print()
    
    # Pull selected models
    success_count = 0
    for model in selected_models:
        if pull_model(model):
            success_count += 1
            print()
    
    print()
    print("=" * 60)
    print(f"✅ Setup complete! {success_count}/{len(selected_models)} models installed")
    print("=" * 60)
    print()
    
    # Test first model
    if selected_models and success_count > 0:
        print("🧪 Testing first model...")
        test_model(selected_models[0])
    
    print()
    print("🎉 Local AI infrastructure is ready!")
    print()
    print("Next steps:")
    print("  1. Run: streamlit run dashboard.py")
    print("  2. Navigate to AI Diagnosis tab")
    print("  3. Select 'Local Ollama' as AI source")
    print()


if __name__ == "__main__":
    main()
