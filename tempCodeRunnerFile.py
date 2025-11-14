import os, sys, shutil
from pathlib import Path

# --- Configuring the console output to support special characters (e.g. accents) ---
sys.stdout.reconfigure(encoding='utf-8')

# --- Reception function ---
def welcoming_message():
    """Displays a welcome message to the user."""
    print("Hello and thanks for using this script.")


# --- User directory selection function ---
def user_repertory():
    """
    Asks the user to provide the path to a directory to be cleaned.
    Checks that:
      - the path exists,
      - it belongs to the current user session,
      - it is not a file but a folder.
    Returns: Path(absolute path to the directory) or None if the user quits.
    """
    authorised_user_path = Path.home()

    while True:
        user_path = input("Please give me the path to the repertory you want to clean e.g C:\\Users\\Home\\Downloads :")
        if user_path == "leave":
            print("Leaving programm...")
            return None

        absolute_user_path = Path(user_path).resolve()

        if absolute_user_path.exists():
            try:
                absolute_user_path.relative_to(authorised_user_path)
                if absolute_user_path.is_file():
                    print("Please note that you have specified a file: please specify a path.")
                elif absolute_user_path.is_dir():
                    return(absolute_user_path)
            except ValueError:
                print("Select a directory that is present in your user session.")         
        else:
            print("Oops, the path you specified does not exist!")

# --- Listing the files present in a directory function ---
def file_listening(repertory):
    """
    returns a list of Path objects representing only the files
    (and not the subfolders) present in the given directory.
    """
    files_path_list = []
    for element in repertory.iterdir():
        if element.is_file():
            files_path_list.append(element)
    return(files_path_list)

# --- Programme principal --- 
welcoming_message()

# Selecting the user directory
user_path = user_repertory()

if user_path == None:
    print("None: Program will stop now.")
else:
    # Récupération de la liste des fichiers à traiter
    files_list = file_listening(user_path)
    print(files_list)
    for file_path in files_list:
        files_name = file_path.name
        extension = file_path.suffix[1:]
        home_path = Path.home()
        destination_path = home_path / "Documents"
        print(destination_path)