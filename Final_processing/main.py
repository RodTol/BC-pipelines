import sys
from parse_data import load_json
from parse_data import parse_BCP_logs
from parse_data import rework_csv

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Error!")
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)
    
    # Load the configuration from the specified JSON file
    json_file = sys.argv[1]
    config = load_json(json_file)


    csv_filename = parse_BCP_logs(config)
    rework_csv(csv_filename)