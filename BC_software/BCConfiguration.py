

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
    engine_polling_interval = 1
    engine_id = ''
    engine_optimal_request_size = 100
    
    keep_alive_terminate_url = "http://127.0.0.1:40765/completed"
    keep_alive_url = "http://127.0.0.1:40765/keepalive"


