

class Conf:
    """
    Class that collects all configurable parameters.
    """

    mngt_batch_size = 3
    mngt_outputdir = '/AB_20T_output/nanopore_output/BC_run_output/run_sup_1_dgx-4_gpu'
    mngt_inputdir = '/AB_20T_input/dataset/CliveOME_5mc_dataset_POD5'

    request_work_url =  "http://127.0.0.1:40765/assignwork"
    
    engine_external_script = "/u/dssc/tolloi/Cluster_Basecalling_Manager/BC_software/orfeo_executable/executable_dgx002/launch_supervisor.sh"
    engine_outputdir = '/AB_20T_output/nanopore_output/BC_run_output/run_sup_1_dgx-4_gpu'
    engine_inputdir = "/AB_20T_input/dataset/CliveOME_5mc_dataset_POD5"
    engine_polling_interval = 1
    engine_id = "dgx002_engine"
    engine_optimal_request_size = 111
    
    keep_alive_terminate_url = "http://127.0.0.1:40765/completed"
    keep_alive_url = "http://127.0.0.1:40765/keepalive"
