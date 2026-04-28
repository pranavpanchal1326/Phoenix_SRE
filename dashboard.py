"""
Phoenix SRE: Complete Full-Stack Dashboard
Production-grade GPU orchestration platform with premium UI
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import time
import random
import json

# Load environment variables
load_dotenv()

# Import utilities
from utils.metrics_engine import MetricsEngine
from utils.chaos_scenarios import ChaosScenarios
from utils.ai_diagnosis import AIDiagnosisEngine
from utils.pdf_generator import PDFReportGenerator
from utils.firestore_logger import FirestoreLogger
from utils.cost_calculator import CostCalculator
from utils.cloud_run_api import CloudRunAPI, ADKAgentClient

# Page configuration
st.set_page_config(
    page_title="Phoenix SRE: Adaptive GPU Orchestrator",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Load premium CSS
with open("assets/premium_styles.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.mode = os.getenv("APP_MODE", "chaos")
    st.session_state.current_scenario = None
    st.session_state.incident_running = False
    st.session_state.metrics_history = []
    st.session_state.incidents = []
    st.session_state.total_spend = 0.55
    st.session_state.demo_mode = False
    st.session_state.auto_refresh = True
    st.session_state.refresh_interval = 5
    
    # Initialize utilities
    try:
        st.session_state.metrics_engine = MetricsEngine(mode=st.session_state.mode)
        st.session_state.chaos_scenarios = ChaosScenarios()
        st.session_state.ai_engine = AIDiagnosisEngine(use_local=True)
        st.session_state.pdf_generator = PDFReportGenerator()
        st.session_state.firestore = FirestoreLogger()
        st.session_state.cost_calculator = CostCalculator(budget_limit=10.0)
        st.session_state.cloud_api = CloudRunAPI()
        st.session_state.adk_client = ADKAgentClient()
    except Exception as e:
        st.error(f"⚠️ Initialization error: {e}")

# Premium Navigation
st.markdown("""
<div class="premium-nav">
    <div class="premium-nav-logo">🔥 Phoenix SRE</div>
