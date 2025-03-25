#!/usr/bin/env python3
"""
5G Modem Intelligence Crew - Main Application

This script runs a multi-agent AI system that analyzes 5G modem performance,
detects anomalies, generates optimization recommendations, and creates
comprehensive reports.
"""
import os
import sys
import argparse
import json
from datetime import datetime
import logging


# Add the project directory to the path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Import project modules
from src.utils import load_config, check_pcap_file, ensure_output_dir, setup_logger
from src.crews.modem_intelligence_crew import create_modem_intelligence_crew

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="5G Modem Intelligence Crew - AI-powered modem performance analysis"
    )
    
    parser.add_argument(
        "--pcap", 
        dest="pcap_file", 
        help="Path to the PCAP file for analysis"
    )
    
    parser.add_argument(
        "--output-dir", 
        dest="output_dir",
        help="Directory to save analysis results"
    )
    
    parser.add_argument(
        "--verbose", 
        dest="verbose", 
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--model", 
        dest="model_name",
        help="OpenAI model to use (e.g., gpt-3.5-turbo, gpt-4)"
    )
    
    return parser.parse_args()

def main():
    """Main application entry point."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Load configuration
    config = load_config()
    
    # Override config with command line arguments if provided
    if args.pcap_file:
        config["pcap_file"] = args.pcap_file
    if args.output_dir:
        config["output_dir"] = args.output_dir
    if args.verbose:
        config["verbose_level"] = 2
    if args.model_name:
        config["model_name"] = args.model_name
    
    # Set up logging
    log_file = os.path.join(config["output_dir"], f"modem_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    logger = setup_logger(log_file=log_file, level=logging.INFO if config["verbose_level"] > 0 else logging.WARNING)
    
    # Ensure the PCAP file exists
    if not check_pcap_file(config["pcap_file"]):
        logger.error(f"PCAP file not found or not readable: {config['pcap_file']}")
        sys.exit(1)
    
    # Ensure the output directory exists
    ensure_output_dir(config["output_dir"])
    
    logger.info("Starting 5G Modem Intelligence Crew analysis")
    logger.info(f"PCAP file: {config['pcap_file']}")
    logger.info(f"Output directory: {config['output_dir']}")
    logger.info(f"Using model: {config['model_name']}")
    
    try:
        # Create the modem intelligence crew
        crew = create_modem_intelligence_crew(verbose=config["verbose_level"])
        
        # Set up input data for the crew
        crew_inputs = {
            "pcap_file": config["pcap_file"],
            "output_dir": config["output_dir"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Run the crew
        logger.info("Running modem intelligence analysis...")
        result = crew.kickoff(inputs=crew_inputs)
        
        # Save the result
        result_file = os.path.join(config["output_dir"], "analysis_result.json")
        with open(result_file, 'w') as f:
            json.dump({"result": str(result)}, f, indent=2)
        
        logger.info(f"Analysis completed successfully. Results saved to {config['output_dir']}")
        logger.info(f"Final result: {result}")
        
        print("\n✅ Analysis completed successfully!")
        print(f"Results saved to {config['output_dir']}")
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}", exc_info=True)
        print(f"\n❌ Error during analysis: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    import logging
    main()
