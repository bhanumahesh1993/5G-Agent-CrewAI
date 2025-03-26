from .base_agent import create_base_agent
from crewai_tools import SerperDevTool
import os

def create_optimization_agent(tools=None, allow_delegation=True, verbose=None):
    """
    Create an Optimization & Self-Healing Agent.
    
    This agent is responsible for suggesting or applying corrective measures
    to resolve detected network issues and optimize modem performance.
    
    Args:
        tools (list, optional): Additional tools for the agent
        allow_delegation (bool, optional): Whether the agent can delegate tasks
        verbose (bool, optional): Whether to enable verbose mode
        
    Returns:
        Agent: Configured Optimization & Self-Healing Agent
    """
    # Define agent details
    role = "Optimization & Self-Healing Agent"
    goal = "Develop and apply effective optimization strategies to enhance 5G modem performance and resolve detected issues"
    backstory = (
        "You are an expert in 5G network optimization with extensive experience in "
        "modem firmware, protocol tuning, and cellular network parameters. Your background "
        "includes working on cutting-edge 5G deployment projects where you developed innovative "
        "approaches to solving complex performance challenges. You have a deep understanding of "
        "radio frequency optimization, beam management, power control algorithms, and adaptive "
        "modulation techniques. Your specialty is translating technical diagnostics into practical, "
        "effective optimization strategies that measurably improve network performance. You pride "
        "yourself on your ability to recommend precise adjustments that balance multiple competing "
        "factors like throughput, latency, power efficiency, and connection stability."
    )
    
    # Create standard tools if none provided
    if tools is None:
        serper_api_key = os.getenv("SERPER_API_KEY", "your_serper_api_key_here")
        tools = [
            SerperDevTool(api_key=serper_api_key)  # Using search tool with provided API key
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
