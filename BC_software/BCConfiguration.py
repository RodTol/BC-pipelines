import json

class Conf:
    """
    Class that collects all configurable parameters.
    """

    mngt_batch_size = 3
    mngt_outputdir = ''
    mngt_inputdir = ''

    request_work_url = 'http://127.0.0.1:40765/assignwork'
    
    engine_external_script = ''
    engine_outputdir = ''
    engine_inputdir = ''
    engine_polling_interval = 1 #indicates after how long it will try to do a polling. It's multiplied by 60
    engine_id = ''
    engine_optimal_request_size = 100
    engine_model = ''
    
    keep_alive_terminate_url = "http://127.0.0.1:40765/completed"
    keep_alive_url = "http://127.0.0.1:40765/keepalive"

    @classmethod
    def from_json(cls, file_path, node_index):
        """
        Initialize the Conf class from a JSON file.

        Args:
            file_path (str): Path to the JSON file.
            node_index (int): index for the node in the config.json list.

        Returns:
            Conf: An instance of Conf with settings loaded from the JSON file.
        """
        with open(file_path, 'r') as json_file:
            config = json.load(json_file)
        
        conf_instance = cls()
        
        conf_instance.mngt_outputdir = config["Basecalling"]["output_dir"]
        conf_instance.mngt_inputdir = config["Basecalling"]["input_dir"]

        conf_instance.request_work_url = 'http://127.0.0.1:40765/assignwork'
        
        conf_instance.engine_external_script = config["Resources"]["supervisor_script_path"]
        conf_instance.engine_outputdir = config["Basecalling"]["output_dir"]
        conf_instance.engine_inputdir = config["Basecalling"]["input_dir"]
        conf_instance.engine_polling_interval = 1
        conf_instance.engine_id = config["Resources"]["nodes_list"][node_index]
        conf_instance.engine_optimal_request_size = config["Resources"]["batch_size_list"][node_index]
        conf_instance.engine_model = config["Basecalling"]["model"]
        
        conf_instance.keep_alive_terminate_url = "http://127.0.0.1:40765/completed"
        conf_instance.keep_alive_url = "http://127.0.0.1:40765/keepalive"

        return conf_instance
