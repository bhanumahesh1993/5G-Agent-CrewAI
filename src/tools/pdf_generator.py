from crewai.tools import BaseTool
from fpdf import FPDF
import matplotlib.pyplot as plt
import os
import json
import base64
from io import BytesIO
import pandas as pd
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
from pydantic import Field

load_dotenv()

class PDFGeneratorTool(BaseTool):
    """
    Tool for generating PDF reports with 5G modem performance analysis results.
    
    This tool creates comprehensive PDF reports including charts, tables,
    and analysis of modem performance metrics.
    """
    
    name: str = "PDF Generator Tool"
    description: str = "Creates PDF reports with 5G modem analysis results, including charts and recommendations"
    output_dir: str = Field(default="output")

    def __init__(self, output_dir=None):
        """
        Initialize the PDF generator tool.
        
        Args:
            output_dir (str, optional): Directory to save generated PDFs. 
                                      Defaults to the path in .env file.
        """
        super().__init__()
        self.output_dir = output_dir or os.getenv("OUTPUT_DIR", "output")
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def _run(self, report_data, report_name=None):
        """Generate a PDF report."""
        try:
            # Parse the JSON report data
            if isinstance(report_data, str):
                try:
                    data = json.loads(report_data)
                    print(f"Successfully parsed report data JSON")
                except json.JSONDecodeError:
                    print(f"Could not parse as JSON, treating as plain text")
                    data = {"content": report_data}
            else:
                data = report_data
            
            # Generate default report name if none provided
            if not report_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                report_name = f"modem_analysis_report_{timestamp}.pdf"
            
            # Ensure report name has .pdf extension
            if not report_name.endswith(".pdf"):
                report_name += ".pdf"
            
            # Create the PDF
            print(f"Creating PDF report with name: {report_name}")
            pdf = SafeModemReportPDF()
            
            # Add report content
            self._add_report_content(pdf, data)
            
            # Save the PDF
            output_path = os.path.join(self.output_dir, report_name)
            print(f"Saving PDF to: {output_path}")
            pdf.output(output_path)
            
            print(f"PDF report successfully generated at: {output_path}")
            return f"PDF report generated: {output_path}"
        
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"Error generating PDF report: {str(e)}"
        
    def _add_report_content(self, pdf, data):
        """Add content to the PDF report."""
        # Add title page
        pdf.add_page()
        pdf.add_title_page("5G Modem Performance Analysis Report")
        
        # Add executive summary
        pdf.add_page()
        pdf.add_section_title("Executive Summary")
        
        if "summary" in data:
            pdf.add_paragraph(data["summary"])
        else:
            pdf.add_paragraph("This report provides a comprehensive analysis of 5G modem performance metrics, "
                             "including latency, throughput, signal strength, and identified anomalies. "
                             "The analysis is based on network packet data and provides recommendations "
                             "for optimizing modem performance.")
        
        # Add performance metrics section
        pdf.add_page()
        pdf.add_section_title("Performance Metrics")
        
        if "metrics" in data:
            metrics = data["metrics"]
            
            # Add latency metrics
            if "latency" in metrics:
                pdf.add_subsection_title("Latency Analysis")
                latency = metrics["latency"]
                pdf.add_metrics_table([
                    ["Metric", "Value"],
                    ["Average Latency", f"{latency.get('avg_ms', 'N/A')} ms"],
                    ["Minimum Latency", f"{latency.get('min_ms', 'N/A')} ms"],
                    ["Maximum Latency", f"{latency.get('max_ms', 'N/A')} ms"],
                    ["Jitter", f"{latency.get('jitter_ms', 'N/A')} ms"]
                ])
                
                # Generate and add latency chart
                if all(k in latency for k in ["avg_ms", "min_ms", "max_ms"]):
                    chart_path = self._generate_latency_chart(latency)
                    if chart_path:
                        pdf.add_image(chart_path, "Latency Metrics")
            
            # Add throughput metrics
            if "throughput" in metrics:
                pdf.add_subsection_title("Throughput Analysis")
                throughput = metrics["throughput"]
                pdf.add_metrics_table([
                    ["Metric", "Value"],
                    ["Average Throughput", f"{throughput.get('avg_kbps', 'N/A')} kbps"],
                    ["Peak Throughput", f"{throughput.get('peak_kbps', 'N/A')} kbps"]
                ])
                
                # Generate and add throughput chart
                if "avg_kbps" in throughput and "peak_kbps" in throughput:
                    chart_path = self._generate_throughput_chart(throughput)
                    if chart_path:
                        pdf.add_image(chart_path, "Throughput Metrics")
            
            # Add signal strength metrics
            if "signal_strength" in metrics:
                pdf.add_subsection_title("Signal Strength Analysis")
                signal = metrics["signal_strength"]
                pdf.add_metrics_table([
                    ["Metric", "Value"],
                    ["RSSI", f"{signal.get('rssi_dbm', 'N/A')} dBm"],
                    ["SINR", f"{signal.get('sinr_db', 'N/A')} dB"]
                ])
                
                # Generate and add signal strength chart
                if "rssi_dbm" in signal:
                    chart_path = self._generate_signal_chart(signal)
                    if chart_path:
                        pdf.add_image(chart_path, "Signal Strength Metrics")
        
        # Add anomalies section
        if "anomalies" in data:
            pdf.add_page()
            pdf.add_section_title("Detected Anomalies")
            
            anomalies = data["anomalies"]
            if isinstance(anomalies, list) and anomalies:
                for i, anomaly in enumerate(anomalies):
                    pdf.add_subsection_title(f"Anomaly {i+1}: {anomaly.get('type', 'Unknown')}")
                    pdf.add_paragraph(anomaly.get("description", "No description available."))
                    
                    if "severity" in anomaly:
                        pdf.add_info_box(f"Severity: {anomaly['severity']}")
                    
                    if "impact" in anomaly:
                        pdf.add_paragraph(f"Impact: {anomaly['impact']}")
            else:
                pdf.add_paragraph("No anomalies detected during the analysis period.")
        
        # Add recommendations section
        if "recommendations" in data:
            pdf.add_page()
            pdf.add_section_title("Optimization Recommendations")
            
            recommendations = data["recommendations"]
            if isinstance(recommendations, list) and recommendations:
                for i, rec in enumerate(recommendations):
                    pdf.add_subsection_title(f"Recommendation {i+1}: {rec.get('title', 'Unnamed')}")
                    pdf.add_paragraph(rec.get("description", "No description available."))
                    
                    if "priority" in rec:
                        pdf.add_info_box(f"Priority: {rec['priority']}")
                    
                    if "benefits" in rec:
                        pdf.add_paragraph(f"Expected Benefits: {rec['benefits']}")
            else:
                pdf.add_paragraph("No specific recommendations available.")
        
        # Add conclusion
        pdf.add_page()
        pdf.add_section_title("Conclusion")
        
        if "conclusion" in data:
            pdf.add_paragraph(data["conclusion"])
        else:
            pdf.add_paragraph("This report has provided a comprehensive analysis of the 5G modem performance "
                             "based on the available network data. By implementing the recommended optimizations, "
                             "modem performance can be significantly improved, leading to better user experience "
                             "and more reliable connectivity.")
    
    def _generate_latency_chart(self, latency_data):
        """Generate a chart for latency metrics."""
        try:
            plt.figure(figsize=(10, 4))
            
            # Extract metrics
            metrics = ['avg_ms', 'min_ms', 'max_ms', 'jitter_ms']
            values = [latency_data.get(m, 0) for m in metrics]
            labels = ['Average', 'Minimum', 'Maximum', 'Jitter']
            
            # Create bar chart
            plt.bar(labels, values, color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'])
            plt.ylabel('Milliseconds (ms)')
            plt.title('Latency Metrics')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            
            # Add values on top of bars
            for i, v in enumerate(values):
                plt.text(i, v + 0.5, f"{v:.2f}", ha='center')
            
            # Save as separate file
            chart_filename = f"latency_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            chart_path = os.path.join(self.output_dir, chart_filename)
            plt.tight_layout()
            plt.savefig(chart_path)
            
            # Save to BytesIO for PDF embedding
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            
            # Return as base64 string
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            return f"data:image/png;base64,{image_base64}"
        
        except Exception as e:
            print(f"Error generating latency chart: {str(e)}")
            return None
    
    def _generate_throughput_chart(self, throughput_data):
        """Generate a chart for throughput metrics."""
        try:
            plt.figure(figsize=(8, 4))
            
            # Extract metrics
            metrics = ['avg_kbps', 'peak_kbps']
            values = [throughput_data.get(m, 0) for m in metrics]
            labels = ['Average Throughput', 'Peak Throughput']
            
            # Create bar chart
            plt.bar(labels, values, color=['#3498db', '#e74c3c'])
            plt.ylabel('Kilobits per second (kbps)')
            plt.title('Throughput Metrics')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            
            # Add values on top of bars
            for i, v in enumerate(values):
                plt.text(i, v + (max(values) * 0.01), f"{v:.2f}", ha='center')
            
            # Save to BytesIO
            buffer = BytesIO()
            plt.tight_layout()
            plt.savefig(buffer, format='png')
            plt.close()
            
            # Return as base64 string
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            return f"data:image/png;base64,{image_base64}"
        
        except Exception as e:
            print(f"Error generating throughput chart: {str(e)}")
            return None
    
    def _generate_signal_chart(self, signal_data):
        """Generate a chart for signal strength metrics."""
        try:
            plt.figure(figsize=(10, 5))
            
            # Create gauge-like visualization for RSSI
            rssi = signal_data.get('rssi_dbm', -65)
            sinr = signal_data.get('sinr_db', 15)
            
            # RSSI gauge
            ax1 = plt.subplot(1, 2, 1)
            gauge_range = np.linspace(-120, -30, 100)
            colors = []
            for val in gauge_range:
                if val < -100:
                    colors.append('#e74c3c')  # Red for poor
                elif val < -80:
                    colors.append('#f39c12')  # Orange for fair
                else:
                    colors.append('#2ecc71')  # Green for good
            
            plt.barh(y=0, width=1, height=0.5, color='lightgrey')
            rssi_norm = (rssi + 120) / 90  # Normalize to 0-1
            rssi_norm = min(max(rssi_norm, 0), 1)  # Clamp to 0-1
            plt.barh(y=0, width=rssi_norm, height=0.5, color=colors[int(rssi_norm * 99)])
            
            plt.title('RSSI Signal Strength')
            plt.xlim(0, 1)
            plt.ylim(-0.5, 0.5)
            plt.text(rssi_norm, 0, f"{rssi} dBm", ha='center', va='center', color='black', fontweight='bold')
            plt.xticks([0, 0.5, 1], ['-120 dBm', '-75 dBm', '-30 dBm'])
            plt.yticks([])
            
            # SINR gauge
            ax2 = plt.subplot(1, 2, 2)
            gauge_range = np.linspace(0, 30, 100)
            colors = []
            for val in gauge_range:
                if val < 10:
                    colors.append('#e74c3c')  # Red for poor
                elif val < 20:
                    colors.append('#f39c12')  # Orange for fair
                else:
                    colors.append('#2ecc71')  # Green for good
            
            plt.barh(y=0, width=1, height=0.5, color='lightgrey')
            sinr_norm = sinr / 30  # Normalize to 0-1
            sinr_norm = min(max(sinr_norm, 0), 1)  # Clamp to 0-1
            plt.barh(y=0, width=sinr_norm, height=0.5, color=colors[int(sinr_norm * 99)])
            
            plt.title('SINR Quality')
            plt.xlim(0, 1)
            plt.ylim(-0.5, 0.5)
            plt.text(sinr_norm, 0, f"{sinr} dB", ha='center', va='center', color='black', fontweight='bold')
            plt.xticks([0, 0.5, 1], ['0 dB', '15 dB', '30 dB'])
            plt.yticks([])
            
            # Save to BytesIO
            buffer = BytesIO()
            plt.tight_layout()
            plt.savefig(buffer, format='png')
            plt.close()
            
            # Return as base64 string
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            return f"data:image/png;base64,{image_base64}"
        
        except Exception as e:
            print(f"Error generating signal strength chart: {str(e)}")
            return None


class ModemReportPDF(FPDF):
    """Custom PDF class for modem analysis reports."""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        #self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        #self.add_font('DejaVu', 'B', 'DejaVuSansCondensed-Bold.ttf', uni=True)

        # Set default font
        self.set_font('Arial', '', 11)
        
        # Define colors
        self.title_color = (41, 128, 185)  # Blue
        self.section_color = (52, 73, 94)  # Dark Blue-Gray
        self.text_color = (44, 62, 80)  # Dark Gray
        self.accent_color = (46, 204, 113)  # Green
    
    def header(self):
        """Add header to each page."""
        if self.page_no() > 1:  # Skip header on title page
            # Add logo here if available
            # self.image('logo.png', 10, 8, 33)
            
            # Add report title
            self.set_font('Arial', 'B', 10)
            self.set_text_color(*self.title_color)
            self.cell(0, 10, '5G Modem Performance Analysis Report', 0, 0, 'R')
            
            # Add line
            self.ln(12)
            self.set_draw_color(200, 200, 200)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(10)
    
    def footer(self):
        """Add footer to each page."""
        if self.page_no() > 1:  # Skip footer on title page
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
            
            # Add date on the right
            current_date = datetime.now().strftime("%Y-%m-%d")
            self.cell(0, 10, current_date, 0, 0, 'R')
    
    def add_title_page(self, title):
        """Add a title page to the report."""
        # Set font color
        self.set_text_color(*self.title_color)
        
        # Add title
        self.set_font('Arial', 'B', 24)
        self.ln(60)
        self.cell(0, 20, title, 0, 1, 'C')
        
        # Add subtitle
        self.set_font('Arial', '', 16)
        self.set_text_color(*self.section_color)
        self.ln(10)
        self.cell(0, 10, 'Analysis and Optimization Recommendations', 0, 1, 'C')
        
        # Add date
        self.set_font('Arial', '', 12)
        self.ln(40)
        current_date = datetime.now().strftime("%B %d, %Y")
        self.cell(0, 10, f'Generated on {current_date}', 0, 1, 'C')
        
        # Add company/author
        self.ln(10)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(*self.accent_color)
        self.cell(0, 10, 'Modem Intelligence Crew', 0, 1, 'C')
    
    def add_section_title(self, title):
        """Add a section title."""
        self.ln(5)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(*self.section_color)
        self.cell(0, 10, title, 0, 1, 'L')
        
        # Add underline
        self.set_draw_color(*self.section_color)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(10)
    
    def add_subsection_title(self, title):
        """Add a subsection title."""
        self.ln(5)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(*self.text_color)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)
    
    def add_paragraph(self, text):
        """Add a paragraph of text."""
        self.set_font('Arial', '', 11)
        
        # Ensure text_color is correct, use default if corrupted
        try:
            # Check if text_color has the right structure
            if not (isinstance(self.text_color, tuple) and len(self.text_color) == 3):
                # Reset to default if corrupted
                self.text_color = (44, 62, 80)  # Reset to default
            
            self.set_text_color(*self.text_color)
        except Exception as e:
            # Fallback to black text if something goes wrong
            self.set_text_color(0, 0, 0)
            print(f"Warning: Using default text color due to: {e}")
        
        # Process the text to ensure it's a valid string
        if text is None:
            text = "No content available"
        
        try:
            self.multi_cell(0, 6, str(text))
        except Exception as e:
            print(f"Error adding text: {e}")
            self.multi_cell(0, 6, "Error displaying content")
        
        self.ln(5)
    
    def add_metrics_table(self, data):
        """Add a table with metrics."""
        self.ln(5)
        
        # Calculate column widths
        col_width = 190 / 2
        
        # Add table headers
        self.set_font('Arial', 'B', 11)
        self.set_fill_color(240, 240, 240)
        for header in data[0]:
            self.cell(col_width, 10, header, 1, 0, 'C', 1)
        self.ln()
        
        # Add table data
        self.set_font('Arial', '', 11)
        for row in data[1:]:
            for i, cell in enumerate(row):
                # Make the first column bold
                if i == 0:
                    self.set_font('Arial', 'B', 11)
                    self.cell(col_width, 8, cell, 1, 0, 'L')
                    self.set_font('Arial', '', 11)
                else:
                    self.cell(col_width, 8, cell, 1, 0, 'C')
            self.ln()
        
        self.ln(5)
    
    def add_info_box(self, text):
        """Add an information box."""
        self.ln(5)
        self.set_fill_color(235, 245, 251)  # Light blue background
        self.set_font('Arial', 'B', 11)
        self.set_text_color(*self.text_color)
        self.multi_cell(0, 8, text, 1, 'L', 1)
        self.ln(5)
    
    def add_image(self, image_path, caption=None):
        """Add an image to the PDF."""
        try:
            # Check if the image path is a base64 data URL
            if image_path.startswith('data:image'):
                # Split the data URL to get the base64 data
                header, base64_data = image_path.split(",", 1)
                
                # Create a temporary file name
                temp_path = f"temp_image_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
                
                # Decode base64 and save as temporary image
                with open(temp_path, 'wb') as temp_file:
                    temp_file.write(base64.b64decode(base64_data))
                
                # Add the image
                self.image(temp_path, x=10, y=None, w=180)
                
                # Remove the temporary file
                os.remove(temp_path)
            else:
                # Add image directly from file path
                self.image(image_path, x=10, y=None, w=180)
            
            # Add caption if provided
            if caption:
                self.ln(2)
                self.set_font('Arial', 'I', 10)
                self.set_text_color(100, 100, 100)
                self.cell(0, 10, caption, 0, 1, 'C')
            
            self.ln(5)
        
        except Exception as e:
            print(f"Error adding image: {str(e)}")
            self.add_paragraph(f"[Error loading image: {str(e)}]")


