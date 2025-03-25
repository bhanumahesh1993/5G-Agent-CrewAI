from .base_agent import create_base_agent
from ..tools.anomaly_detector import AnomalyDetectorTool
from ..tools.metrics_extractor import MetricsExtractorTool

def create_anomaly_detection_agent(tools=None, allow_delegation=True, verbose=None):
    """
    Create an Anomaly Detection & Diagnosis Agent.
    
    This agent is responsible for detecting abnormal patterns in modem performance
    data and diagnosing the root causes of issues.
    
    Args:
        tools (list, optional): Additional tools for the agent
        allow_delegation (bool, optional): Whether the agent can delegate tasks
        verbose (bool, optional): Whether to enable verbose mode
        
    Returns:
        Agent: Configured Anomaly Detection & Diagnosis Agent
    """
    # Define agent details
    role = "Anomaly Detection & Diagnosis Agent"
    goal = "Identify, classify, and diagnose 5G modem performance issues with high accuracy and actionable context"
    backstory = (
        "You are an expert in network diagnostics with deep expertise in identifying "
        "and resolving 5G connection issues. Your background combines statistical analysis, "
        "machine learning, and telecommunications domain knowledge, making you exceptionally "
        "skilled at detecting subtle anomalies in network performance data. Your experience "
        "includes working with major telecom equipment manufacturers where you developed "
        "advanced diagnostic algorithms. You excel at classifying different types of network "
        "issues and tracing them to their root causes, providing clear explanations that help "
        "guide resolution efforts. Your analytical approach is both comprehensive and precise, "
        "ensuring no detail escapes your attention."
    )
    
    # Create standard tools if none provided
    if tools is None:
        tools = [
            AnomalyDetectorTool(),
            MetricsExtractorTool()
        ]
    
    # Create and return the agent
    return create_base_agent(
        role=role,
        goal=goal,
        backstory=backstory,
        tools=tools,
        allow_delegation=allow_delegation,
        verbose=verbose
    )
