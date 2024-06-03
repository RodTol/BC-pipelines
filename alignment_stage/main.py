import sys
from merge_and_config import *

if __name__ == "__main__":

    config_file_path = sys.argv[1]
    merge_fastq(config_file_path)
    create_configurations_file(config_file_path)