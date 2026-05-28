import os
import sys
import subprocess

def open_in_default_editor(file_path: str) -> None:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found.")
    
    if sys.platform.startswith("win"):
        # Windows: uses the associated editor for the file type
        os.startfile(file_path)
    elif sys.platform == "darwin":
        # macOS: opens with default application for the file extension
        subprocess.Popen(["open", file_path])
    else:
        # Linux/Unix: check EDITOR env var or use xdg-open
        editor = os.environ.get("EDITOR") or os.environ.get("VISUAL")
        if editor:
            subprocess.Popen([editor, file_path])
        else:
            subprocess.Popen(["xdg-open", file_path])