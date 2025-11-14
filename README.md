# File Organiser Script

A Python script to organize files in a user-specified directory into categorized folders based on file extensions. This project is designed to evolve into a more structured file management tool.

## Current Features (First Version)

- Supports common file types:
  - Documents (`.pdf`, `.doc`)
  - Images (`.jpeg`, `.jpg`, `.png`)
  - Videos (`.mp4`, `.mkv`)
  - Executables (`.exe`)
- Automatically creates destination folders if they don't exist.
- Moves all other file types into an "Others" folder.
- Simple command-line interface.
- Basic error handling for files that cannot be moved.
- Restricts access to sensitive system folders like `AppData`.

## Planned Features / Next Implementations

### Photo Sorting by Date
- Automatically create subfolders by **Year** and **Month** under `File_Triage/Images`.
- Photos without EXIF data will use file creation/modification dates.
- Default category: personal photos (`Perso`) unless keywords indicate otherwise.

### Logging
- All file movements will be logged with timestamp: `source → destination`.
- Errors (permissions, conflicts, missing folders) will also be logged.
- Log file location: `File_Triage/Logs/tri_photos.log`.

### Document Convention Handling
- For important documents (PDF, DOC, Excel), implement a naming convention:  
  `[Category]_[YYYY-MM-DD]_[Description].ext`.
- Categories may include Work, Insurance, Revenue, etc.
- Files not following the convention go to `Autres / Others` folder.

### Modular Code Structure
- Separate functions for scanning directories, resolving conflicts, moving files, logging, and date extraction.
- Easier to maintain and extend in future versions.

### Future Improvements
- Option for a “simulation mode” to preview movements before executing.
- Extendable for automatic categorization using keywords in file names.
- Potential GUI integration for selecting directories easily.

## Usage

1. Clone the repository:  
   ```bash
   git clone https://github.com/quentin-lab/File_Organiser.git

2. Run the script:
python file_organiser.py

3. Follow the prompts to select the directory you want to clean.

## Support / Tips

If you find this project useful and want to support its development, you can send a small tip via [PayPal](https://www.paypal.me/0Reap).