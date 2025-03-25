from .base_agent import create_base_agent
from ..tools.pcap_analyzer import PcapAnalyzerTool
from ..tools.metrics_extractor import MetricsExtractorTool
import os
from langchain_openai import ChatOpenAI

def create_network_monitoring_agent(tools=None, allow_delegation=True, verbose=None):
    """
    Create a Network Monitoring Agent.
    
    This agent is responsible for collecting and analyzing real-time modem
    performance metrics like latency, signal strength, and throughput.
    
    Args:
        tools (list, optional): Additional tools for the agent
        allow_delegation (bool, optional): Whether the agent can delegate tasks
        verbose (bool, optional): Whether to enable verbose mode
        
    Returns:
        Agent: Configured Network Monitoring Agent
    """
    # Define agent details
    role = "Network Monitoring Agent"
    goal = "Collect and analyze comprehensive 5G modem performance metrics to provide accurate network insights"
    backstory = (
        "You are an expert in telecommunications network monitoring with specialized knowledge "
        "in 5G technology and modem performance analysis. Your background includes "
        "extensive experience with network protocols, packet analysis, and performance optimization. "
        "You excel at extracting meaningful insights from complex network data and can "
        "identify subtle patterns that might indicate performance issues. Your precise "
        "measurements and detailed analysis are crucial for understanding the current state "
        "of the network and detecting any anomalies."
    )
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
    verbose_level = int(os.getenv("VERBOSE_LEVEL", "1")) if verbose is None else verbose
    
    # Create standard tools if none provided
    agent_tools = tools if tools is not None else [
        PcapAnalyzerTool(),
        MetricsExtractorTool()
    ]
    
    # Create and return the agent
    return create_base_agent(
        role=role,
        goal=goal,
        backstory=backstory,
        tools=agent_tools,
        
        allow_delegation=allow_delegation,
        verbose=verbose_level
    )
