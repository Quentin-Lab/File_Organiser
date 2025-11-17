from pathlib import Path

def welcoming_message():
    """
    Displays a welcome message to the user.
    """
    print("Hello and thanks for using this script.\n")


def asking_number_photo():
    """
    Ask the user for the minimum number of pictures in a day to create a folder.
    
    Returns:
        int: Minimum number of pictures per day to create a folder.
    """
    while True:
        try:
            min_photos_per_day = int(
                input("From how many pictures in a day would you like to create a folder for this day? ")
            )
            if min_photos_per_day < 2:
                print("Please enter a number greater than 1.")
                continue
            return min_photos_per_day
        except ValueError:
            print("Please enter a valid integer.")
            
def ask_user_for_directory():
    """
    Prompt the user to enter a directory path to be cleaned.

    Checks:
            - Path exists.
            - Path is within the current user's home directory.
            - Path is a folder, not a file.
            - Avoids restricted folders like 'AppData'.

    Returns:
            Path: Absolute path to the directory selected by the user.
            None: If the user types 'leave' to exit.
    """
    allowed_base_path = Path.home()

    while True:
        target_directory = input("Please give me the path to the directory you want to clean e.g C:\\Users\\Home\\Downloads or type leave:")
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

# --- Display the stat ---
def display_summary(stats):
    """
    Display a summary of moved files per category.

    Args:
        stats (defaultdict): Dictionary with folder names as keys and moved file counts as values.
    """
    total_files = sum(stats.values())
    print(f"\n Total filed moved: {total_files}")
    for (key, value) in stats.items():
        print(f"{key} : {value} files moved")