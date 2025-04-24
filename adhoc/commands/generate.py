from ..db.database import get_explanations
from ..utils.latex_utils import render_latex_document
from ..utils.markdown_utils import render_markdown_document
from ..utils.word_utils import render_word_document
from ..utils.config_utils import load_config  # Import the config loader
from ..db.database import get_codebase_summary


def generate_command(args):
    config = load_config()
    OUTPUT_FORMAT = config.get('OUTPUT_FORMAT', 'latex')
    AUTHOR_NAME = config.get('AUTHOR_NAME', 'Default Author')
    explanations = get_explanations()
    codebase_summary = get_codebase_summary()
    FOLDER_PATH = "output/"

    # Pass AUTHOR_NAME to rendering functions if needed

    # Determine the output format
    if OUTPUT_FORMAT == 'latex':
        latex_content = render_latex_document(explanations, codebase_summary, AUTHOR_NAME)
        output_filename = 'documentation.tex'
        file_path = FOLDER_PATH + output_filename
        with open(file_path, 'w') as f:
            f.write(latex_content)
        print(f"LaTeX documentation generated: {file_path}")
    elif OUTPUT_FORMAT == 'markdown':
        markdown_content = render_markdown_document(explanations, codebase_summary, AUTHOR_NAME)
        output_filename = 'documentation.md'
        file_path = FOLDER_PATH + output_filename
        with open(file_path, 'w') as f:
            f.write(markdown_content)
        print(f"Markdown documentation generated: {output_filename}")
    elif OUTPUT_FORMAT == 'word':
        output_filename = "documentation.docx"
        render_word_document(explanations, codebase_summary, file_path, AUTHOR_NAME)
        print(f"Word documentation generated: {output_filename}")
        
    else:
        print(f"Unsupported output format: {OUTPUT_FORMAT}")
