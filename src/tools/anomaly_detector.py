from crewai.tools import BaseTool
import json
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class AnomalyDetectorTool(BaseTool):
    """
    Tool for detecting anomalies in 5G modem performance metrics.
    
    This tool analyzes various performance metrics to identify abnormal patterns
    and potential issues affecting modem connectivity and performance.
    """
    
    name: str = "Anomaly Detector Tool"
    description: str = "Detects anomalies in 5G modem performance metrics using statistical methods and pattern recognition"
    
    def __init__(self):
        """Initialize the anomaly detector tool."""
        super().__init__()
    
    def _run(self, data, sensitivity="medium"):
        """
        Detect anomalies in performance metrics.
        
        Args:
            data (str): JSON string containing performance metrics
            sensitivity (str, optional): Detection sensitivity.
                                       Options: "low", "medium", "high"
                                    
        Returns:
            str: JSON string containing detected anomalies with descriptions
        """
        try:
            # Parse input data
            if isinstance(data, str):
                try:
                    metrics = json.loads(data)
                except json.JSONDecodeError:
                    return "Error: Invalid JSON data provided"
            else:
                metrics = data
            
            # Set anomaly detection thresholds based on sensitivity
            if sensitivity.lower() == "low":
                threshold_factor = 3.0  # Less sensitive (only detect major anomalies)
            elif sensitivity.lower() == "high":
                threshold_factor = 2.0  # More sensitive (detect subtle anomalies)
            else:  # Default to medium
                threshold_factor = 2.5
            
            # Initialize results
            anomalies = []
            
            # Check for latency anomalies
            latency_anomalies = self._detect_latency_anomalies(metrics, threshold_factor)
            if latency_anomalies:
                anomalies.extend(latency_anomalies)
            
            # Check for throughput anomalies
            throughput_anomalies = self._detect_throughput_anomalies(metrics, threshold_factor)
            if throughput_anomalies:
                anomalies.extend(throughput_anomalies)
            
            # Check for signal strength anomalies
            signal_anomalies = self._detect_signal_anomalies(metrics, threshold_factor)
            if signal_anomalies:
                anomalies.extend(signal_anomalies)
            
            # Check for packet loss anomalies
            packet_loss_anomalies = self._detect_packet_loss_anomalies(metrics, threshold_factor)
            if packet_loss_anomalies:
                anomalies.extend(packet_loss_anomalies)
            
            # Check for connection anomalies
            connection_anomalies = self._detect_connection_anomalies(metrics, threshold_factor)
            if connection_anomalies:
                anomalies.extend(connection_anomalies)
            
            # Add timestamp to each anomaly
            for anomaly in anomalies:
                anomaly["detected_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Return results
            result = {
                "anomalies": anomalies,
                "total_anomalies": len(anomalies),
                "sensitivity": sensitivity
            }
            
            return json.dumps(result, indent=2)
        
        except Exception as e:
            return f"Error detecting anomalies: {str(e)}"
    
    def _detect_latency_anomalies(self, metrics, threshold_factor):
        """Detect anomalies in latency metrics."""
        anomalies = []
        
        if "latency" in metrics:
            latency = metrics["latency"]
            
            # Check for high average latency
            avg_latency = latency.get("avg_ms", 0)
            if avg_latency > 150:
                anomalies.append({
                    "type": "High Latency",
                    "metric": "avg_ms",
                    "value": avg_latency,
                    "threshold": 150,
                    "severity": "high" if avg_latency > 200 else "medium",
                    "description": f"Average latency ({avg_latency} ms) is above acceptable threshold for 5G.",
                    "impact": "High latency affects real-time applications, gaming, and video calls.",
                    "possible_causes": [
                        "Network congestion",
                        "Distance from base station",
                        "Interference",
                        "Backhaul limitations"
                    ]
                })
            
            # Check for high jitter
            jitter = latency.get("jitter_ms", 0)
            if jitter > 30:
                anomalies.append({
                    "type": "High Jitter",
                    "metric": "jitter_ms",
                    "value": jitter,
                    "threshold": 30,
                    "severity": "high" if jitter > 50 else "medium",
                    "description": f"Latency variation (jitter) of {jitter} ms is above acceptable levels.",
                    "impact": "High jitter causes instability in real-time applications and streaming.",
                    "possible_causes": [
                        "Network congestion",
                        "Interference",
                        "Cell tower handover issues",
                        "Radio resource scheduling inconsistency"
                    ]
                })
            
            # Check for abnormal ratio between min and max latency
            min_latency = latency.get("min_ms", 0)
            max_latency = latency.get("max_ms", 0)
            
            if min_latency > 0 and max_latency > 0:
                latency_ratio = max_latency / min_latency if min_latency > 0 else 0
                
                if latency_ratio > 10:
                    anomalies.append({
                        "type": "Latency Spikes",
                        "metric": "latency_ratio",
                        "value": latency_ratio,
                        "threshold": 10,
                        "severity": "medium",
                        "description": f"Large discrepancy between minimum and maximum latency (ratio: {latency_ratio:.2f}).",
                        "impact": "Intermittent performance issues and unpredictable user experience.",
                        "possible_causes": [
                            "Interference spikes",
                            "Cell tower handovers",
                            "Congestion patterns",
                            "Competing network traffic"
                        ]
                    })
        
        return anomalies
    
    def _detect_throughput_anomalies(self, metrics, threshold_factor):
        """Detect anomalies in throughput metrics."""
        anomalies = []
        
        if "throughput" in metrics:
            throughput = metrics["throughput"]
            
            # Check for low average throughput for 5G
            avg_throughput = throughput.get("avg_kbps", 0)
            avg_mbps = avg_throughput / 1000  # Convert to Mbps
            
            if avg_mbps < 50:  # 5G should typically provide >50 Mbps
                anomalies.append({
                    "type": "Low Throughput",
                    "metric": "avg_kbps",
                    "value": avg_throughput,
                    "threshold": 50000,  # 50 Mbps in kbps
                    "severity": "high" if avg_mbps < 20 else "medium",
                    "description": f"Average throughput ({avg_mbps:.2f} Mbps) is below expected 5G performance.",
                    "impact": "Slow data transfers, buffering during streaming, and poor download/upload speeds.",
                    "possible_causes": [
                        "Poor signal quality",
                        "Network congestion",
                        "Suboptimal frequency band allocation",
                        "Cell edge conditions",
                        "Backhaul limitations"
                    ]
                })
            
            # Check for abnormal peak to average throughput ratio
            peak_throughput = throughput.get("peak_kbps", 0)
            
            if avg_throughput > 0 and peak_throughput > 0:
                throughput_ratio = peak_throughput / avg_throughput
                
                if throughput_ratio > 10:
                    anomalies.append({
                        "type": "Inconsistent Throughput",
                        "metric": "throughput_ratio",
                        "value": throughput_ratio,
                        "threshold": 10,
                        "severity": "medium",
                        "description": f"Large discrepancy between average and peak throughput (ratio: {throughput_ratio:.2f}).",
                        "impact": "Inconsistent user experience with periods of high performance followed by slowdowns.",
                        "possible_causes": [
                            "Network load fluctuations",
                            "Interference patterns",
                            "Dynamic frequency allocation issues",
                            "Scheduling algorithm inefficiencies"
                        ]
                    })
        
        return anomalies
    
    def _detect_signal_anomalies(self, metrics, threshold_factor):
        """Detect anomalies in signal strength metrics."""
        anomalies = []
        
        if "signal_strength" in metrics:
            signal = metrics["signal_strength"]
            
            # Check for weak RSSI
            rssi = signal.get("rssi_dbm", 0)
            if rssi < -100:
                anomalies.append({
                    "type": "Weak Signal",
                    "metric": "rssi_dbm",
                    "value": rssi,
                    "threshold": -100,
                    "severity": "high" if rssi < -110 else "medium",
                    "description": f"Signal strength (RSSI: {rssi} dBm) is below acceptable threshold.",
                    "impact": "Poor connection quality, frequent disconnections, and reduced data rates.",
                    "possible_causes": [
                        "Distance from cell tower",
                        "Physical obstructions",
                        "Building penetration losses",
                        "Antenna misalignment"
                    ]
                })
            
            # Check for poor SINR
            sinr = signal.get("sinr_db", 0)
            if sinr < 5:
                anomalies.append({
                    "type": "Poor Signal Quality",
                    "metric": "sinr_db",
                    "value": sinr,
                    "threshold": 5,
                    "severity": "high" if sinr < 0 else "medium",
                    "description": f"Signal-to-interference-plus-noise ratio (SINR: {sinr} dB) is below acceptable threshold.",
                    "impact": "Reduced throughput, higher error rates, and more frequent retransmissions.",
                    "possible_causes": [
                        "Interference from other transmitters",
                        "Cell overlap issues",
                        "Environmental noise",
                        "Multipath fading"
                    ]
                })
        
        return anomalies
    
    def _detect_packet_loss_anomalies(self, metrics, threshold_factor):
        """Detect anomalies in packet loss metrics."""
        anomalies = []
        
        if "packet_loss" in metrics:
            packet_loss = metrics["packet_loss"]
            
            # Check for high packet loss
            loss_percentage = packet_loss.get("loss_percentage", 0)
            if loss_percentage > 2:  # More than 2% packet loss is problematic
                anomalies.append({
                    "type": "High Packet Loss",
                    "metric": "loss_percentage",
                    "value": loss_percentage,
                    "threshold": 2,
                    "severity": "high" if loss_percentage > 5 else "medium",
                    "description": f"Packet loss rate ({loss_percentage:.2f}%) is above acceptable threshold.",
                    "impact": "Connection instability, retransmissions, and degraded application performance.",
                    "possible_causes": [
                        "Poor signal quality",
                        "Network congestion",
                        "Radio interference",
                        "Hardware issues",
                        "Mobility challenges during handovers"
                    ]
                })
            
            # Check for high retransmission count
            retransmits = packet_loss.get("retransmits", 0)
            total_packets = packet_loss.get("total_packets", 0)
            
            if total_packets > 0 and retransmits > total_packets * 0.05:  # More than 5% retransmissions
                anomalies.append({
                    "type": "Excessive Retransmissions",
                    "metric": "retransmits",
                    "value": retransmits,
                    "threshold": total_packets * 0.05,
                    "severity": "medium",
                    "description": f"High number of packet retransmissions ({retransmits}).",
                    "impact": "Reduced effective throughput and increased latency due to retransmission overhead.",
                    "possible_causes": [
                        "Signal quality fluctuations",
                        "Interference spikes",
                        "Suboptimal modulation and coding scheme selection",
                        "Error correction limitations"
                    ]
                })
        
        return anomalies
    
    def _detect_connection_anomalies(self, metrics, threshold_factor):
        """Detect anomalies in connection establishment and maintenance."""
        anomalies = []
        
        if "connection_stats" in metrics:
            connection = metrics["connection_stats"]
            
            # Check for slow handshake times
            handshake_time = connection.get("handshake_time_ms", 0)
            if handshake_time > 300:  # Handshakes should be quick in 5G
                anomalies.append({
                    "type": "Slow Connection Establishment",
                    "metric": "handshake_time_ms",
                    "value": handshake_time,
                    "threshold": 300,
                    "severity": "medium",
                    "description": f"TCP handshake time ({handshake_time} ms) is abnormally high.",
                    "impact": "Delayed connection setup affecting application start times and responsiveness.",
                    "possible_causes": [
                        "Network congestion",
                        "High latency",
                        "Suboptimal TCP parameters",
                        "Middlebox interference"
                    ]
                })
            
            # Check for connection instability
            if "handovers" in metrics:
                handovers = metrics["handovers"]
                success_rate = handovers.get("success_rate", 100)
                
                if success_rate < 90:
                    anomalies.append({
                        "type": "Handover Failures",
                        "metric": "handover_success_rate",
                        "value": success_rate,
                        "threshold": 90,
                        "severity": "high" if success_rate < 80 else "medium",
                        "description": f"Cell handover success rate ({success_rate:.2f}%) is below acceptable threshold.",
                        "impact": "Connection drops during mobility and service interruptions when changing cells.",
                        "possible_causes": [
                            "Coverage gaps between cells",
                            "Improper handover parameter configuration",
                            "Timing synchronization issues",
                            "Interference in overlapping areas"
                        ]
                    })
        
        return anomalies
