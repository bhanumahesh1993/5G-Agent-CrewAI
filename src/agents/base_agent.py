from crewai import Agent
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def create_base_agent(
    role, 
    goal, 
    backstory, 
    tools=None, 
    allow_delegation=True, 
    verbose=None
):
    """
    Create a base agent with common configuration.
    """
    # Get environment variables
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
    verbose_level = int(os.getenv("VERBOSE_LEVEL", "1")) if verbose is None else verbose
    
    # Create the LLM
    llm = ChatOpenAI(
        model_name=model_name, 
        temperature=0.7
    )
    
    # Structure based on error messages
    agent_config = {
        # Required top-level fields
        "role": role,
        "goal": goal,
        "backstory": backstory,
        
        # Other fields
        "verbose": verbose_level,
        "allow_delegation": allow_delegation,
        "llm": llm
    }
    
    # Add tools if provided
    if tools:
        agent_config["tools"] = tools
    
    # Try to create the agent
    try:
        return Agent(**agent_config)
    except Exception as e:
        print(f"Agent creation error: {e}")
        
        # Let's try a minimal approach as fallback
        return Agent(
            role=role,
            goal=goal,
            backstory=backstory
        )