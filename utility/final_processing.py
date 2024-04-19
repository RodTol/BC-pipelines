import json

class Final_processing :
    
    def __init__(self, config_file_path) :
        with open(config_file_path, 'r') as file:
            template_config = json.load(file)
        self.total_output_dir = template_config['Basecalling']['output_dir']        
    