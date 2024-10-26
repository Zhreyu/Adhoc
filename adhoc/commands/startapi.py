import os
import argparse
import subprocess
import sys
from typing import Optional
import uvicorn
from pathlib import Path

def find_fastapi_app() -> Optional[str]:
    """
    Finds the api.py FastAPI application file in the current directory.
    Looks for common patterns like main.py, app.py, or api.py.
    
    Returns:
        str: The module path to the FastAPI app, or None if not found
    """
    common_names = ['main.py', 'app.py', 'api.py']
    
    # First, look in current directory
    for name in common_names:
        if os.path.exists(name):
            module_name = name.replace('.py', '')
            return f"{module_name}:app"
    
    # Then look in app directory
    if os.path.exists('app'):
        for name in common_names:
            if os.path.exists(os.path.join('app', name)):
                module_name = name.replace('.py', '')
                return f"app.{module_name}:app"
    
    return None

def run_server_command(args):
    API_PATH = './adhoc/api/api.py'
    """
    Command handler for running the FastAPI server
    
    Args:
        args: Parsed command line arguments containing:
            - port: Port number to run the server on
            - host: Host address to bind to
            - reload: Whether to enable auto-reload
            - workers: Number of worker processes
    """
    
    # If no app specified, try to find it
    app_path = API_PATH
    if not app_path:
        app_path = find_fastapi_app()
        if not app_path:
            print("Error: Could not find FastAPI application. Please specify with --app")
            return 1

    try:
        # Check if we're in a virtual environment
        in_venv = sys.prefix != sys.base_prefix
        if in_venv:
            print("Warning: Running in a virtual environment.")
            print("Consider running without a virtual environment for better performance.")
            
        # Check if required packages are installed
        try:
            import fastapi
            import uvicorn
        except ImportError:
            print("Error: Required packages not found. Please install fastapi and uvicorn:")
            print("pip install fastapi uvicorn")
            return 1
        
        # Print startup message
        print(f"\nStarting FastAPI server:")
        print(f"→ Application: {app_path}")
        print(f"→ Host: {args.host}")
        print(f"→ Port: {args.port}")
        print(f"→ Reload: {'enabled' if args.reload else 'disabled'}")
        print(f"→ Workers: {args.workers}")
        print("\nAPI documentation will be available at:")
        print(f"→ Swagger UI: http://{args.host}:{args.port}/docs")
        print(f"→ ReDoc: http://{args.host}:{args.port}/redoc")
        print("\n Api will be available at: http://{args.host}:{args.post}/ \n ") 
        print("\nPress Ctrl+C to stop the server\n")

        # Run the server
        uvicorn.run(
            app_path,
            host=args.host,
            port=args.port,
            reload=args.reload,
            workers=args.workers,
            log_level="info"
        )
        
    except Exception as e:
        print(f"Error running server: {str(e)}")
        return 1
    
    return 0
