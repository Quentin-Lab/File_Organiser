from pathlib import Path
import shutil

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
    try:
        shutil.move(src, dest)
        return True
    except Exception as e:
        print(f"Could not move {src}: {e}")
        return False
    