class SafeModemReportPDF(FPDF):
    """A more robust PDF class that doesn't rely on class attributes for colors."""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_font('Arial', '', 11)
    
    def safe_text_color(self, r, g, b):
        """Safely set text color with explicit RGB values."""
        try:
            self.set_text_color(r, g, b)
        except Exception as e:
            print(f"Warning: Color setting failed: {e}")
            self.set_text_color(0, 0, 0)  # Default to black
    
    def add_title_page(self, title):
        """Add a title page with hardcoded colors."""
        # Blue title
        self.safe_text_color(41, 128, 185)
        
        self.set_font('Arial', 'B', 24)
        self.ln(60)
        self.cell(0, 20, title, 0, 1, 'C')
        
        # Dark blue-gray subtitle
        self.safe_text_color(52, 73, 94)
        
        self.set_font('Arial', '', 16)
        self.ln(10)
        self.cell(0, 10, 'Analysis and Optimization Recommendations', 0, 1, 'C')
        
        # Date
        self.set_font('Arial', '', 12)
        self.ln(40)
        current_date = datetime.now().strftime("%B %d, %Y")
        self.cell(0, 10, f'Generated on {current_date}', 0, 1, 'C')
        
        # Green author
        self.safe_text_color(46, 204, 113)
        
        self.set_font('Arial', 'B', 14)
        self.ln(10)
        self.cell(0, 10, 'Modem Intelligence Crew', 0, 1, 'C')
    
    def add_section_title(self, title):
        """Add a section title with hardcoded colors."""
        self.ln(5)
        self.set_font('Arial', 'B', 16)
        
        # Dark blue-gray
        self.safe_text_color(52, 73, 94)
        
        self.cell(0, 10, title, 0, 1, 'L')
        
        # Add underline with same color
        self.set_draw_color(52, 73, 94)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(10)
    
    def add_subsection_title(self, title):
        """Add a subsection title with hardcoded colors."""
        self.ln(5)
        self.set_font('Arial', 'B', 14)
        
        # Dark gray
        self.safe_text_color(44, 62, 80)
        
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)
    
    def add_paragraph(self, text):
        """Add a paragraph with hardcoded colors."""
        if text is None:
            text = "No content available"
            
        self.set_font('Arial', '', 11)
        
        # Dark gray
        self.safe_text_color(44, 62, 80)
        
        try:
            self.multi_cell(0, 6, str(text))
        except Exception as e:
            print(f"Error in add_paragraph: {e}")
            self.multi_cell(0, 6, "Error displaying content")
            
        self.ln(5)
    
    # Add other methods with similar hardcoded colors...
    def add_metrics_table(self, data):
        """Add a table with metrics."""
        self.ln(5)
        
        # Calculate column widths
        col_width = 190 / 2
        
        # Add table headers
        self.set_font('Arial', 'B', 11)
        self.set_fill_color(240, 240, 240)
        for header in data[0]:
            self.cell(col_width, 10, header, 1, 0, 'C', 1)
        self.ln()
        
        # Add table data
        self.set_font('Arial', '', 11)
        for row in data[1:]:
            for i, cell in enumerate(row):
                # Make the first column bold
                if i == 0:
                    self.set_font('Arial', 'B', 11)
                    self.cell(col_width, 8, cell, 1, 0, 'L')
                    self.set_font('Arial', '', 11)
                else:
                    self.cell(col_width, 8, cell, 1, 0, 'C')
            self.ln()
        
        self.ln(5)
    
    def add_info_box(self, text):
        """Add an information box."""
        self.ln(5)
        self.set_fill_color(235, 245, 251)  # Light blue background
        self.set_font('Arial', 'B', 11)
        self.set_text_color(*self.text_color)
        self.multi_cell(0, 8, text, 1, 'L', 1)
        self.ln(5)
    
    def add_image(self, image_path, caption=None):
        """Add an image to the PDF."""
        try:
            # Check if the image path is a base64 data URL
            if image_path.startswith('data:image'):
                # Split the data URL to get the base64 data
                header, base64_data = image_path.split(",", 1)
                
                # Create a temporary file name
                temp_path = f"temp_image_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
                
                # Decode base64 and save as temporary image
                with open(temp_path, 'wb') as temp_file:
                    temp_file.write(base64.b64decode(base64_data))
                
                # Add the image
                self.image(temp_path, x=10, y=None, w=180)
                
                # Remove the temporary file
                os.remove(temp_path)
            else:
                # Add image directly from file path
                self.image(image_path, x=10, y=None, w=180)
            
            # Add caption if provided
            if caption:
                self.ln(2)
                self.set_font('Arial', 'I', 10)
                self.set_text_color(100, 100, 100)
                self.cell(0, 10, caption, 0, 1, 'C')
            
            self.ln(5)
        except Exception as e:
            print(f"Error adding image: {str(e)}")
            self.add_paragraph(f"[Error loading image: {str(e)}]")