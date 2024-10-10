import time
import os
import sys
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from ..utils.diff_utils import get_code_diffs
from ..utils.llm_utils import generate_explanation
from ..db.database import get_connection
from ..utils.latex_utils import render_latex_document

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("Adhoc.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

class AdocEventHandler(FileSystemEventHandler):
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.Adhoc_dir = os.path.join(project_dir, '.Adhoc')

    def on_modified(self, event):
        if event.is_directory:
            return
        if '.Adhoc' in event.src_path:
            return
        logging.info(f"Detected modification: {event.src_path}")
        self.handle_change()

    def on_created(self, event):
        if event.is_directory:
            return
        if '.Adhoc' in event.src_path:
            return
        logging.info(f"Detected creation: {event.src_path}")
        self.handle_change()

    def on_deleted(self, event):
        if event.is_directory:
            return
        if '.Adhoc' in event.src_path:
            return
        logging.info(f"Detected deletion: {event.src_path}")
        self.handle_change()

    def handle_change(self):
        try:
            # Get diffs
            diffs = get_code_diffs(
                os.path.join(self.Adhoc_dir, 'original_codebase'),
                self.project_dir,
                exclude_dirs=['.Adhoc', '__pycache__', '.git']
            )

            if not diffs:
                logging.info('No changes detected.')
                return

            # Process each diff
            conn = get_connection()
            cursor = conn.cursor()

            for diff in diffs:
                # Generate explanation using LLM
                explanation = generate_explanation(
                    diff.get('old_code', ''),
                    diff.get('new_code', ''),
                    diff['file_path']
                )

                # Insert into the database
                cursor.execute(
                    '''
                    INSERT INTO changes (file_path, change_type, old_code, new_code, explanation, user_message)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''',
                    (
                        diff['file_path'],
                        diff['change_type'],
                        diff.get('old_code', ''),
                        diff.get('new_code', ''),
                        explanation,
                        None  # No user message in auto-commit
                    )
                )

                logging.info(f"Changes in {diff['file_path']} committed.")

            conn.commit()
            conn.close()

            # Update the original codebase snapshot
            import shutil
            shutil.rmtree(os.path.join(self.Adhoc_dir, 'original_codebase'))
            shutil.copytree(
                self.project_dir,
                os.path.join(self.Adhoc_dir, 'original_codebase'),
                ignore=shutil.ignore_patterns('.Adhoc', '__pycache__', '*.pyc', '.git')
            )

            # Optionally, regenerate documentation
            render_latex_document_from_db(self.project_dir)
        except Exception as e:
            logging.error(f"Error handling change: {e}", exc_info=True)

def render_latex_document_from_db(project_dir):
    from db.database import get_connection
    from utils.latex_utils import render_latex_document

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT file_path, change_type, old_code, new_code, explanation FROM changes'
        )
        changes = cursor.fetchall()

        conn.close()

        if not changes:
            logging.info('No changes to document.')
            return

        # Prepare data for LaTeX rendering
        changes_data = []
        for change in changes:
            changes_data.append({
                'file_path': change[0],
                'change_type': change[1],
                'old_code': change[2],
                'new_code': change[3],
                'explanation': change[4]
            })

        # Render the LaTeX document
        output_path = os.path.join(project_dir, 'Adhoc_documentation.tex')
        render_latex_document(changes_data, output_path)

        logging.info(f'Documentation generated at {output_path}')
    except Exception as e:
        logging.error(f"Error generating LaTeX document: {e}", exc_info=True)

def watch_command(args):
    project_dir = os.getcwd()
    Adhoc_dir = os.path.join(project_dir, '.Adhoc')

    if not os.path.exists(Adhoc_dir):
        logging.error("Adoc is not initialized in this directory. Please run 'Adhoc init' first.")
        sys.exit(1)

    event_handler = AdocEventHandler(project_dir)
    observer = Observer()
    observer.schedule(event_handler, path=project_dir, recursive=True)
    observer.start()
    logging.info(f"Started watching {project_dir} for changes. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    logging.info("Stopped watching for changes.")