import json
import shutil
import os 

class Final_processing :
    
    def __init__(self, config_file_path) :
        with open(config_file_path, 'r') as file:
            template_config = json.load(file)
        self.total_output_dir = template_config['Basecalling']['output_dir'] 
        self.total_pass_dir = os.path.join(self.total_output_dir, "pass") 
        self.total_fail_dir = os.path.join(self.total_output_dir, "fail")       
    
    def _find_batch_directories(self, output_dir):
        batch_directories = []
        for root, dirs, files in os.walk(output_dir):
            for dir_name in dirs:
                if dir_name.startswith("BATCH"):
                    batch_directories.append(os.path.join(root, dir_name))
        return batch_directories

    def _move_files_from_pass_directory(batch_dir, total_pass_dir):
        batch_pass_dir = os.path.join(batch_dir, 'pass')
        if not os.path.isdir(batch_pass_dir):
            print("Batch 'pass' directory not found.")
            return
        
        if not os.path.exists(total_pass_dir):
            print("Total 'pass' dir not found")
            return
    
        for root, dirs, files in os.walk(batch_pass_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                shutil.move(file_path, total_pass_dir)

    def _move_files_from_fail_directory(batch_dir, total_fail_dir):
        batch_fail_dir = os.path.join(batch_dir, 'fail')
        if not os.path.isdir(batch_fail_dir):
            print("Batch 'fail' directory not found.")
            return
        
        if not os.path.exists(total_fail_dir):
            print("Total 'fail' dir not found")
            return
    
        for root, dirs, files in os.walk(batch_fail_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                shutil.move(file_path, total_fail_dir)

    def put_togheter_outputs(self):
        batch_directories = self._find_batch_directories(self.total_output_dir)
        print("\033[31m" + "Batch directories" + "\033[0m")
        print(batch_directories)
        for dir in batch_directories:
            self._move_files_from_pass_directory(dir, self.total_pass_dir)
            print("\033[31m" + "Pass file moved" + "\033[0m")
            self._move_files_from_fail_directory(dir, self.total_fail_dir)
            print("\033[31m" + "Fail file moved" + "\033[0m")

        
