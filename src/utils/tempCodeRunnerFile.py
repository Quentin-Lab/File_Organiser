from pathlib import Path
from datetime import datetime
from PIL import Image
import stat, os

path = "C:\\Users\\quent\\Downloads\\IMG_5034.jpg"
status = os.path.getctime(path)
print(status)