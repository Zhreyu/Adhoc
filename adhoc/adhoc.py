# Existing imports
import sys
import argparse

from .commands.init import init_command
from .commands.commit import commit_command
from .commands.generate import generate_command
from .commands.config import config_command  # New import

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
    parser_config.add_argument('-p', '--provider', type=str, choices=['ollama', 'openai'],
                               help='Set the LLM provider (ollama or openai)')
    parser_config.add_argument('-k', '--api-key', type=str, help='Set the OpenAI API key')
    parser_config.add_argument('-e', '--api-endpoint', type=str, 
                               help='Set the OpenAI API endpoint (for custom model routers)')
    parser_config.add_argument('-m', '--model', type=str, help='Set the model name')
    parser_config.set_defaults(func=config_command)

    # Parse arguments
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    # Dispatch to the appropriate command function
    args.func(args)

if __name__ == '__main__':
    main()