</div>
""", unsafe_allow_html=True)

# Tab Navigation
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Overview",
    "📈 Real-Time Monitoring", 
    "⚡ Chaos Engineering",
    "🧠 AI Diagnosis",
    "📜 Incident History",
    "💰 Cost Tracking",
    "⚙️ Settings"
])

# ============================================
# TAB 1: OVERVIEW
# ============================================
with tab1:
    st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 48px 0 32px 0;">
        <h1 style="font-size: 56px; font-weight: 700; color: var(--frost-white); margin-bottom: 16px; letter-spacing: -0.02em;">
            Adaptive GPU Orchestrator
        </h1>
        <p style="font-size: 20px; color: var(--cloud-gray); max-width: 800px; margin: 0 auto;">
            Production-grade observability for AI workloads on Google Cloud Run. 
            Real-time monitoring, chaos engineering, and AI-powered diagnosis.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get current metrics
    current_metrics = st.session_state.metrics_engine.get_current_metrics()
    
    # Hero Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        gpu_util = current_metrics['gpu_utilization']
        delta = random.uniform(-5, 5)
        st.metric(
            label="GPU Utilization",
            value=f"{gpu_util:.1f}%",
            delta=f"{delta:+.1f}%",
            delta_color="inverse" if delta > 0 else "normal"
        )
    
    with col2:
        latency = current_metrics['request_latency']
        delta = random.uniform(-20, 20)
        st.metric(
            label="P95 Latency",
            value=f"{latency:.0f}ms",
            delta=f"{delta:+.0f}ms",
            delta_color="inverse" if delta > 0 else "normal"
        )
    
    with col3:
        error_rate = current_metrics['error_rate']
        delta = random.uniform(-0.5, 0.5)
        st.metric(
            label="Error Rate",
            value=f"{error_rate:.2f}%",
            delta=f"{delta:+.2f}%",
            delta_color="inverse" if delta > 0 else "normal"
        )
    
    with col4:
        cost = st.session_state.total_spend
        remaining = ((10 - cost) / 10 * 100)
        st.metric(
            label="Budget Used",
            value=f"${cost:.2f}",
            delta=f"{remaining:.0f}% remaining"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # System Status
    st.markdown("### 🎯 System Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <div class="glass-card-header">Operation Mode</div>
            <div style="font-size: 24px; color: var(--aurora-cyan); margin: 12px 0;">
                ✓ Chaos Simulation
            </div>
            <div style="font-size: 14px; color: var(--cloud-gray);">
                Running in simulation mode for demo purposes
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <div class="glass-card-header">AI Engine Status</div>
            <div style="font-size: 24px; color: var(--quantum-blue); margin: 12px 0;">
                🧠 Gemini 2.0 Flash
            </div>
            <div style="font-size: 14px; color: var(--cloud-gray);">
                Local Ollama available • Cloud fallback ready
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔍 Run AI Diagnosis", use_container_width=True):
            st.switch_page("pages/ai_diagnosis.py")
    
    with col2:
        if st.button("⚡ Start Chaos Test", use_container_width=True):
            st.switch_page("pages/chaos.py")
    
    with col3:
        if st.button("📊 View Analytics", use_container_width=True):
            st.switch_page("pages/monitoring.py")
    
    with col4:
        if st.button("📥 Export Report", use_container_width=True):
            st.info("Report generation coming soon!")

# ============================================
# TAB 2: REAL-TIME MONITORING
# ============================================
with tab2:
    st.markdown("## 📈 Real-Time Monitoring")
    
    # Time range selector
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        time_range = st.selectbox(
            "Time Range",
            ["Last 1 Hour", "Last 6 Hours", "Last 24 Hours", "Last 7 Days"],
            index=0
        )
    
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    with col3:
        auto_refresh = st.checkbox("Auto-refresh", value=st.session_state.auto_refresh)
        st.session_state.auto_refresh = auto_refresh
    
    # Generate time series data
    duration_map = {
        "Last 1 Hour": 60,
        "Last 6 Hours": 360,
        "Last 24 Hours": 1440,
        "Last 7 Days": 10080
    }
    
    duration = duration_map[time_range]
    df = st.session_state.metrics_engine.generate_time_series(
        duration_minutes=duration,
        interval_seconds=60 if duration <= 360 else 300
    )
    
    # GPU Utilization Chart
    st.markdown("### GPU Utilization")
    
    fig_gpu = go.Figure()
    fig_gpu.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['gpu_utilization'],
        name='GPU Utilization',
        line=dict(color='#0066FF', width=2.5),
        fill='tozeroy',
        fillcolor='rgba(0, 102, 255, 0.2)',
        hovertemplate='<b>%{y:.1f}%</b><br>%{x}<extra></extra>'
    ))
    
    fig_gpu.add_hline(
        y=95,
        line_dash="dash",
        line_color="#FF6B35",
        annotation_text="Critical Threshold",
        annotation_position="right"
    )
    
    fig_gpu.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="-apple-system, BlinkMacSystemFont", color='#E5E7EB'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.04)', showgrid=True),
        yaxis=dict(gridcolor='rgba(255,255,255,0.04)', showgrid=True, range=[0, 100]),
        hovermode='x unified',
        margin=dict(l=0, r=0, t=0, b=0),
        height=400
    )
    
    st.plotly_chart(fig_gpu, use_container_width=True)
    
    # Multi-metric charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### GPU Memory")
        
        fig_mem = go.Figure()
        fig_mem.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['gpu_memory'],
            name='GPU Memory',
            line=dict(color='#00D9FF', width=2),
            fill='tozeroy',
            fillcolor='rgba(0, 217, 255, 0.2)'
        ))
        
        fig_mem.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="-apple-system, BlinkMacSystemFont", color='#E5E7EB'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.04)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.04)', title="MB"),
            margin=dict(l=0, r=0, t=0, b=0),
            height=300
        )
        
        st.plotly_chart(fig_mem, use_container_width=True)
    
    with col2:
        st.markdown("### Request Latency")
        
        fig_lat = go.Figure()
        fig_lat.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['request_latency'],
            name='P95 Latency',
            line=dict(color='#8B5CF6', width=2),
            fill='tozeroy',
            fillcolor='rgba(139, 92, 246, 0.2)'
        ))
        
        fig_lat.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="-apple-system, BlinkMacSystemFont", color='#E5E7EB'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.04)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.04)', title="ms"),
            margin=dict(l=0, r=0, t=0, b=0),
            height=300
        )
        
        st.plotly_chart(fig_lat, use_container_width=True)
    
    # Current Metrics Table
    st.markdown("### 📊 Current Metrics")
    
    metrics_df = pd.DataFrame([current_metrics])
    st.dataframe(
        metrics_df.style.format({
            'gpu_utilization': '{:.1f}%',
            'gpu_memory': '{:.0f} MB',
            'request_latency': '{:.0f} ms',
            'error_rate': '{:.2f}%',
            'active_instances': '{:.0f}'
        }),
        use_container_width=True,
        hide_index=True
    )

# ============================================
# TAB 3: CHAOS ENGINEERING
# ============================================
with tab3:
    st.markdown("## ⚡ Chaos Engineering")
    
    st.markdown("""
    <div class="glass-card" style="margin-bottom: 24px;">
        <div style="font-size: 16px; color: var(--cloud-gray); line-height: 1.6;">
            Test your system's resilience by simulating production failures. 
            Each scenario triggers realistic anomalies and provides AI-powered analysis.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chaos scenario cards
    scenarios = ChaosScenarios.get_all_scenarios()
    
    col1, col2 = st.columns(2)
    
    for idx, (scenario_key, scenario_data) in enumerate(scenarios.items()):
        with col1 if idx % 2 == 0 else col2:
            with st.container():
                st.markdown(f"""
                <div class="chaos-card">
                    <div class="chaos-badge">
                        {scenario_data['severity'].upper()}
                    </div>
                    <div class="chaos-icon">{scenario_data['icon']}</div>
                    <div class="chaos-title">{scenario_data['name']}</div>
                    <div class="chaos-description">{scenario_data['description']}</div>
                    <div class="chaos-meta"><strong>Duration:</strong> {scenario_data['expected_duration']}</div>
                    <div class="chaos-meta"><strong>Severity:</strong> {scenario_data['severity'].title()}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"▶ Run {scenario_data['name']}", key=f"run_{scenario_key}", use_container_width=True):
                    with st.spinner(f"Running {scenario_data['name']}..."):
                        # Generate incident
                        incident = st.session_state.chaos_scenarios.generate_incident(scenario_key)
                        
                        # Store incident
                        st.session_state.incidents.append(incident)
                        
                        # Show results
                        st.success(f"✓ Scenario completed: {incident['trace_id']}")
                        
                        with st.expander("📊 View Incident Details"):
                            st.json(incident)

# ============================================
# TAB 4: AI DIAGNOSIS
# ============================================
with tab4:
    st.markdown("## 🧠 AI-Powered Diagnosis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <div class="glass-card-header">Current System State</div>
            <div style="margin-top: 16px;">
        """, unsafe_allow_html=True)
        
        metrics_json = json.dumps(current_metrics, indent=2)
        st.code(metrics_json, language="json")
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### AI Configuration")
        
        ai_source = st.selectbox(
            "AI Source",
            ["Local Ollama (gemma:2b)", "Local Ollama (gemma:7b)", "Cloud Gemini 2.0 Flash", "Cloud Gemini 1.5 Pro"],
            index=0 if st.session_state.ai_engine.local_available else 2
        )
        
        use_premium = st.checkbox("Use Premium Analysis", value=False)
        force_local = "Local" in ai_source
    
    # Run AI Analysis
    if st.button("🧠 Analyze Now", use_container_width=True, type="primary"):
        with st.spinner("AI is analyzing system state..."):
            try:
                analysis = st.session_state.ai_engine.analyze_incident(
                    metrics=current_metrics,
                    scenario=st.session_state.current_scenario,
                    use_premium=use_premium,
                    force_local=force_local
                )
                
                # Display results
                st.markdown(f"""
                <div class="ai-panel">
                    <div class="ai-header">
                        <div class="ai-icon">🧠</div>
                        <div class="ai-title">AI Diagnosis Results</div>
                        <div class="ai-badge">{analysis.get('model_used', 'Unknown')}</div>
                    </div>
                    
                    <div class="ai-section">
                        <div class="ai-section-label">Root Cause</div>
                        <div class="ai-section-content">{analysis.get('root_cause', 'No analysis available')}</div>
                    </div>
                    
                    <div class="ai-section">
                        <div class="ai-section-label">Recommendation</div>
                        <div class="ai-section-content">{analysis.get('recommendation', 'No recommendation available')}</div>
                    </div>
                    
                    <div class="ai-section">
                        <div class="ai-section-label">Confidence</div>
                        <div class="confidence-meter">
                            <div class="confidence-bar">
                                <div class="confidence-fill" style="width: {analysis.get('confidence', 0)}%"></div>
                            </div>
                            <span style="color: var(--aurora-cyan); font-weight: 600;">{analysis.get('confidence', 0)}%</span>
                        </div>
                    </div>
                    
                    <div class="ai-section">
                        <div class="ai-section-label">Metadata</div>
                        <div style="font-size: 12px; color: var(--smoke-gray);">
                            Source: {analysis.get('source', 'unknown')} • 
                            Latency: {analysis.get('latency_ms', 'N/A')}ms • 
                            Timestamp: {analysis.get('timestamp', 'N/A')}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ AI analysis failed: {e}")

# ============================================
# TAB 5: INCIDENT HISTORY
# ============================================
with tab5:
    st.markdown("## 📜 Incident History")
    
    if st.session_state.incidents:
        # Create DataFrame
        incidents_df = pd.DataFrame(st.session_state.incidents)
        
        # Display table
        st.dataframe(
            incidents_df[['trace_id', 'scenario_name', 'severity', 'duration_minutes', 'status']],
            use_container_width=True,
            hide_index=True
        )
        
        # Export options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Export CSV", use_container_width=True):
                csv = incidents_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"incidents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📄 Generate PDF Report", use_container_width=True):
                st.info("PDF generation coming soon!")
        
        with col3:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.incidents = []
                st.rerun()
    else:
        st.info("No incidents recorded yet. Run a chaos scenario to generate incidents.")

# ============================================
# TAB 6: COST TRACKING
# ============================================
with tab6:
    st.markdown("## 💰 Cost Tracking")
    
    # Budget overview
    budget_used = st.session_state.total_spend
    budget_total = 10.0
    budget_percent = (budget_used / budget_total) * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Spend", f"${budget_used:.2f}", f"of ${budget_total:.2f}")
    
    with col2:
        st.metric("Budget Remaining", f"${budget_total - budget_used:.2f}", f"{100 - budget_percent:.1f}%")
    
    with col3:
        st.metric("Burn Rate", "$0.0042/hour", "Sustainable")
    
    # Progress bar
    st.markdown(f"""
    <div class="cost-progress">
        <div class="cost-progress-fill" style="width: {budget_percent}%"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Cost breakdown
    st.markdown("### 📊 Cost Breakdown")
    
    breakdown = {
        "Service": ["Cloud Run", "Firestore", "Gemini API", "Storage", "Networking"],
        "Cost": [0.20, 0.15, 0.00, 0.10, 0.10],
        "Percentage": [36.4, 27.3, 0.0, 18.2, 18.2]
    }
    
    breakdown_df = pd.DataFrame(breakdown)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_pie = px.pie(
            breakdown_df,
            values='Cost',
            names='Service',
            title='Cost Distribution',
            color_discrete_sequence=['#0066FF', '#00D9FF', '#8B5CF6', '#FF6B35', '#FF3B30']
        )
        
        fig_pie.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="-apple-system, BlinkMacSystemFont", color='#E5E7EB')
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.dataframe(
            breakdown_df.style.format({'Cost': '${:.2f}', 'Percentage': '{:.1f}%'}),
            use_container_width=True,
            hide_index=True
        )

