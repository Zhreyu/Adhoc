import os
import json

ADHOC_DIR = os.path.join(os.getcwd(), '.Adhoc')
CONFIG_FILE_PATH = os.path.join(ADHOC_DIR, 'config.json')

def load_config():
    # Load existing configuration or return defaults
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'r') as f:
            config = json.load(f)
    else:
        # Default configuration
        config = {}
        config.setdefault("OLLAMA_API_ENDPOINT", "http://localhost:11434/api/generate/")
        config.setdefault("MODEL_NAME", "llama3.1")
        config.setdefault("OUTPUT_FORMAT", "latex")
        config.setdefault("AUTHOR_NAME", "Default Author")
    return config
