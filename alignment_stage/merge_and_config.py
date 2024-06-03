import os 
import re
import json 
import shutil

def merge_files(input_dir, output_file):
    file_pattern = ".fastq" 
    with open(output_file, 'w') as outfile: 
        for file_name in sorted(os.listdir(input_dir)):
            if file_pattern in file_name:
                with open(os.path.join(input_dir, file_name), 'r') as infile:
                    outfile.write(infile.read())

def merge_fastq(job_config_path):
    '''
    This function, will read the job_config and locate the pass
    dir inside the basecalling output dir. Then it will perform 
    a merge of the fastq files and collocate the final one inside
    the Batch dir
    '''
    with open(job_config_path, 'r') as file:
        config = json.load(file)
    pass_dir = os.path.join(config['Basecalling']['output_dir'], "pass")
    fail_dir = os.path.join(config['Basecalling']['output_dir'], "fail")

    run_number = re.search(r'\d+', config["General"]["run_name"]).group()
    pass_merged_file = os.path.join(config['Basecalling']['output_dir'], "pass_batch_" + run_number + "_total.fastq")
    fail_merged_file = os.path.join(config['Basecalling']['output_dir'], "fail_batch_" + run_number + "_total.fastq")

    merge_files(pass_dir, pass_merged_file)
    merge_files(fail_dir, fail_merged_file)

def create_align_output_dirs(job_config):
    '''
    This function will create in the output dir of the align
    job the BATCH dir with correct name where all the results of the alignment will be stored
    '''

def create_configurations_file(job_config_path) :
    '''
    This function needs to modify the template_config.json for the alignment in order
    to launch the alignment from the batch dir merged_fastq_pass to a
    selected output directory
    '''
    with open(job_config_path, 'r') as file:
        config = json.load(file)

    config_dir = config["Alignment"]["path_to_tmp_config"]
    run_number = re.search(r'\d+', config["General"]["run_name"]).group()
    tmp_config_name = f'align_config_{str(run_number)}.json'

    #Create a copy of the template for the alignment in the correct dir
    path_to_template_config = config["Alignment"]["template_config"]
    path_for_tmp_config = os.path.join(config_dir, tmp_config_name)

    shutil.copy(path_to_template_config, path_for_tmp_config)

    
    
    



