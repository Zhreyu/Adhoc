import json
import os
import shutil
import os

from ..utils.config_utils import CONFIG_FILE_PATH

from ..db.database import initialize_database, save_codebase_summary
from ..utils.llm_utils import generate_codebase_summary

def collect_codebase_content():
    codebase_content = ""
    for root, dirs, files in os.walk('.'):
        for file in files:
            file_path = os.path.join(root, file)
            # Skip non-text files
            if not is_text_file(file_path):
                continue

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                codebase_content += f"\n\n# File: {file_path}\n"
                codebase_content += f.read()
    return codebase_content

def is_text_file(file_path):
    import mimetypes
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith('text')


def init_command(args):
    # Create necessary directories
    if not os.path.exists('.Adhoc'):
        os.makedirs('.Adhoc')
        print('Initialized .Adhoc directory for tracking.')

        # Initialize the database
        initialize_database()
        print('Database initialized.')

        # Copy the current codebase as the initial snapshot
        shutil.copytree(
            '.',
            '.Adhoc/original_codebase',
            ignore=shutil.ignore_patterns('.Adhoc', '__pycache__', '*.pyc', '.git')
        )
            # Collect the entire codebase
        codebase_content = collect_codebase_content()

        # Generate summary of the codebase
        codebase_summary = generate_codebase_summary(codebase_content)

        # Save the summary to the database
        save_codebase_summary(codebase_summary)
        print('Original codebase snapshot created.')

    else:
        print('Adoc has already been initialized in this directory.')
    
    # print(f"Checking if config file exists at {CONFIG_FILE_PATH}")  # Debugging statement
    if not os.path.exists(CONFIG_FILE_PATH):
        # print("Config file does not exist. Creating default config.json...")  # Debugging statement
        default_config = {
            "OLLAMA_API_ENDPOINT": "http://localhost:11434/api/generate/",
            "MODEL_NAME": args.model,
            "OUTPUT_FORMAT": "latex",
            "AUTHOR_NAME": "Default Author"
        }
        with open(CONFIG_FILE_PATH, 'w') as f:
            json.dump(default_config, f, indent=4)
        print("Created default configuration file.")
    else:
        print("Configuration file already exists.")
    
    with open(CONFIG_FILE_PATH, 'r') as f:
            config = json.load(f)

    if config.get("MODEL_NAME") != args.model:
        config["MODEL_NAME"] = args.model
        with open(CONFIG_FILE_PATH, 'w') as f:
            json.dump(config, f, indent=4)