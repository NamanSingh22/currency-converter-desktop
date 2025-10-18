import os
import sys

def resource_path(relative_path):
    try:
        # for pyinstaller; for packaging with the logo png
        
        base_path = sys._MEIPASS #type:ignore
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
