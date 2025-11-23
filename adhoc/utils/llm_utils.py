import requests
from requests.exceptions import RequestException
from ..utils.config_utils import load_config

def send_to_llm(prompt):
    config = load_config()
    provider = config.get('LLM_PROVIDER', 'ollama')
    model_name = config.get('MODEL_NAME', 'llama3.1')
    
    if provider == 'openai':
        return _send_to_openai_style_api(prompt, config, model_name)
    else:
        return _send_to_ollama(prompt, config, model_name)

def _send_to_ollama(prompt, config, model_name):
    """Send request to Ollama API"""
    api_endpoint = config.get('OLLAMA_API_ENDPOINT', 'http://localhost:11434/api/generate/')
    payload = {
        'prompt': prompt,
        'model': model_name,
        'stream': False
    }

    try:
        response = requests.post(api_endpoint, json=payload)
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

def _send_to_openai_style_api(prompt, config, model_name):
    """Send request to OpenAI-style API (OpenAI, OpenRouter, LiteLLM, etc.)"""
    api_endpoint = config.get('OPENAI_API_ENDPOINT', 'https://api.openai.com/v1/chat/completions')
    api_key = config.get('OPENAI_API_KEY', '')
    
    if not api_key:
        print("Error: OPENAI_API_KEY is not configured. Please set it using 'adhoc config --api-key YOUR_KEY'")
        return ''
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': model_name,
        'messages': [
            {'role': 'user', 'content': prompt}
        ],
        'stream': False
    }

    try:
        response = requests.post(api_endpoint, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
    except ValueError as ve:
        print(f"JSON decoding failed: {ve}")
        print(f"Response content: {response.text}")
        return ''
    except RequestException as e:
        print(f"Error connecting to OpenAI-style API: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response content: {e.response.text}")
        return ''
    except (KeyError, IndexError) as e:
        print(f"Unexpected response format: {e}")
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
