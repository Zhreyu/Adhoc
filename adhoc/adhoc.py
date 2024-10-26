# Existing imports
import sys
import argparse

from .commands.init import init_command
from .commands.commit import commit_command
from .commands.generate import generate_command
from .commands.config import config_command  # New import
from .commands.startapi import run_server_command

def main():
    parser = argparse.ArgumentParser(
        prog='adhoc',
        description='Auto Document Codebase Changes'
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Init command
    parser_init = subparsers.add_parser('init', help='Initialize the codebase for adhoc tracking')
    parser_init.add_argument(
        '-m', '--model',
        type=str,
        default='llama3.1',
        help='Specify the model name (default: llama3.1)'
    )
    parser_init.set_defaults(func=init_command)

    # Commit command
    parser_commit = subparsers.add_parser('commit', help='Commit code changes and generate explanations')
    parser_commit.add_argument('-m', '--message', type=str, help='Optional commit message explaining the changes')
    parser_commit.set_defaults(func=commit_command)

    # Generate command
    parser_generate = subparsers.add_parser('generate', help='Generate documentation')
    parser_generate.set_defaults(func=generate_command)

    # Config command
    parser_config = subparsers.add_parser('config', help='Configure adhoc settings')
    parser_config.add_argument('-d', '--document-format', type=str, choices=['md', 'tex', 'word'],
                               help='Set the output document format (md, tex, word)')
    parser_config.add_argument('-u', '--username', type=str, help='Set the author username')
    parser_config.set_defaults(func=config_command)

    #? Start API command
    parser_startapi = subparsers.add_parser('startapi', help='Start the FastAPI server')

    # Add arguments for host, reloads, worker and port
    parser_startapi.add_argument('-p', '--port', type=int, default=8000, help='Port number to run the server on')
    parser_startapi.add_argument('-H', '--host', type=str, default='0.0.0.0', help='Host address to bind to')
    parser_startapi.add_argument('-r', '--reload', action='store_true', help='Enable auto-reload')
    parser_startapi.add_argument('-w', '--workers', type=int, default=1, help='Number of worker processes')

    parser_startapi.set_defaults(func=run_server_command)

    # Parse arguments
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    # Dispatch to the appropriate command function
    args.func(args)

if __name__ == '__main__':
    main()
