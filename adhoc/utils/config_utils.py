import os
import json

ADHOC_DIR = os.path.join(os.getcwd(), '.Adhoc')
CONFIG_FILE_PATH = os.path.join(ADHOC_DIR, 'config.json')

def load_config():
    # Load existing configuration or create defaults
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'r') as f:
            config = json.load(f)
    else:
        config = {}
    
    # Ensure all default keys exist (for backward compatibility)
    config.setdefault("OLLAMA_API_ENDPOINT", "http://localhost:11434/api/generate/")
    config.setdefault("MODEL_NAME", "llama3.1")
    config.setdefault("OUTPUT_FORMAT", "latex")
    config.setdefault("AUTHOR_NAME", "Default Author")
    config.setdefault("LLM_PROVIDER", "ollama")
    config.setdefault("OPENAI_API_ENDPOINT", "https://api.openai.com/v1/chat/completions")
    config.setdefault("OPENAI_API_KEY", "")
    
    return config
