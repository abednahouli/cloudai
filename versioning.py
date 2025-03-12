# versioning.py

import os
import datetime

def save_versioned_file(directory, base_filename, content, ext):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    versioned_filename = f"{base_filename}_{timestamp}.{ext}"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, versioned_filename)
    with open(file_path, "w") as f:
        f.write(content)
    return file_path

def list_versions(directory):
    if not os.path.exists(directory):
        return []
    return sorted(os.listdir(directory), reverse=True)

def restore_version(directory, index):
    versions = list_versions(directory)
    if not versions or index >= len(versions):
        return None
    version_file = os.path.join(directory, versions[index])
    with open(version_file, "r") as f:
        content = f.read()
    return content, versions[index]

def get_newest_terraform_file(directory):
    """
    Returns the path to the newest .tf file in the given directory,
    or None if the directory is empty or contains no .tf files.
    """
    if not os.path.exists(directory):
        return None
    # Sort in descending order by filename, so the newest (largest timestamp) is first
    files = sorted(os.listdir(directory), reverse=True)
    tf_files = [f for f in files if f.endswith(".tf")]
    if not tf_files:
        return None
    newest_file = tf_files[0]
    return os.path.join(directory, newest_file)
