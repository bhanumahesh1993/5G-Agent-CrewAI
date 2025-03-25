#!/usr/bin/env python3
"""
5G Modem Intelligence Crew - Analysis Runner

A simple script to start the modem performance analysis.
"""
import sys
import os

# Run the main application
if __name__ == "__main__":
    # Add the project directory to the path
    project_dir = os.path.dirname(os.path.abspath(__file__))
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)
    
    # Import and run the main application
    from src.main import main
    main()
