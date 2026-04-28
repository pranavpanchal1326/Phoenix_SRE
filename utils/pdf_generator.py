"""
PDF Report Generator - Create professional incident reports
Uses FPDF2 for PDF generation with custom styling
"""

from fpdf import FPDF
from datetime import datetime
from typing import Dict, List, Optional
import os


class PDFReportGenerator:
    """
    Generate professional PDF incident reports
    Includes Phoenix SRE branding and formatting
    """
    
    def __init__(self):
        """Initialize PDF generator with custom styling"""
        self.colors = {
            "primary": (66, 133, 244),  # Google Blue
            "success": (52, 168, 83),   # Google Green
            "warning": (251, 188, 5),   # Google Yellow
            "danger": (234, 67, 53),    # Google Red
            "gray": (95, 99, 104),      # Google Gray
            "black": (32, 33, 36),
            "white": (255, 255, 255),
        }
        
    def generate_incident_report(
        self,
        incident_data: Dict,
        output_path: str = "incident_report.pdf"
    ) -> str:
        """
        Generate complete incident report PDF
        
        Args:
            incident_data: Complete incident object
            output_path: Where to save the PDF
            
        Returns:
            Path to generated PDF
        """
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        self._add_header(pdf, incident_data)
        
        # Executive Summary
        self._add_executive_summary(pdf, incident_data)
        
        # Timeline
        self._add_timeline(pdf, incident_data)
        
        # Technical Analysis
        self._add_technical_analysis(pdf, incident_data)
        
        # Metrics
        self._add_metrics_section(pdf, incident_data)
        
        # Cost Impact
        self._add_cost_impact(pdf, incident_data)
        
        # Recommendations
        self._add_recommendations(pdf, incident_data)
        
        # Footer
        self._add_footer(pdf)
        
        # Save PDF
        pdf.output(output_path)
        return output_path
    
    def _add_header(self, pdf: FPDF, incident_data: Dict):
        """Add report header with branding"""
        # Title
        pdf.set_font("Arial", "B", 24)
        pdf.set_text_color(*self.colors["primary"])
        pdf.cell(0, 15, "Phoenix SRE", ln=True, align="C")
        
        pdf.set_font("Arial", "", 12)
        pdf.set_text_color(*self.colors["gray"])
        pdf.cell(0, 8, "Adaptive GPU Orchestrator - Incident Report", ln=True, align="C")
        
        pdf.ln(5)
        
        # Incident header box
        pdf.set_fill_color(*self.colors["primary"])
        pdf.set_text_color(*self.colors["white"])
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"  {incident_data['icon']} {incident_data['scenario_name']}", ln=True, fill=True)
        
        # Incident metadata
        pdf.set_text_color(*self.colors["black"])
        pdf.set_font("Arial", "", 10)
        pdf.ln(3)
        
        metadata = [
            ("Trace ID:", incident_data['trace_id']),
            ("Severity:", incident_data['severity'].upper()),
            ("Status:", incident_data['status'].upper()),
            ("Duration:", f"{incident_data['duration_minutes']} minutes"),
        ]
        
        for label, value in metadata:
            pdf.set_font("Arial", "B", 10)
            pdf.cell(40, 6, label)
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 6, value, ln=True)
        
        pdf.ln(5)
    
    def _add_executive_summary(self, pdf: FPDF, incident_data: Dict):
        """Add executive summary section"""
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(*self.colors["primary"])
        pdf.cell(0, 10, "Executive Summary", ln=True)
        
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(*self.colors["black"])
        
        summary = f"""On {incident_data['start_time'][:10]}, the {incident_data['service']} service experienced a {incident_data['severity']} severity incident lasting {incident_data['duration_minutes']} minutes. The incident was automatically detected by Phoenix AI and resolved through human-approved scaling actions.

Impact: Approximately {incident_data['affected_users']} users experienced degraded service during the incident window.

Resolution: {incident_data['ai_recommendation']}"""
        
        pdf.multi_cell(0, 5, summary)
        pdf.ln(5)
    
    def _add_timeline(self, pdf: FPDF, incident_data: Dict):
        """Add incident timeline"""
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(*self.colors["primary"])
        pdf.cell(0, 10, "Incident Timeline", ln=True)
        
        pdf.set_font("Arial", "", 9)
        pdf.set_text_color(*self.colors["black"])
        
        # Timeline table
        col_widths = [45, 145]
        
        # Header
        pdf.set_fill_color(*self.colors["gray"])
        pdf.set_text_color(*self.colors["white"])
        pdf.set_font("Arial", "B", 9)
        pdf.cell(col_widths[0], 7, "Time", 1, 0, "C", True)
        pdf.cell(col_widths[1], 7, "Event", 1, 1, "C", True)
        
        # Rows
        pdf.set_text_color(*self.colors["black"])
        pdf.set_font("Arial", "", 9)
        
        for action in incident_data.get('actions', []):
            time_str = action['time'][11:19]  # Extract HH:MM:SS
            pdf.cell(col_widths[0], 6, time_str, 1)
            pdf.cell(col_widths[1], 6, f"{action['action']} ({action['actor']})", 1, 1)
        
        pdf.ln(5)
    
    def _add_technical_analysis(self, pdf: FPDF, incident_data: Dict):
        """Add technical analysis section"""
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(*self.colors["primary"])
        pdf.cell(0, 10, "Root Cause Analysis", ln=True)
        
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(*self.colors["black"])
        pdf.multi_cell(0, 5, incident_data['root_cause'])
        
        pdf.ln(5)
    
    def _add_metrics_section(self, pdf: FPDF, incident_data: Dict):
        """Add metrics section"""
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(*self.colors["primary"])
        pdf.cell(0, 10, "Key Metrics", ln=True)
        
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(*self.colors["black"])
        
        metrics = incident_data.get('metrics', {})
        for key, value in metrics.items():
            label = key.replace('_', ' ').title()
            pdf.cell(80, 6, f"{label}:")
            pdf.cell(0, 6, str(value), ln=True)
        
        pdf.ln(5)
    
    def _add_cost_impact(self, pdf: FPDF, incident_data: Dict):
        """Add cost impact section"""
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(*self.colors["primary"])
        pdf.cell(0, 10, "Cost Impact", ln=True)
        
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(*self.colors["black"])
        
        cost_items = [
            ("Total Incident Cost:", f"${incident_data['total_cost']}"),
            ("Scaling Cost/Hour:", f"${incident_data['scaling_cost_per_hour']}/hr"),
            ("Cost Savings (Early Detection):", f"${incident_data['cost_savings']}"),
        ]
        
        for label, value in cost_items:
            pdf.set_font("Arial", "B", 10)
            pdf.cell(80, 6, label)
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 6, value, ln=True)
        
        pdf.ln(5)
    
    def _add_recommendations(self, pdf: FPDF, incident_data: Dict):
        """Add recommendations section"""
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(*self.colors["primary"])
        pdf.cell(0, 10, "Recommendations", ln=True)
        
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(*self.colors["black"])
        pdf.multi_cell(0, 5, incident_data['ai_recommendation'])
        
        pdf.ln(5)
    
    def _add_footer(self, pdf: FPDF):
        """Add report footer"""
        pdf.set_y(-20)
        pdf.set_font("Arial", "I", 8)
        pdf.set_text_color(*self.colors["gray"])
        pdf.cell(0, 10, f"Generated by Phoenix SRE on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 0, "C")
