from pathlib import Path
from datetime import datetime
from datetime import date
from PIL import Image
import stat, os

def format_date(date: datetime) -> str:
    return date.strftime("%Y_%m_%d")
""" 
def format_date(date):

    Convert a date (EXIF string or datetime or timestamp) to "YYYY_MM_DD" format.

    Args:
        date (str | datetime | float | int): EXIF string, datetime object, or Unix timestamp.

    Returns:
        str: Formatted date as "YYYY_MM_DD".

    
    if isinstance(date, str):
        date_obj = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
    elif isinstance(date, (float, int)):
        date_obj = datetime.fromtimestamp(date)
    elif isinstance(date, datetime):
        date_obj = date
    else:
        raise TypeError(f"Unsupported date type: {type(date)}")
    
    return date_obj.strftime("%Y_%m_%d")
"""

def get_date_taken(path):
    """
    Retrieve the date the photo was taken from EXIF metadata if available,
    otherwise fallback to the file creation time.

    Args:
        path (Path): Path to the image file.

    Returns:
        str: Formatted date "YYYY_MM_DD".
    """
    try:
        exif = Image.open(path).getexif()
        if 306 in exif:
            date_taken = exif[306]
            return datetime.strptime(date_taken, "%Y:%m:%d %H:%M:%S")
        else:
            date_taken = os.path.getctime(path)
        return datetime.fromtimestamp(date_taken)
    
    except Exception as e:
        print(f"An error has occured with {path}: {e}")
        return None