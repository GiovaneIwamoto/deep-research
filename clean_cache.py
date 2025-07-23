import os
import shutil

def remove_pycache(root_dir="."):
    """
    Recursively remove all __pycache__ directories starting from root_dir.
    """
    removed = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "__pycache__" in dirnames:
            pycache_path = os.path.join(dirpath, "__pycache__")
            shutil.rmtree(pycache_path)
            print(f"Removed: {pycache_path}")
            removed += 1
    if removed == 0:
        print("No __pycache__ directories found.")
    else:
        print(f"Total __pycache__ directories removed: {removed}")

if __name__ == "__main__":
    remove_pycache(".")