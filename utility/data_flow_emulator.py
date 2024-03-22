import os
import sys
import shutil
import time
import random

def mimic_live_writing(src_dir, dest_dir, interval_seconds=30):
    copied_files = set()  # Set to keep track of copied files

    while True:
        files = os.listdir(src_dir)
        available_files = [file for file in files if file not in copied_files]

        if available_files:
            file_to_copy = random.choice(available_files)  # Choose a random file from the available files
            src_file_path = os.path.join(src_dir, file_to_copy)
            dest_file_path = os.path.join(dest_dir, file_to_copy)
            print(f"Copying file: {file_to_copy}", end=" ")
            shutil.copy(src_file_path, dest_file_path)
            print("Copy successful")
            copied_files.add(file_to_copy)  # Add the copied file to the set
        else:
            print("No new files to copy.")

        time.sleep(interval_seconds)
        sys.exit()

if __name__ == "__main__":
    src_dir = sys.argv[1]  # Source directory
    dest_dir = sys.argv[2]    # Destination directory

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    mimic_live_writing(src_dir, dest_dir)
