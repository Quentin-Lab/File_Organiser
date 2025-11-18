from pathlib import Path
from utils.date_utils import get_date_taken
from collections import defaultdict

IMAGE_EXTENSIONS = ["jpg", "jpeg", "png"]
MIN_PHOTO_PER_DAY = 5

# Determine the number of image in a file list regarding IMAGE_EXTENSIONS.
def count_image_in_list(files_list):
    """
    Determine the number of image in a file list regarding IMAGE_EXTENSIONS.
    Args: 
        files_list (Path): a list with path.
    Returns:
        The number of image in this list.
    """
    return sum(1 for f in files_list if f.suffix[1:].lower() in IMAGE_EXTENSIONS)

def count_image_in_directory(directory, target_date, mode="day"):
    """
    Count how many images match the target_date in the given directory.

    Args:
        directory (Path): Directory to inspect.
        target_date (datetime): Date of the photo (from get_date_taken).
        mode (str): "day" to count per day, "month" to count per month.

    Returns:
        int: Number of images matching the date according to mode.
    """
    if not directory.exists():
        return 0
    
    count = 0
    for file in directory.iterdir():
        if file.is_file() and file.suffix[1:].lower() in IMAGE_EXTENSIONS:
            file_date = get_date_taken(file)
            if file_date is None:
                continue
            if mode == "day" and file_date.date() == target_date.date():
                count += 1
            elif mode == "month" and file_date.year == target_date.year and file_date.month == target_date.month:
                count += 1
    return count

def group_image_by_day(directory):
    image_by_day = defaultdict(list)
    for f in directory.iterdir():
        if f.is_file() and f.suffix[1:].lower() in IMAGE_EXTENSIONS:
            date_taken = get_date_taken(f)
            if date_taken:
                image_by_day[date_taken.date()].append(f)
    return image_by_day


def get_destination(file_path, extension_to_folder):
    """
    Determine the destination folder for a non-image file based on its extension.

    Args:
        file_path (Path): The path to the file.
        extension_to_folder (dict): Mapping of file extensions (str) to folder paths (Path).

    Returns:
        Path: The full path to the destination folder for the file.
    """
    home_path = Path.home()
    file_extension = file_path.suffix[1:].lower()

    if file_extension in extension_to_folder:
        return home_path / extension_to_folder[file_extension]

    return home_path / "File_Triage" / "Autres"

def organize_images_by_day(selected_directory, min_photos_per_day, log_file, stats):
    from utils.categorization import group_image_by_day
    from utils.file_ops import resolve_file_conflict, move_file, create_directory_if_missing
    from utils.date_utils import get_date_taken
    from pathlib import Path
    import utils.logging_utils as log

    images_by_day = group_image_by_day(selected_directory)

    for day, files in images_by_day.items():
        date_taken = get_date_taken(files[0])
        base_folder = Path.home() / "File_Triage" / "Images"
        year_folder = base_folder / str(date_taken.year)
        month_folder = year_folder / date_taken.strftime("%B")

        # Décider si on crée le dossier du jour
        if len(files) >= min_photos_per_day:
            destination_folder = month_folder / f"{day.day:02d}"
        else:
            destination_folder = month_folder

        create_directory_if_missing(destination_folder)

        # Déplacer toutes les images du jour
        for file_path in files:
            safe_path = resolve_file_conflict(file_path, destination_folder)
            try:
                move_file(file_path, safe_path)
                log.log_event(log_file, f"The file {file_path} has been successfully moved toward : {safe_path}")
                stats[base_folder.name] += 1
            except Exception as e:
                log.log_event(log_file, f"The file {file_path} has not been moved. Error:{e}")