import sys
import shutil
from pathlib import Path
from collections import defaultdict

import utils.file_ops as file_ops
import utils.categorization as cat
import utils.date_utils as date_utils
import utils.logging_utils as log
import utils.ui_utils as ui

# --- Config console for UTF-8 support (Windows) ---
sys.stdout.reconfigure(encoding='utf-8')


# --- Main function --- 
# Main function: ask user for a directory, scan files, move them to categorized folders,
# and log all actions in a daily log file.

def main():
    ui.welcoming_message()
    min_photos_per_day = ui.asking_number_photo()
    selected_directory = ui.ask_user_for_directory()
    if selected_directory is None:
        print("None: Program will stop now.")
        return

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

    stats = defaultdict(int)
    log_folder = Path.home() / "File_Triage" / "Logs"
    file_ops.create_directory_if_missing(log_folder)
    log_file = log.ensure_daily_log_file(log_folder)
    files_paths = file_ops.scan_directory_for_files(selected_directory)
    if not files_paths:
        print("No files to back up in this folder")
    else:
        file_ops.creating_back_up(files_paths, selected_directory)

    # Load rules from JSON
    rules_path = Path(cat.__file__).parent / "rules.json"
    rules = cat.get_rules(rules_path)

    category_to_folder = {
        "payslip" : Path("File_Triage") / "Documents" / "Travail" / "Fiche de paie",
        "resume" : Path("File_Triage") / "Documents" / "Travail" / "CV & Lettre de motivation",
        "identity" : Path("File_Triage") / "Documents" / "Identité & permis"
        
    }

    # Files
    for file_path in files_paths:

         #Detect category
        category = cat.get_category(file_path.name, rules)
            
        # Priority: category-based destination
        date_for_folder = cat.extract_year_from_filename(file_path.name)

        if category and category in category_to_folder:
            if category == "payslip":
                if date_for_folder:
                    destination_folder = Path.home() / category_to_folder[category] / date_for_folder
                else:
                    destination_folder = Path.home() / category_to_folder[category] / "Unknown"
            else:
                destination_folder = Path.home() / category_to_folder[category]
        else:
            #extension-based.
            destination_folder = cat.get_destination(file_path, extension_to_folder)
        
        safe_path = file_ops.resolve_file_conflict(file_path, destination_folder)
        try:
            file_ops.move_file(file_path, safe_path)
            log.log_event(log_file,
                            f"The file {file_path} has been successfully moved toward : {safe_path}",type="MOVE")
            
            if category and category in category_to_folder:
                stats_key = category_to_folder[category].name
                stats[stats_key] +=1
            else:
                stats_key = destination_folder.name
            stats[stats_key.name] += 1

        except Exception as e:
                log.log_event(log_file,
                            f"The file {file_path} has not been moved. Error:{e}",type="ERROR")
    # Organizing pictures by day
    cat.organize_images_by_day(selected_directory, min_photos_per_day, log_file, stats)


    ui.display_summary(stats)
3
# --- Programme --- 

if __name__ == "__main__":
    main()