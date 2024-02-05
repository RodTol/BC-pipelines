import os
import json

#Load in config the json file
with open('config.json', 'r') as json_file:
    config = json.load(json_file)

run_name = config['General']['run_name']
input_dir = config['Basecalling']['input_dir']
output_dir = config['Basecalling']['output_dir']
date = config["General"]["date"]

print(f"Value of INPUT_DIR: {input_dir}")
print(f"Value of OUTPUT_DIR: {output_dir}")
print(f"date for config.json: {date}")