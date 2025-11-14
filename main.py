import sys
import shutil
from pathlib import Path
from collections import defaultdict

# --- Config console for UTF-8 support (Windows) ---
sys.stdout.reconfigure(encoding='utf-8')

# --- Reception function ---
def welcoming_message():
    """Displays a welcome message to the user."""
    print("Hello and thanks for using this script.\n")


# --- User directory selection function ---
def ask_user_for_directory():
    """
    Asks the user to provide the path to a directory to be cleaned.
    Checks that:
      - the path exists,
      - it belongs to the current user session,
      - it is not a file but a folder.
    Returns: Path(absolute path to the directory) or None if the user quits.
    """
    allowed_base_path = Path.home()

    while True:
        target_directory = input("Please give me the path to the directory you want to clean e.g C:\\Users\\Home\\Downloads :")
        if target_directory == "leave":
            print("Leaving programm...")
            return None

        absolute_selected_directory = Path(target_directory).resolve()

        if absolute_selected_directory.exists():
            try:
                absolute_selected_directory.relative_to(allowed_base_path)
                if absolute_selected_directory.is_file():
                    print("Please note that you have specified a file: please specify a path.")
                elif absolute_selected_directory.is_dir():
                    if "AppData" in absolute_selected_directory.parts:
                        print("Access to system folders like AppData is not allowed.")
                        continue
                    return(absolute_selected_directory)
            except ValueError:
                print("Select a directory that is present in your user session.")         
        else:
            print("Oops, the path you specified does not exist!")

# --- Listing the files present in a directory function ---
def scan_directory_for_files(directory):
    """ Return a list of files (ignoring subfolders) in the given directory"""
    files_paths_list = []
    for element in directory.iterdir():
        if element.is_file():
            files_paths_list.append(element)
    return(files_paths_list)

# --- Ensuring that Directories for triage exist ---
def create_directory_if_missing(path: Path):
    """ Creating the folder and parent if it does not exist"""
    path.mkdir(parents=True, exist_ok=True)

# --- Dealing with file with the same name
def resolve_file_conflict(src, destination_folder):
    safe_path = destination_folder / src.name
    counter = 1
    while safe_path.exists():
        stem = src.stem
        suffix = src.suffix
        safe_path = destination_folder / f"{stem}_{counter}{suffix}"
        counter += 1

    return safe_path


# --- Getting the destination for the file ---
def get_destination(file_path, extension_to_folder):
    home_path = Path.home()
    file_extension = file_path.suffix[1:]
    if file_extension in extension_to_folder:
        destination_path = home_path / extension_to_folder[file_extension]
    else:
        destination_path = home_path / "File_Triage" / "Autres"
    return destination_path 

# --- Moving a file ---
def move_file(src, dest):
    create_directory_if_missing(dest.parent)
    try:
        shutil.move(src, dest)
        return True
    except Exception as e:
        print(f"Could not move {src}: {e}")
        return False
    
# --- Display the stat ---
def display_summary(stats):
    total_files = sum(stats.values())
    print(f"\n Total filed moved: {total_files}")
    for (key, value) in stats.items():
        print(f"{key} : {value} files moved")
# --- Main function --- 

def main():
    welcoming_message()
    selected_directory = ask_user_for_directory()
    if selected_directory == None:
        print("None: Program will stop now.")
    else:
        extension_to_folder = {
            "pdf": Path("File_Triage") / "Documents",
            "doc": Path("File_Triage") / "Documents",
            "jpeg": Path("File_Triage") / "Images",
            "jpg": Path("File_Triage") / "Images",
            "png": Path("File_Triage") / "Images",
            "mp4": Path("File_Triage") / "Vidéos",
            "mkv": Path("File_Triage") / "Vidéos",
            "exe": Path("File_Triage") / "Executable"
        }     
        files_paths = scan_directory_for_files(selected_directory)
        stats = defaultdict(int)
        for file_path in files_paths:
            destination_folder = get_destination(file_path, extension_to_folder)
            safe_path = resolve_file_conflict(file_path, destination_folder)
            move_file(file_path, safe_path)
            stats[safe_path.parent.name] +=1
    display_summary(stats)
# --- Programme principal --- 

if __name__ == "__main__":
    main()