"""
Cloud Run API Client - Real integration with production services
Connects to ADK Agent and Ollama+Gemma GPU services
"""

import os
import requests
from typing import Dict, Optional, List
from datetime import datetime
import json


class CloudRunAPI:
    """
    Client for interacting with Cloud Run services
    Supports both ADK Agent and Ollama+Gemma backends
    """
    
    def __init__(
        self,
        adk_url: Optional[str] = None,
        gemma_url: Optional[str] = None,
        local_ollama_url: str = "http://localhost:11434"
    ):
        """
        Initialize Cloud Run API client
        
        Args:
            adk_url: Production ADK Agent URL
            gemma_url: Production Gemma GPU URL
            local_ollama_url: Local Ollama server URL
        """
        self.adk_url = adk_url or os.getenv("ADK_AGENT_URL", "")
        self.gemma_url = gemma_url or os.getenv("GEMMA_GPU_URL", "")
        self.local_ollama_url = local_ollama_url
        
        # Try local Ollama first, then cloud services
        self.use_local = self._check_local_ollama()
        
    def _check_local_ollama(self) -> bool:
        """Check if local Ollama server is running"""
        try:
            response = requests.get(f"{self.local_ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def get_available_models(self) -> List[Dict]:
        """
        Get list of available models
        
        Returns:
            List of model information
        """
        models = []
        
        # Check local Ollama models
        if self.use_local:
            try:
                response = requests.get(f"{self.local_ollama_url}/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    for model in data.get('models', []):
                        models.append({
                            'name': model['name'],
                            'size': model.get('size', 0),
                            'modified': model.get('modified_at', ''),
                            'source': 'local_ollama'
                        })
            except Exception as e:
                print(f"Error fetching local models: {e}")
        
        # Add cloud models if available
        if self.gemma_url:
            models.append({
                'name': 'gemma3-270m',
                'size': 270_000_000,
                'source': 'cloud_run_gpu'
            })
        
        return models
    
    def generate_completion(
        self,
        prompt: str,
        model: str = "gemma:2b",
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> Dict:
        """
        Generate text completion using available models
        
        Args:
            prompt: Input prompt
            model: Model name to use
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Completion response with text and metadata
        """
        start_time = datetime.now()
        
        # Try local Ollama first
        if self.use_local:
            try:
                response = requests.post(
                    f"{self.local_ollama_url}/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": temperature,
                            "num_predict": max_tokens
                        }
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    elapsed = (datetime.now() - start_time).total_seconds()
                    
                    return {
                        'text': data.get('response', ''),
                        'model': model,
                        'source': 'local_ollama',
                        'latency_ms': int(elapsed * 1000),
                        'tokens': data.get('eval_count', 0),
                        'success': True
                    }
            except Exception as e:
                print(f"Local Ollama failed: {e}")
        
        # Fallback to cloud Gemma if available
        if self.gemma_url:
            try:
                response = requests.post(
                    f"{self.gemma_url}/v1/completions",
                    json={
                        "prompt": prompt,
                        "max_tokens": max_tokens,
                        "temperature": temperature
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    elapsed = (datetime.now() - start_time).total_seconds()
                    
                    return {
                        'text': data.get('choices', [{}])[0].get('text', ''),
                        'model': 'gemma3-270m',
                        'source': 'cloud_run_gpu',
                        'latency_ms': int(elapsed * 1000),
                        'success': True
                    }
            except Exception as e:
                print(f"Cloud Gemma failed: {e}")
        
        # Fallback response
        return {
            'text': 'No AI models available. Please start Ollama or configure cloud services.',
            'model': 'fallback',
            'source': 'error',
            'success': False
        }
    
    def get_service_metrics(self, service_name: str = "ollama") -> Dict:
        """
        Get metrics from a service
        
        Args:
            service_name: Name of service to query
            
        Returns:
            Service metrics
        """
        if service_name == "ollama" and self.use_local:
            try:
                # Get running models
                response = requests.get(f"{self.local_ollama_url}/api/ps")
                if response.status_code == 200:
                    data = response.json()
                    
                    return {
                        'service': 'ollama',
                        'status': 'running',
                        'models_loaded': len(data.get('models', [])),
                        'endpoint': self.local_ollama_url,
                        'timestamp': datetime.now().isoformat()
                    }
            except:
                pass
        
        return {
            'service': service_name,
            'status': 'unavailable',
            'timestamp': datetime.now().isoformat()
        }
    
    def pull_model(self, model_name: str = "gemma:2b") -> Dict:
        """
        Pull a model from Ollama registry
        
        Args:
            model_name: Name of model to pull
            
        Returns:
            Pull status
        """
        if not self.use_local:
            return {
                'success': False,
                'message': 'Local Ollama not available'
            }
        
        try:
            # Start pull (this is async in Ollama)
            response = requests.post(
                f"{self.local_ollama_url}/api/pull",
                json={"name": model_name},
                stream=True,
                timeout=300
            )
            
            if response.status_code == 200:
                # Stream progress
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        status = data.get('status', '')
                        print(f"Pull progress: {status}")
                        
                        if 'error' in data:
                            return {
                                'success': False,
                                'message': data['error']
                            }
                
                return {
                    'success': True,
                    'message': f'Successfully pulled {model_name}'
                }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def chat_completion(
        self,
        messages: List[Dict],
        model: str = "gemma:2b",
        temperature: float = 0.7
    ) -> Dict:
        """
        Chat completion with conversation history
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name
            temperature: Sampling temperature
            
        Returns:
            Chat response
        """
        if not self.use_local:
            return {
                'success': False,
                'message': 'Local Ollama not available'
            }
        
        try:
            response = requests.post(
                f"{self.local_ollama_url}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": temperature
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                return {
                    'success': True,
                    'message': data.get('message', {}),
                    'model': model,
                    'source': 'local_ollama'
                }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }


class ADKAgentClient:
    """
    Client for ADK (Advanced Development Kit) Agent workflows
    Provides tracing, workflow management, and advanced agent capabilities
    """
    
    def __init__(self, adk_url: Optional[str] = None):
        """
        Initialize ADK Agent client
        
        Args:
            adk_url: ADK Agent service URL
        """
        self.adk_url = adk_url or os.getenv("ADK_AGENT_URL", "")
        self.session_id = None
        
    def create_session(self, metadata: Optional[Dict] = None) -> str:
        """
        Create a new ADK session for workflow tracking
        
        Args:
            metadata: Optional session metadata
            
        Returns:
            Session ID
        """
        if not self.adk_url:
            # Local session ID
            self.session_id = f"local-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            return self.session_id
        
        try:
            response = requests.post(
                f"{self.adk_url}/api/sessions",
                json={"metadata": metadata or {}}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.session_id = data.get('session_id')
                return self.session_id
        except Exception as e:
            print(f"ADK session creation failed: {e}")
            self.session_id = f"local-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            return self.session_id
    
    def trace_workflow(
        self,
        workflow_name: str,
        steps: List[Dict],
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Trace an agent workflow with detailed steps
        
        Args:
            workflow_name: Name of the workflow
            steps: List of workflow steps
            metadata: Optional metadata
            
        Returns:
            Trace result
        """
        trace_data = {
            'session_id': self.session_id or self.create_session(),
            'workflow_name': workflow_name,
            'steps': steps,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat()
        }
        
        if not self.adk_url:
            # Local tracing (just log)
            print(f"[ADK Trace] {workflow_name}: {len(steps)} steps")
            return {
                'success': True,
                'trace_id': f"trace-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'source': 'local'
            }
        
        try:
            response = requests.post(
                f"{self.adk_url}/api/traces",
                json=trace_data
            )
            
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"ADK tracing failed: {e}")
        
        return {
            'success': False,
            'message': 'Tracing unavailable'
        }
    
    def get_workflow_history(self, limit: int = 10) -> List[Dict]:
        """
        Get workflow execution history
        
        Args:
            limit: Maximum number of workflows to return
            
        Returns:
            List of workflow executions
        """
        if not self.adk_url:
            return []
        
        try:
            response = requests.get(
                f"{self.adk_url}/api/workflows",
                params={'limit': limit}
            )
            
            if response.status_code == 200:
                return response.json().get('workflows', [])
        except Exception as e:
            print(f"Failed to get workflow history: {e}")
        
        return []
