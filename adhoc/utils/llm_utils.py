import requests
from requests.exceptions import RequestException
from ..utils.config_utils import load_config
config = load_config()
MODEL_NAME = config.get('MODEL_NAME', 'llama3.1')
OLLAMA_API_ENDPOINT = config.get('OLLAMA_API_ENDPOINT', 'http://localhost:11434/api/generate/')
def send_to_llm(prompt):
    payload = {
        'prompt': prompt,
        'model': MODEL_NAME,
        'stream': False
    }

    try:
        response = requests.post(OLLAMA_API_ENDPOINT, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get('response', '')
    except ValueError as ve:
        print(f"JSON decoding failed: {ve}")
        print(f"Response content: {response.text}")
        return ''
    except RequestException as e:
        print(f"Error connecting to Ollama LLM: {e}")
        return ''


def generate_codebase_summary(codebase_content):
    prompt = f"Provide a detailed summary and explanation of the following codebase:\n{codebase_content}"
    summary = send_to_llm(prompt)
    return summary

def generate_change_explanation(codebase_summary, diff):
    prompt = f"""
    Based on the following overall codebase description:

    {codebase_summary}

    Explain why the following changes were made:

    File: {diff['file_path']}
    Changes:
    {diff['diff']}
    """
    explanation = send_to_llm(prompt)
    return explanation


def generate_explanation(old_code, new_code, file_path):
    prompt = f"Explain the changes made in the file {file_path}:\n\n"
    if old_code:
        prompt += f"Before:\n{old_code}\n\n"
    else:
        prompt += "Before: (This is a new file)\n\n"

    prompt += f"After:\n{new_code}\n\n"
    prompt += "Explanation:"

    # Use send_to_llm function
    explanation = send_to_llm(prompt)
    return explanation.strip()
