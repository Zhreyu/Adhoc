import os
import difflib

def get_language(file_path):
    ext = os.path.splitext(file_path)[1]
    languages = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.java': 'Java',
        '.cpp': 'C++',
        '.c': 'C',
        '.rb': 'Ruby',
        # Add more as needed
    }
    return languages.get(ext, 'text')

def get_code_diffs(original_dir, current_dir, exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = []

    diffs = []

    # Create sets of all file paths
    original_files = set()
    for root, dirs, files in os.walk(original_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            path = os.path.relpath(os.path.join(root, file), original_dir)
            original_files.add(path)

    current_files = set()
    for root, dirs, files in os.walk(current_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            path = os.path.relpath(os.path.join(root, file), current_dir)
            current_files.add(path)

    # Detect deleted files
    deleted_files = original_files - current_files
    for file_path in deleted_files:
        original_file_path = os.path.join(original_dir, file_path)
        with open(original_file_path, 'r', encoding='utf-8', errors='ignore') as f_original:
            original_content = f_original.read()
        diffs.append({
            'file_path': file_path,
            'change_type': 'deleted',
            'old_code': original_content,
            'new_code': '',
            'diff': '',
            'language': get_language(file_path)
        })

    # Detect new and modified files
    for file_path in current_files:
        current_file_path = os.path.join(current_dir, file_path)
        original_file_path = os.path.join(original_dir, file_path)

        if os.path.exists(original_file_path):
            # Compare files
            with open(current_file_path, 'r', encoding='utf-8', errors='ignore') as f_current, open(original_file_path, 'r', encoding='utf-8', errors='ignore') as f_original:
                current_content = f_current.readlines()
                original_content = f_original.readlines()

            if current_content != original_content:
                diff = difflib.unified_diff(
                    original_content,
                    current_content,
                    fromfile='original',
                    tofile='current',
                    lineterm=''
                )
                diff_text = '\n'.join(list(diff))
                diffs.append({
                    'file_path': file_path,
                    'change_type': 'modified',
                    'old_code': ''.join(original_content),
                    'new_code': ''.join(current_content),
                    'diff': diff_text,
                    'language': get_language(file_path)
                })
        else:
            # New file added
            with open(current_file_path, 'r', encoding='utf-8', errors='ignore') as f_current:
                current_content = f_current.read()

            diffs.append({
                'file_path': file_path,
                'change_type': 'added',
                'old_code': '',
                'new_code': current_content,
                'diff': '',
                'language': get_language(file_path)
            })

    return diffs