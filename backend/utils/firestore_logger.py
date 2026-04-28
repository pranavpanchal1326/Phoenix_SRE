"""
Firestore Logger - Database operations for incident tracking
Handles all Firestore interactions with graceful fallbacks
"""

from google.cloud import firestore
from datetime import datetime
from typing import Dict, List, Optional
import os


class FirestoreLogger:
    """
    Firestore database operations for Phoenix SRE
    Falls back to in-memory storage if Firestore unavailable
    """
    
    def __init__(self, project_id: Optional[str] = None):
        """
        Initialize Firestore client
        
        Args:
            project_id: GCP project ID (defaults to env variable)
        """
        self.project_id = project_id or os.getenv("GCP_PROJECT")
        self.use_firestore = False
        self.in_memory_store = {
            "incidents": [],
            "scaling_events": [],
            "metrics_snapshots": [],
        }
        
        try:
            if self.project_id:
                self.db = firestore.Client(project=self.project_id)
                self.use_firestore = True
            else:
                print("⚠️ Firestore not configured, using in-memory storage")
        except Exception as e:
            print(f"⚠️ Firestore initialization failed: {e}. Using in-memory storage.")
            self.use_firestore = False
    
    def log_incident(self, incident_data: Dict) -> str:
        """
        Log incident to Firestore
        
        Args:
            incident_data: Complete incident object
            
        Returns:
            Document ID
        """
        incident_data['logged_at'] = datetime.now().isoformat()
        
        if self.use_firestore:
            try:
                doc_ref = self.db.collection('incidents').document(incident_data['trace_id'])
                doc_ref.set(incident_data)
                return incident_data['trace_id']
            except Exception as e:
                print(f"Firestore write failed: {e}")
                return self._log_to_memory('incidents', incident_data)
        else:
            return self._log_to_memory('incidents', incident_data)
    
    def log_scaling_event(self, event_data: Dict) -> str:
        """
        Log scaling event to Firestore
        
        Args:
            event_data: Scaling event details
            
        Returns:
            Document ID
        """
        event_data['timestamp'] = datetime.now().isoformat()
        event_id = f"scale-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        if self.use_firestore:
            try:
                doc_ref = self.db.collection('scaling_events').document(event_id)
                doc_ref.set(event_data)
                return event_id
            except Exception as e:
                print(f"Firestore write failed: {e}")
                return self._log_to_memory('scaling_events', event_data)
        else:
            return self._log_to_memory('scaling_events', event_data)
    
    def log_metrics_snapshot(self, metrics: Dict) -> str:
        """
        Log metrics snapshot to Firestore
        
        Args:
            metrics: Current metrics
            
        Returns:
            Document ID
        """
        snapshot_id = f"metrics-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        metrics['snapshot_id'] = snapshot_id
        metrics['timestamp'] = datetime.now().isoformat()
        
        if self.use_firestore:
            try:
                doc_ref = self.db.collection('metrics_snapshots').document(snapshot_id)
                doc_ref.set(metrics)
                return snapshot_id
            except Exception as e:
                print(f"Firestore write failed: {e}")
                return self._log_to_memory('metrics_snapshots', metrics)
        else:
            return self._log_to_memory('metrics_snapshots', metrics)
    
    def get_recent_incidents(self, limit: int = 10) -> List[Dict]:
        """
        Get recent incidents from Firestore
        
        Args:
            limit: Maximum number of incidents to return
            
        Returns:
            List of incident objects
        """
        if self.use_firestore:
            try:
                docs = (
                    self.db.collection('incidents')
                    .order_by('logged_at', direction=firestore.Query.DESCENDING)
                    .limit(limit)
                    .stream()
                )
                return [doc.to_dict() for doc in docs]
            except Exception as e:
                print(f"Firestore read failed: {e}")
                return self._get_from_memory('incidents', limit)
        else:
            return self._get_from_memory('incidents', limit)
    
    def get_incident_by_id(self, trace_id: str) -> Optional[Dict]:
        """
        Get specific incident by trace ID
        
        Args:
            trace_id: Incident trace ID
            
        Returns:
            Incident object or None
        """
        if self.use_firestore:
            try:
                doc = self.db.collection('incidents').document(trace_id).get()
                return doc.to_dict() if doc.exists else None
            except Exception as e:
                print(f"Firestore read failed: {e}")
                return self._find_in_memory('incidents', 'trace_id', trace_id)
        else:
            return self._find_in_memory('incidents', 'trace_id', trace_id)
    
    def get_scaling_events(self, limit: int = 20) -> List[Dict]:
        """Get recent scaling events"""
        if self.use_firestore:
            try:
                docs = (
                    self.db.collection('scaling_events')
                    .order_by('timestamp', direction=firestore.Query.DESCENDING)
                    .limit(limit)
                    .stream()
                )
                return [doc.to_dict() for doc in docs]
            except Exception as e:
                print(f"Firestore read failed: {e}")
                return self._get_from_memory('scaling_events', limit)
        else:
            return self._get_from_memory('scaling_events', limit)
    
    def _log_to_memory(self, collection: str, data: Dict) -> str:
        """Fallback: Store in memory"""
        self.in_memory_store[collection].append(data)
        return data.get('trace_id') or data.get('snapshot_id') or f"mem-{len(self.in_memory_store[collection])}"
    
    def _get_from_memory(self, collection: str, limit: int) -> List[Dict]:
        """Fallback: Retrieve from memory"""
        items = self.in_memory_store.get(collection, [])
        return sorted(items, key=lambda x: x.get('logged_at') or x.get('timestamp') or '', reverse=True)[:limit]
    
    def _find_in_memory(self, collection: str, key: str, value: str) -> Optional[Dict]:
        """Fallback: Find in memory"""
        items = self.in_memory_store.get(collection, [])
        for item in items:
            if item.get(key) == value:
                return item
        return None
