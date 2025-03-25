from .base_agent import create_base_agent
from crewai_tools import SerperDevTool

def create_user_experience_agent(tools=None, allow_delegation=True, verbose=None):
    """
    Create a User Experience Enhancement Agent.
    
    This agent is responsible for analyzing how network issues impact the user 
    experience and suggesting improvements to prevent latency spikes and 
    dropped connections.
    
    Args:
        tools (list, optional): Additional tools for the agent
        allow_delegation (bool, optional): Whether the agent can delegate tasks
        verbose (bool, optional): Whether to enable verbose mode
        
    Returns:
        Agent: Configured User Experience Enhancement Agent
    """
    # Define agent details
    role = "User Experience Enhancement Agent"
    goal = "Proactively identify and mitigate potential user experience issues before they impact 5G modem users"
    backstory = (
        "You are an expert in telecommunications user experience with a strong "
        "background in both technical network analysis and human-centered design. "
        "You specialize in understanding how network parameters and performance metrics "
        "translate into actual user experiences for different types of applications. "
        "Your unique skill is anticipating how technical issues might manifest as user "
        "frustrations, and suggesting targeted optimizations that prioritize the most "
        "important aspects of user experience. You have extensive knowledge of how "
        "different applications (streaming, gaming, video calls, web browsing) have "
        "different network requirements, and how to optimize for each use case. Your "
        "recommendations always focus on real-world improvements that users will notice."
    )
    
    # Create standard tools if none provided
    if tools is None:
        tools = [
            SerperDevTool()  # Using search tool to gather UX best practices and requirements
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
