from crewai.tools import BaseTool
import json
import pandas as pd
import numpy as np
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class MetricsExtractorTool(BaseTool):
    """
    Tool for extracting and analyzing specific metrics from network data.
    
    This tool processes raw network data to extract specific performance metrics
    and patterns relevant to 5G modem performance analysis.
    """
    
    name: str = "Metrics Extractor Tool"
    description: str = "Extracts and analyzes specific metrics from network data for 5G modem performance analysis"
    
    def __init__(self):
        """Initialize the metrics extractor tool."""
        super().__init__()
    
    def _run(self, data, metric_type=None):
        """
        Extract and analyze specific metrics.
        
        Args:
            data (str): JSON string containing network data
            metric_type (str, optional): Type of metrics to extract.
                                       Options: "latency", "throughput", "signal", "all"
                                    
        Returns:
            str: JSON string containing the extracted and analyzed metrics
        """
        try:
            # Parse input data
            if isinstance(data, str):
                try:
                    parsed_data = json.loads(data)
                except json.JSONDecodeError:
                    return "Error: Invalid JSON data provided"
            else:
                parsed_data = data
            
            # Determine which metrics to extract
            if not metric_type or metric_type.lower() == "all":
                extract_all = True
            else:
                extract_all = False
                metrics_list = [m.strip().lower() for m in metric_type.split(",")]
            
            # Initialize results
            results = {}
            
            # Process different metric types
            if extract_all or "latency" in metrics_list:
                results["latency"] = self._analyze_latency(parsed_data)
            
            if extract_all or "throughput" in metrics_list:
                results["throughput"] = self._analyze_throughput(parsed_data)
            
            if extract_all or "signal" in metrics_list:
                results["signal"] = self._analyze_signal(parsed_data)
            
            if extract_all or "connection" in metrics_list:
                results["connection"] = self._analyze_connections(parsed_data)
            
            if extract_all or "packet_loss" in metrics_list:
                results["packet_loss"] = self._analyze_packet_loss(parsed_data)
            
            if extract_all or "handovers" in metrics_list:
                results["handovers"] = self._analyze_handovers(parsed_data)
            
            # Return results as JSON string
            return json.dumps(results, indent=2)
        
        except Exception as e:
            return f"Error extracting metrics: {str(e)}"
    
    def _analyze_latency(self, data):
        """Analyze latency metrics."""
        try:
            latency_metrics = {
                "analysis": {
                    "quality": "unknown",
                    "issues": [],
                    "recommendations": []
                }
            }
            
            # Extract latency data if available
            if "latency" in data:
                latency_data = data["latency"]
                latency_metrics.update(latency_data)
                
                # Analyze latency quality
                avg_latency = latency_data.get("avg_ms", 0)
                jitter = latency_data.get("jitter_ms", 0)
                
                # Determine latency quality
                if avg_latency < 50:
                    latency_metrics["analysis"]["quality"] = "excellent"
                elif avg_latency < 100:
                    latency_metrics["analysis"]["quality"] = "good"
                elif avg_latency < 150:
                    latency_metrics["analysis"]["quality"] = "fair"
                else:
                    latency_metrics["analysis"]["quality"] = "poor"
                
                # Identify issues
                if avg_latency > 100:
                    latency_metrics["analysis"]["issues"].append("High average latency")
                
                if jitter > 20:
                    latency_metrics["analysis"]["issues"].append("High jitter indicates unstable connection")
                
                # Provide recommendations
                if avg_latency > 100 or jitter > 20:
                    latency_metrics["analysis"]["recommendations"].append(
                        "Optimize network parameters to reduce latency and jitter"
                    )
                    latency_metrics["analysis"]["recommendations"].append(
                        "Check for network congestion or interference"
                    )
            
            return latency_metrics
        
        except Exception as e:
            return {"error": f"Error analyzing latency: {str(e)}"}
    
    def _analyze_throughput(self, data):
        """Analyze throughput metrics."""
        try:
            throughput_metrics = {
                "analysis": {
                    "quality": "unknown",
                    "issues": [],
                    "recommendations": []
                }
            }
            
            # Extract throughput data if available
            if "throughput" in data:
                throughput_data = data["throughput"]
                throughput_metrics.update(throughput_data)
                
                # Analyze throughput quality
                avg_throughput = throughput_data.get("avg_kbps", 0)
                peak_throughput = throughput_data.get("peak_kbps", 0)
                
                # Convert to Mbps for easier analysis
                avg_mbps = avg_throughput / 1000
                peak_mbps = peak_throughput / 1000
                
                # Determine throughput quality for 5G
                if avg_mbps > 100:
                    throughput_metrics["analysis"]["quality"] = "excellent"
                elif avg_mbps > 50:
                    throughput_metrics["analysis"]["quality"] = "good"
                elif avg_mbps > 10:
                    throughput_metrics["analysis"]["quality"] = "fair"
                else:
                    throughput_metrics["analysis"]["quality"] = "poor"
                
                # Identify issues
                if avg_mbps < 10:
                    throughput_metrics["analysis"]["issues"].append("Low average throughput for 5G")
                
                if peak_mbps < 20:
                    throughput_metrics["analysis"]["issues"].append("Low peak throughput indicates potential limitations")
                
                if peak_mbps > avg_mbps * 5:
                    throughput_metrics["analysis"]["issues"].append("Large discrepancy between average and peak throughput")
                
                # Provide recommendations
                if avg_mbps < 50:
                    throughput_metrics["analysis"]["recommendations"].append(
                        "Check for signal quality issues affecting throughput"
                    )
                    throughput_metrics["analysis"]["recommendations"].append(
                        "Verify if the modem is connecting to optimal 5G bands"
                    )
            
            return throughput_metrics
        
        except Exception as e:
            return {"error": f"Error analyzing throughput: {str(e)}"}
    
    def _analyze_signal(self, data):
        """Analyze signal strength metrics."""
        try:
            signal_metrics = {
                "analysis": {
                    "quality": "unknown",
                    "issues": [],
                    "recommendations": []
                }
            }
            
            # Extract signal data if available
            if "signal_strength" in data:
                signal_data = data["signal_strength"]
                signal_metrics.update(signal_data)
                
                # Analyze signal quality
                rssi = signal_data.get("rssi_dbm", 0)
                sinr = signal_data.get("sinr_db", 0)
                
                # Determine signal quality based on RSSI and SINR
                if rssi > -70 and sinr > 20:
                    signal_metrics["analysis"]["quality"] = "excellent"
                elif rssi > -80 and sinr > 10:
                    signal_metrics["analysis"]["quality"] = "good"
                elif rssi > -90 and sinr > 5:
                    signal_metrics["analysis"]["quality"] = "fair"
                else:
                    signal_metrics["analysis"]["quality"] = "poor"
                
                # Identify issues
                if rssi < -90:
                    signal_metrics["analysis"]["issues"].append("Weak signal strength (RSSI)")
                
                if sinr < 5:
                    signal_metrics["analysis"]["issues"].append("Poor signal-to-noise ratio (SINR)")
                
                # Provide recommendations
                if rssi < -85 or sinr < 10:
                    signal_metrics["analysis"]["recommendations"].append(
                        "Check for physical obstructions or interference sources"
                    )
                    signal_metrics["analysis"]["recommendations"].append(
                        "Consider repositioning the modem or using external antennas"
                    )
                    signal_metrics["analysis"]["recommendations"].append(
                        "Verify if the modem is connecting to the optimal cell tower"
                    )
            
            return signal_metrics
        
        except Exception as e:
            return {"error": f"Error analyzing signal strength: {str(e)}"}
    
    def _analyze_connections(self, data):
        """Analyze connection statistics."""
        try:
            connection_metrics = {
                "analysis": {
                    "quality": "unknown",
                    "issues": [],
                    "recommendations": []
                }
            }
            
            # Extract connection data if available
            if "connection_stats" in data:
                conn_data = data["connection_stats"]
                connection_metrics.update(conn_data)
                
                # Analyze connection quality
                handshake_time = conn_data.get("handshake_time_ms", 0)
                
                # Determine connection quality
                if handshake_time < 50:
                    connection_metrics["analysis"]["quality"] = "excellent"
                elif handshake_time < 100:
                    connection_metrics["analysis"]["quality"] = "good"
                elif handshake_time < 200:
                    connection_metrics["analysis"]["quality"] = "fair"
                else:
                    connection_metrics["analysis"]["quality"] = "poor"
                
                # Identify issues
                if handshake_time > 150:
                    connection_metrics["analysis"]["issues"].append("Slow TCP handshake times")
                
                # Provide recommendations
                if handshake_time > 150:
                    connection_metrics["analysis"]["recommendations"].append(
                        "Optimize TCP parameters for better connection establishment"
                    )
                    connection_metrics["analysis"]["recommendations"].append(
                        "Check for network congestion affecting connection setup"
                    )
            
            return connection_metrics
        
        except Exception as e:
            return {"error": f"Error analyzing connections: {str(e)}"}
    
    def _analyze_packet_loss(self, data):
        """Analyze packet loss metrics."""
        try:
            packet_loss_metrics = {
                "analysis": {
                    "quality": "unknown",
                    "issues": [],
                    "recommendations": []
                }
            }
            
            # Extract packet loss data if available
            if "packet_loss" in data:
                loss_data = data["packet_loss"]
                packet_loss_metrics.update(loss_data)
                
                # Analyze packet loss quality
                loss_percentage = loss_data.get("loss_percentage", 0)
                
                # Determine packet loss quality
                if loss_percentage < 0.1:
                    packet_loss_metrics["analysis"]["quality"] = "excellent"
                elif loss_percentage < 0.5:
                    packet_loss_metrics["analysis"]["quality"] = "good"
                elif loss_percentage < 2:
                    packet_loss_metrics["analysis"]["quality"] = "fair"
                else:
                    packet_loss_metrics["analysis"]["quality"] = "poor"
                
                # Identify issues
                if loss_percentage > 1:
                    packet_loss_metrics["analysis"]["issues"].append("High packet loss rate")
                
                # Provide recommendations
                if loss_percentage > 1:
                    packet_loss_metrics["analysis"]["recommendations"].append(
                        "Check for interference or signal quality issues"
                    )
                    packet_loss_metrics["analysis"]["recommendations"].append(
                        "Verify if error correction mechanisms are properly configured"
                    )
            
            return packet_loss_metrics
        
        except Exception as e:
            return {"error": f"Error analyzing packet loss: {str(e)}"}
    
    def _analyze_handovers(self, data):
        """Analyze handover metrics (frequency and success rate)."""
        try:
            # Note: Handover information might not be directly available in PCAP data
            # This is a simulated analysis based on available data
            
            handover_metrics = {
                "handovers_detected": 0,
                "success_rate": 100.0,
                "avg_duration_ms": 0,
                "analysis": {
                    "quality": "unknown",
                    "issues": [],
                    "recommendations": []
                }
            }
            
            # Look for cell ID changes or mobility management messages if available
            if "protocol_stats" in data and "ngap" in data["protocol_stats"]:
                ngap_data = data["protocol_stats"]["ngap"]
                
                # Look for handover-related procedures
                handover_procedures = [
                    proc for proc in ngap_data.get("procedures", [])
                    if "handover" in proc.get("name", "").lower()
                ]
                
                if handover_procedures:
                    # Count handovers
                    handover_metrics["handovers_detected"] = len(handover_procedures)
                    
                    # Calculate success rate
                    successful = sum(1 for proc in handover_procedures if proc.get("result") == "success")
                    if handover_procedures:
                        handover_metrics["success_rate"] = (successful / len(handover_procedures)) * 100
                    
                    # Calculate average duration if available
                    durations = [proc.get("duration_ms", 0) for proc in handover_procedures if "duration_ms" in proc]
                    if durations:
                        handover_metrics["avg_duration_ms"] = sum(durations) / len(durations)
                    
                    # Determine quality
                    if handover_metrics["success_rate"] > 95 and handover_metrics["avg_duration_ms"] < 100:
                        handover_metrics["analysis"]["quality"] = "excellent"
                    elif handover_metrics["success_rate"] > 90 and handover_metrics["avg_duration_ms"] < 200:
                        handover_metrics["analysis"]["quality"] = "good"
                    elif handover_metrics["success_rate"] > 80 and handover_metrics["avg_duration_ms"] < 300:
                        handover_metrics["analysis"]["quality"] = "fair"
                    else:
                        handover_metrics["analysis"]["quality"] = "poor"
                    
                    # Identify issues
                    if handover_metrics["success_rate"] < 90:
                        handover_metrics["analysis"]["issues"].append("Low handover success rate")
                    
                    if handover_metrics["avg_duration_ms"] > 200:
                        handover_metrics["analysis"]["issues"].append("Slow handover execution")
                    
                    # Provide recommendations
                    if handover_metrics["success_rate"] < 90 or handover_metrics["avg_duration_ms"] > 200:
                        handover_metrics["analysis"]["recommendations"].append(
                            "Review handover parameters for optimization"
                        )
                        handover_metrics["analysis"]["recommendations"].append(
                            "Check for coverage gaps between cells"
                        )
                else:
                    handover_metrics["analysis"]["quality"] = "not_applicable"
                    handover_metrics["analysis"]["issues"].append("No handovers detected in the analyzed data")
            else:
                handover_metrics["analysis"]["quality"] = "unknown"
                handover_metrics["analysis"]["issues"].append("No handover data available")
            
            return handover_metrics
        
        except Exception as e:
            return {"error": f"Error analyzing handovers: {str(e)}"}
