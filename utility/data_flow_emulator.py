import os
import sys
import shutil
import time
from tqdm import tqdm

def mimic_live_writing(src_dir, dest_dir, interval_seconds=30):
    files = os.listdir(src_dir)
    files_set = set(files)  # Set to keep track of copied files

    for file in tqdm(files_set):    
        src_file_path = os.path.join(src_dir, file)
        dest_file_path = os.path.join(dest_dir, file)
        print(f"Copying file: {file}", end=" ")
        shutil.copy(src_file_path, dest_file_path)
        print("Copy successful")
    
        time.sleep(interval_seconds)
    
    print("No new files to copy.")
    sys.exit()        

if __name__ == "__main__":
    src_dir = sys.argv[1]  # Source directory
    dest_dir = sys.argv[2]    # Destination directory

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    mimic_live_writing(src_dir, dest_dir)
