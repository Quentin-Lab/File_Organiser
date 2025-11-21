from pathlib import Path
from datetime import datetime
import shutil
import zipfile
import json

def scan_directory_for_files(directory):
    """
    List all files in a directory, ignoring subfolders.

    Args:
        directory (Path): Path to the directory to scan.

    Returns:
        list[Path]: List of file paths found in the directory.
    """
    files_paths_list = []
    for element in directory.iterdir():
        if element.is_file():
            files_paths_list.append(element)
    return(files_paths_list)

def create_directory_if_missing(path: Path):
    """
    Ensure a directory exists, creating it along with parent directories if needed.

    Args:
        path (Path): Path to the directory.
    """
    path.mkdir(parents=True, exist_ok=True)

def resolve_file_conflict(src, destination_folder):
    """
    Resolve file name conflicts in the destination folder by appending a counter.

    Args:
        src (Path): Source file path.
        destination_folder (Path): Target folder where file will be moved.

    Returns:
        Path: Safe destination path with a unique file name.
    """
    safe_path = destination_folder / src.name
    counter = 1
    while safe_path.exists():
        stem = src.stem
        suffix = src.suffix
        safe_path = destination_folder / f"{stem}_{counter}{suffix}"
        counter += 1

    return safe_path

def move_file(src, dest):
    """
    Move a file to the destination path, ensuring parent directories exist.

    Args:
        src (Path): Source file path.
        dest (Path): Destination file path.

    Returns:
        bool: True if file was successfully moved, False otherwise.
    """
    create_directory_if_missing(dest.parent)
    shutil.move(src, dest)
    
def creating_back_up(files_list, backup_folder):
    """
    Create a zip with all the file before moving them.
    Args:
        files_list (list) all the files that need to be saved before being moved.
        backup_folder (path) path to the backupfolder (should be the one he want to clean)
    """
    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    name_zip_file = f"user_backup_{timestamp}.zip"
    archive_name = backup_folder.joinpath(name_zip_file)
    
    files_to_backup = [f for f in files_list if f.exists() and f.is_file()]

    if not files_to_backup:
        print("No valid files to back up in this folder.")
        return
    
    with zipfile.ZipFile(archive_name, mode='w') as zipf:
        for file in files_to_backup:
            zipf.write(file, arcname = file.name)

    print(f"Backup created: {archive_name}")

def get_rules(json_path: Path):
    with json_path.open(encoding="utf-8") as f:
        rules = json.load(f)
    return rules   
