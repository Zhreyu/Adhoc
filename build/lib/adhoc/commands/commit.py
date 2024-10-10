import os
import shutil
from ..utils.llm_utils import generate_change_explanation
from ..utils.diff_utils import get_code_diffs
from ..utils.llm_utils import generate_explanation
from ..db.database import get_codebase_summary,get_connection, save_explanations

def commit_command(args):
    codebase_summary = get_codebase_summary()
    diffs = get_code_diffs(
        '.Adhoc/original_codebase',
        '.',
        exclude_dirs=['.Adhoc', '__pycache__', '.git']
    )

    if not diffs:
        print('No changes detected.')
        return

    # For each changed file, generate explanations and store in the database
    conn = get_connection()
    cursor = conn.cursor()

    explanations = []
    for diff in diffs:
        explanation = generate_change_explanation(codebase_summary, diff)
        explanations.append({
            'file_path': diff['file_path'],
            'explanation': explanation
        })

    # Save explanations to database
    save_explanations(explanations)

    # print("Changes committed and explanations generated.")

    print(f"Changes in {diff['file_path']} committed.")

    conn.commit()
    conn.close()

    # Update the original codebase snapshot
    shutil.rmtree('.Adhoc/original_codebase')
    shutil.copytree(
        '.',
        '.Adhoc/original_codebase',
        ignore=shutil.ignore_patterns('.Adhoc', '__pycache__', '*.pyc', '.git')
    )

    print('Original codebase snapshot updated.')