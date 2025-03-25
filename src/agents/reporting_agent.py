from .base_agent import create_base_agent
from ..tools.pdf_generator import PDFGeneratorTool

def create_reporting_agent(tools=None, allow_delegation=True, verbose=None):
    """
    Create a Reporting & Insights Agent.
    
    This agent is responsible for generating comprehensive reports with performance
    trends, anomalies, and AI-driven optimizations for modem performance.
    
    Args:
        tools (list, optional): Additional tools for the agent
        allow_delegation (bool, optional): Whether the agent can delegate tasks
        verbose (bool, optional): Whether to enable verbose mode
        
    Returns:
        Agent: Configured Reporting & Insights Agent
    """
    # Define agent details
    role = "Reporting & Insights Agent"
    goal = "Create detailed, actionable reports that clearly communicate network performance, issues, and optimization recommendations"
    backstory = (
        "You are an expert in data visualization and technical communication with "
        "a specialty in translating complex network performance data into clear, "
        "insightful reports. Your background combines telecommunications expertise "
        "with data science and technical writing, allowing you to identify the most "
        "important patterns in large datasets and communicate them effectively to "
        "both technical and non-technical audiences. You excel at creating visual "
        "representations of data that highlight key insights and trends, and your "
        "written analyses are known for being comprehensive yet accessible. You have "
        "a talent for explaining technical concepts in plain language without sacrificing "
        "accuracy or detail, and for structuring information in a way that guides readers "
        "to the most important conclusions and actionable recommendations."
    )
    
    # Create standard tools if none provided
    if tools is None:
        tools = [
            PDFGeneratorTool()
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
