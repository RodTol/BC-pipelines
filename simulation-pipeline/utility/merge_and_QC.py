import os

def merge_files(input_dir, output_file):
    file_pattern = "*.fastq"
    with open(output_file, 'w') as outfile:
        for file_name in sorted(os.listdir(input_dir)):
            with open(os.path.join(input_dir, file_name), 'r') as infile:
                outfile.write(infile.read())