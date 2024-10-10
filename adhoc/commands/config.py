import os
import json

CONFIG_FILE_PATH = os.path.join('.Adhoc', 'config.json')

def config_command(args):
    # Ensure the configuration directory exists
    if not os.path.exists('.Adhoc'):
        os.makedirs('.Adhoc')

    # Load existing configuration or create a new one
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'r') as f:
            config = json.load(f)
    else:
        config = {}

    # Update configuration based on arguments
    if args.document_format:
        format_map = {'md': 'markdown', 'tex': 'latex', 'word': 'word'}
        config['OUTPUT_FORMAT'] = format_map.get(args.document_format, 'latex')

    if args.username:
        config['AUTHOR_NAME'] = args.username

    # Save the updated configuration
    with open(CONFIG_FILE_PATH, 'w') as f:
        json.dump(config, f, indent=4)

    print("Configuration updated successfully.")
