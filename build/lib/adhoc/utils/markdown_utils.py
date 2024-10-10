import os
from jinja2 import Environment, FileSystemLoader
import re

def escape_markdown_special_chars(text):
    """
    Escapes Markdown special characters in the given text.
    """
    special_chars = {
        '*': r'\*',
        '_': r'\_',
        '`': r'\`',
        '[': r'\[',
        ']': r'\]',
        '#': r'\#',
        '+': r'\+',
        '-': r'\-',
        '!': r'\!',
    }
    regex = re.compile('|'.join(re.escape(key) for key in special_chars.keys()))
    escaped_text = regex.sub(lambda match: special_chars[match.group()], text)
    return escaped_text

def render_markdown_document(explanations, codebase_summary,author_name):
    # Get the absolute path to the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(script_dir, '..', 'templates')
    templates_dir = os.path.abspath(templates_dir)
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template('document_template.md')

    # Escape special characters in explanations
    escaped_explanations = []
    for item in explanations:
        explanation_text = escape_markdown_special_chars(item['explanation'])
        escaped_item = {
            'file_path': escape_markdown_special_chars(item['file_path']),
            'explanation': explanation_text,
            'timestamp': item['timestamp']
        }
        if 'commit_message' in item:
            commit_message = escape_markdown_special_chars(item['commit_message'])
            escaped_item['commit_message'] = commit_message
        escaped_explanations.append(escaped_item)

    # Prepare context
    context = {
        'author_name': author_name,
        'codebase_summary': escape_markdown_special_chars(codebase_summary),
        'explanations': escaped_explanations
    }

    markdown_content = template.render(context)
    return markdown_content
