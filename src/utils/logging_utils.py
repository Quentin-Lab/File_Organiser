from pathlib import Path
from datetime import datetime
import utils.file_ops as file_ops
import os

INFO = "INFO"
ERROR = "ERROR"
MOVE = "MOVE"

def ensure_daily_log_file(log_folder_path: Path):
    """
    Ensure a daily log file exists in the given log folder. 
    If it does not exist, create it.

    Args:
        log_folder_path (Path): Path to the folder where logs are stored.

    Returns:
        Path: Path to the log file for today's date.
    """

    current_Time = datetime.now()
    current_date = f"{current_Time.year}_{current_Time.month}_{current_Time.day}"
    log_file_path = log_folder_path / f"{current_date}.log"
    if log_file_path.exists():
        return log_file_path
    else:
        with open(log_file_path, "w", encoding="utf-8") as fp:
            pass
        return log_file_path


def log_event(log_file_path, message, type=INFO):
    """
    Append a log message to the specified log file with timestamp and type.

    Args:
        log_file_path (Path): Path to the log file.
        message (str): Message to log.
        type (str): Type of the log message (INFO, ERROR, MOVE).
    """
    
    current_Time = datetime.now()
    time_stamp = current_Time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write (f"{time_stamp}:{type}\t{message}\n") 