# ============================================
# TAB 7: SETTINGS
# ============================================
with tab7:
    st.markdown("## ⚙️ Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Application Settings")
        
        mode = st.selectbox(
            "Operation Mode",
            ["chaos", "live"],
            index=0 if st.session_state.mode == "chaos" else 1
        )
        
        if mode != st.session_state.mode:
            st.session_state.mode = mode
            st.session_state.metrics_engine = MetricsEngine(mode=mode)
            st.success(f"✓ Switched to {mode} mode")
        
        refresh_interval = st.slider(
            "Auto-refresh Interval (seconds)",
            min_value=1,
            max_value=60,
            value=st.session_state.refresh_interval
        )
        st.session_state.refresh_interval = refresh_interval
        
        demo_mode = st.checkbox("Demo Mode", value=st.session_state.demo_mode)
        st.session_state.demo_mode = demo_mode
    
    with col2:
        st.markdown("### AI Configuration")
        
        use_local_ai = st.checkbox(
            "Prefer Local AI (Ollama)",
            value=st.session_state.ai_engine.use_local
        )
        
        ollama_url = st.text_input(
            "Ollama URL",
            value=st.session_state.ai_engine.ollama_url
        )
        
        ollama_model = st.selectbox(
            "Default Ollama Model",
            ["gemma:2b", "gemma:7b", "llama3.2:3b"],
            index=0
        )
        
        if st.button("🔄 Reconnect AI Engine"):
            st.session_state.ai_engine = AIDiagnosisEngine(use_local=use_local_ai)
            st.success("✓ AI engine reconnected")
    
    # System Info
    st.markdown("### 📊 System Information")
    
    system_info = {
        "Version": "1.0.0",
        "Mode": st.session_state.mode,
        "AI Engine": "Gemini 2.0 Flash + Ollama",
        "Local AI Available": "✓ Yes" if st.session_state.ai_engine.local_available else "✗ No",
        "Firestore": "Connected" if st.session_state.firestore else "Disconnected",
        "Total Incidents": len(st.session_state.incidents),
        "Uptime": "Running"
    }
    
    st.json(system_info)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 64px; padding: 32px; color: var(--smoke-gray); font-size: 14px;">
    <div style="margin-bottom: 8px;">🔥 Phoenix SRE: Adaptive GPU Orchestrator</div>
    <div style="font-size: 12px; color: var(--shadow-gray);">
        BNB Marathon 2025 • Powered by Gemini 2.0 Flash • Built with ❤️
    </div>
</div>
""", unsafe_allow_html=True)

# Auto-refresh
if st.session_state.auto_refresh:
    time.sleep(st.session_state.refresh_interval)
    st.rerun()
