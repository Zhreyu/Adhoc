import re
from jinja2 import Environment, BaseLoader
import importlib.resources
import os
from ..db.database import get_codebase_summary

def markdown_to_latex(text):
    # Convert bold **text** to \textbf{text}
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    # Convert italic *text* to \textit{text}
    text = re.sub(r'\*(.+?)\*', r'\\textit{\1}', text)
    # Convert inline code `code` to \texttt{code}
    text = re.sub(r'`(.+?)`', r'\\texttt{\1}', text)
    # Convert headings
    text = re.sub(r'^# (.+)$', r'\\section*{\1}', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'\\subsection*{\1}', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'\\subsubsection*{\1}', text, flags=re.MULTILINE)
    # Convert lists
    text = re.sub(r'^\* (.+)$', r'\\item \1', text, flags=re.MULTILINE)
    # Wrap lists in itemize environment
    text = re.sub(r'(\\item .+(\n)?)+', lambda m: '\\begin{itemize}\n' + m.group() + '\\end{itemize}\n', text, flags=re.MULTILINE)
    return text


def render_latex_document(explanations,codebase_summary,author_name):
    # Read the template content from package resources
    with importlib.resources.open_text('adhoc.templates', 'document_template.tex') as f:
        template_content = f.read()
    env = Environment(loader=BaseLoader())
    template = env.from_string(template_content)
    codebase_summary = get_codebase_summary()
    if codebase_summary:
        # Escape LaTeX special characters and convert Markdown to LaTeX if needed
        codebase_summary = escape_latex_special_chars(codebase_summary)
        codebase_summary = markdown_to_latex(codebase_summary)
    else:
        codebase_summary = "No codebase summary available."

    escaped_explanations = []
    for item in explanations:
        escaped_item = {
            'file_path': escape_latex_special_chars(item['file_path']),
            'explanation': escape_latex_special_chars(item['explanation']),
            'timestamp': item['timestamp']
        }
        if 'commit_message' in item:
            escaped_item['commit_message'] = escape_latex_special_chars(item['commit_message'])
        escaped_explanations.append(escaped_item)

    context = {
        'author_name': author_name,
        'codebase_summary': codebase_summary,
        'explanations': escaped_explanations
    }

    latex_content = template.render(context)
    return latex_content




def escape_latex_special_chars(text):
    """
    Escapes LaTeX special characters in the given text.
    """
    # Define the mapping of special characters
    special_chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
    }
    
    # Use a regular expression to replace each special character
    regex = re.compile('|'.join(re.escape(key) for key in special_chars.keys()))
    escaped_text = regex.sub(lambda match: special_chars[match.group()], text)
    return escaped_text

