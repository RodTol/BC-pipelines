import os
import sys
import json

def process_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        # Your logic to process the JSON data
        return data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error!")
        print("Usage: python script.py <json_file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    config = process_json(json_file)

    run_name = config['General']['run_name']
    input_dir = config['Basecalling']['input_dir']
    output_dir = config['Basecalling']['output_dir']
    date = config["General"]["date"]

    print(f"Value of INPUT_DIR: {input_dir}")
    print(f"Value of OUTPUT_DIR: {output_dir}")
    print(f"date for config.json: {date}")