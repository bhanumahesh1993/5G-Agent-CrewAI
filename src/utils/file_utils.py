import os
import shutil
from datetime import datetime

def check_pcap_file(file_path):
    """
    Check if the PCAP file exists and is readable.
    
    Args:
        file_path (str): Path to the PCAP file
        
    Returns:
        bool: True if file exists and is readable, False otherwise
    """
    # Check if file exists
    if not os.path.exists(file_path):
        return False
    
    # Check if file is readable
    try:
        with open(file_path, 'rb') as f:
            # Try to read a small part of the file
            f.read(1024)
        return True
    except Exception:
        return False

def ensure_output_dir(output_dir):
    """
    Ensure the output directory exists, creating it if necessary.
    
    Args:
        output_dir (str): Path to the output directory
        
    Returns:
        str: Path to the output directory
    """
    # Create directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    return output_dir

def create_timestamped_output_dir(base_dir):
    """
    Create a timestamped output directory for this run.
    
    Args:
        base_dir (str): Base output directory
        
    Returns:
        str: Path to the timestamped output directory
    """
    # Ensure base directory exists
    ensure_output_dir(base_dir)
    
    # Create timestamped directory name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(base_dir, f"analysis_{timestamp}")
    
    # Create the directory
    os.makedirs(output_dir)
    
    return output_dir

def save_intermediate_result(data, filename, output_dir):
    """
    Save intermediate results to a file.
    
    Args:
        data (str): Data to save
        filename (str): Name of the file
        output_dir (str): Directory to save the file in
        
    Returns:
        str: Path to the saved file
    """
    # Ensure output directory exists
    ensure_output_dir(output_dir)
    
    # Create file path
    file_path = os.path.join(output_dir, filename)
    
    # Save the data
    with open(file_path, 'w') as f:
        f.write(data)
    
    return file_path
