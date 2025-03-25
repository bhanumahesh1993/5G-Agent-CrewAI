import os
from dotenv import load_dotenv

def load_config():
    """
    Load configuration from environment variables.
    
    Returns:
        dict: Configuration values
    """
    # Ensure environment variables are loaded
    load_dotenv()
    
    # Create configuration dictionary
    config = {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "model_name": os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo"),
        "pcap_file": os.getenv("PCAP_FILE_PATH", "data/free5gc-compose.pcap"),
        "output_dir": os.getenv("OUTPUT_DIR", "output"),
        "verbose_level": int(os.getenv("VERBOSE_LEVEL", "1"))
    }
    
    return config

def validate_config(config):
    """
    Validate that all required configuration values are present.
    
    Args:
        config (dict): Configuration values
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check for required values
    if not config.get("openai_api_key"):
        return False, "OPENAI_API_KEY is not set in the environment variables or .env file"
    
    if not os.path.exists(config.get("pcap_file", "")):
        return False, f"PCAP file not found at {config.get('pcap_file')}"
    
    # If we get here, config is valid
    return True, ""
