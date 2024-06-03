import sys
from merge_and_config import merge_fastq

if __name__ == "__main__":

    config_file_path = sys.argv[1]
    merge_fastq(config_file_path)