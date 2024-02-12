import sys
import time
import requests
import os
import subprocess
import threading
from BCManagement import bc_status
from BCConfiguration import Conf

class BCKeepAlive(threading.Thread):
    """
    Class that encapsulates a thread where the BCEngine constantly informs the BCController on the state
    of the ongoing processing.

    It implements a resiliance protocol, thereby signalling to initiate a SHUTDOWN should the communication
    with the BC Controller encounter any problem: a crash, a network interruption, a malfunctioning. Likewise
    the BC Controller is aware of this protocol, so it knows we'll shutdown as soon as possible and eventually
    be restarted with a cleared internal state.

    In general, the Single Writer principle is followed: volatile variables are used where there is by design
    a single Thread expected to write/change a variable, while any number of threads can read that variable. In
    Python this is not needed, but it's important to spell it out in order to clarify the design and intended
    way of usage (indeed there is no 'volatile' in python).

    Essentially, the main thread where basecalling is happening, should get an instance and start the keepalive;
    then it should periodically check whether there are problems with the bc controller and so terminate; or upon
    completion of processing, it should communicate back the result and terminate the keepalive thread.

    Convenience methods have been provided, so they can be invoked on a BCKeepAlive instance; however it is
    possible also to check/interact directly with the internal 'volatile' variables: provided the resiliance
    protocol logic is implemented i.e. decide when to shutdown.
    """

    @classmethod
    def started_instance(cls, answer, starting_state):
        """
        Class method that returns an instance of BCKeepAlive and also starts the internal keep alive thread.

        :param answer: dictionary with the JSON of the BCBatch reply
        :param starting_state: string representing the starting state od the processing
        :return: BCKeepAlive with a thread running the keep-alive with the BC Controller
        """
        report_back_interval = answer['report_back_interval']
        job_id = answer['jobid']
        keep_alive_thread = BCKeepAlive(report_back_interval, job_id, starting_state)
        keep_alive_thread.start()
        return keep_alive_thread

    def __init__(self, report_back_interval, job_id, starting_state):
        """
        Constructor that requires the interval in seconds between successive keep-alive messages, the job_id for
        which we are sending the keep_alive, the processing starting_state

        :param report_back_interval: int representing seconds between successive keep-alive messages
        :param job_id: string representing the batch being processed
        :param starting_state string representing the current starting processing state
        """

        #Qua forse devo invocare il costruttore coi parametri giusti
        super().__init__()
        self.report_back_interval = report_back_interval
        self.job_id = job_id
        self.starting_state = starting_state
        self.final_state = ''  # volatile variable to indicate to this Thread, what is the final state reached by the processing main thread: once it's set, it implies immediate communication back to server  and shutdown.
        
        # Qua devo mettere il creatore con il json per le cose giuste ??

        #----------
        self.keep_alive_url = Conf.keep_alive_url # "http://127.0.0.1:5000/keepalive"
        self.keep_alive_terminate_url = Conf.keep_alive_terminate_url # "http://127.0.0.1:5000/completed"
        
        self.BCCONTROLLER_PB = False  # volatile variable to indicate to the main thread it should stop and shutdown: the bccontroller seems to have crashed!

    def run(self):
        """
        Method that starts a loop periodically calling back the BCController to inform it of the ongoing processing.

        Once the final state is reached, regardless of success or failure, the BCController is informed, the keep-alive
        is stopped, and the loop exits; thereby ending the thread!
        :return:
        """

        try:
            interval = int(self.report_back_interval / 2)  # report back already after half the allowed time!
            while self.final_state == '':
                # send a keep-alive!
                payload = {'job_id': self.job_id, 'job_state': self.starting_state}
                response = requests.get(self.keep_alive_url, params=payload)
                response.raise_for_status()  # SO ALSO HTTP ERRORS ARE RAISED AS EXCEPTIONS!
                #if response.json()["late"]:
                #    raise Exception("Basecalling Controller replied the keepalive is late, so workload will be reassigned.")
                time.sleep(interval)
            # exiting while: it means a final state has been reached and the BCController must be informed
            payload = {'job_id': self.job_id, 'job_state': self.final_state}
            response = requests.get(self.keep_alive_terminate_url, params=payload)
            response.raise_for_status()
        except Exception as e:
            """
            EXCEPTION DURING KEEPALIVE! THIS MEANS THE SERVER IS DOWN / UNREACHABLE / PROBLEMATIC!
            As per protocol, we'll interrupt ongoing work and initiate a shutdown of this BCEngine.
            """
            print("EXCEPTION DURING KEEPALIVE! PROTOCOL INITIATION OF BCENGINE SHUTDOWN! " + str(e))
            self.BCCONTROLLER_PB = True

    def shutdown_if_broken_keepalive(self):
        """
        Method that checks for a spotted problematic BC Controller: it crashed, the network is down,
        an exception on the server is returned back.

        It will initiate a client shutdown as per protocol, should the BCController be problematic.

        This is meant to be invoked from the main thread where the processing is taking place.
        :return:
        """
        if self.BCCONTROLLER_PB:
            print("BC CONTROLLER PROBLEM! ABORTING PROCESSING AND SHUTTING DOWN!")
            sys.exit(1)

    def terminate_keepalive(self, final_state):
        """
        Private method that tells the keep_alive_thread that processing is complete, so
        the BC Controller should be informed

        This method blocks until that thread ends.

        This is meant to be invoked from the main thread where the processing is taking place.

        :param final_state string representing the final state that was reached by the processing
        :return:
        """
        self.final_state = final_state
        self.join()




class BCEngine:
    """
    Class that represents a Basecalling Engine sitting in a physical node where GPUs are available.

    It will periodically connect back to BCController to request work for processing. It will then
    invoke a local guppy system such as supervisor-guppy, to carry out the work.
    """

    def __init__(self, json_file_path, node_index):
        # READ ALL THE FOLLOWING PARAMS FROM A CONFIG FILE
        print("*************BCP READ FROM JSON*************")
        conf = Conf.from_json(json_file_path, node_index)
        # ideal number of fast5 files to process per request
        self.optimal_request_size = conf.engine_optimal_request_size #2
        # unique ID of engine
        self.engine_id = conf.engine_id #"TEST-ENGINE"
        # minimum time in minutes between successive requests
        self.polling_interval = conf.engine_polling_interval # 1
        # ROOT of the inputdir where fast5 files are stored
        self.INPUTDIR = conf.engine_inputdir #"/home/ezio/PycharmProjects/ONPBasecaller/bcworkloaddir/inputdir"
        self.OUTPUTDIR = conf.engine_outputdir #"/home/ezio/PycharmProjects/ONPBasecaller/bcworkloaddir/outputdir"
        # local script to execute for BC processing
        self.bc_script = conf.engine_external_script #'/home/ezio/PycharmProjects/ONPBasecaller/bcworkloaddir/script.sh'
        self.bc_model = conf.engine_model
        # internal state of processing
        self.PROCESSING_STATE = 'STOPPED'
        # API URL
        self.api_url = conf.request_work_url #"http://127.0.0.1:5000/assignwork"
        # shutdown
        self.shutdown = False
        # work until none is left
        self.work_until_none_left = False

    def begin_working(self):
        """
        Method that kicks-off continuous periodic polling for new batches of fast5 files to process.

        Polling will occur every polling_interval minutes.

        However, after a batch has been processed, if the processing time took longer than the polling
        interval, then only 30 secs will be waited for before a new request is made. This is to allow
        for sustained processing throughput, while at the same time not heavily loading the server with
        useless requests when there is nothing to process.

        The loop can be cleanly interrupted by setting shutdown internal variable to True: upon completion
        of the running batch, it will stop.

        In case of any problem while communicating with the BC Controller, the loop will be interrupted
        and the client will shutdown, as per protocol.

        :return:
        """

        self.PROCESSING_STATE = bc_status.STARTED
        while not self.shutdown:
            # request a batch
            answer = self._request_a_batch(self.api_url, self.engine_id, self.optimal_request_size)
            # if there is something to process, then go on.
            batchsize = answer['batch_size']
            start_time = time.time()
            if (batchsize > 0):
                self.PROCESSING_STATE = bc_status.PROCESSING
                # get a keep_alive manager with a running keep-alive thread
                keep_alive_manager = BCKeepAlive.started_instance(answer, self.PROCESSING_STATE)
                # Prepare inputdir and outputdir for processing
                input_dir = os.path.join(self.INPUTDIR, answer['job_input_dir'])
                output_dir = os.path.join(self.OUTPUTDIR, answer['job_output_dir'])
                # Check how the BCController is doing
                keep_alive_manager.shutdown_if_broken_keepalive()
                # -------------------------------------------------------------
                # invoke the external script passing the input dir as parameter
                # it will block until complete
                self._basecalling_work(input_dir, output_dir, self.bc_model)
                # -------------------------------------------------------------
                # Check how the BCController is doing
                keep_alive_manager.shutdown_if_broken_keepalive()
                # Tell keepalive thread to send the result and terminate: will block until thread ends.
                keep_alive_manager.terminate_keepalive(self.PROCESSING_STATE)
                # Check how the BCController is doing
                keep_alive_manager.shutdown_if_broken_keepalive()
                # Go back to START state
                self.PROCESSING_STATE = bc_status.STARTED
            else:
                # returned batchsize is 0
                if self.work_until_none_left:
                    self.shutdown = True
            # sleep some time before requesting more batches
            end_time = time.time()
            if not self.shutdown: #basecalling work may have failed unexpectedly and signaled to shutdown! There is no point in sleeping!
                self._sleep_before_next_batch(start_time, end_time)
        # exiting while loop: log it somehow
        self.PROCESSING_STATE = bc_status.STOPPED # 'STOPPED'
        print("STOPPING BATCH REQUEST LOOP: ENGINE " + str(self.engine_id) + " WILL NO LONGER ASK FOR NEW BATCHES OF WORK.")

    def _request_a_batch(self, api_url, engine_id, optimal_request_size):
        """
        Private method to request a batch for processing to the BC Controller

        As per protocol, in case of any error with the BC Controller, this client will shutdown.

        :return: dictionary with the response from the BC Controller, i.e. JSON of BCBatch
        """

        try:
            # send a request for a batch to process
            payload = {'engineid': engine_id, 'batchsize': optimal_request_size}
            response = requests.get(api_url, params=payload)
            response.raise_for_status()
            # response is expected to be the JSON dump of BCBatch:
            #  {'report_back_interval' : int, 'jobid' : string, 'job_input_dir' : string, 'bc_engine_id' : string, 'batch_size' : int, 'batch' : [] }
            return response.json()
        except Exception as e:
            # BCController SERVER PROBLEMS!
            print("BC CONTROLLER PROBLEM! AS PER PROTOCOL, ABORTING PROCESSING AND SHUTTING DOWN! " + str(e))
            sys.exit(1)

    def _basecalling_work(self, input_dir, output_dir, model):
        """
        Private method that handles the actual Basecall processing. This implementation will invoke an
        external script that interacts with guppy_server.

        It will update the internal variable self.PROCESSING_STATE according to the output of the external
        script.

        However, should an exception be raised for any reason, self.PROCESSING_STATE will become FAIL but also
        self.shutdown will be set to True. In this way the engine will cleanly shutdown so the exception cause
        can be investigated.

        :param input_dir:
        :param output_dir:
        :return:
        """
        try:
            completed_process = subprocess.run([self.bc_script, input_dir, output_dir, model])
            return_code = completed_process.returncode
            if return_code == 0:
                self.PROCESSING_STATE = bc_status.DONE #'DONE'
            else:
                self.PROCESSING_STATE = bc_status.FAILED #'FAILED'
            # LOG SOMEHOW THE RESULT
            print("Processing result: " + str(return_code) + " PROCESSING_STATE is: "+self.PROCESSING_STATE)
        except Exception as e:
            # Something went wrong! Signal the failure to the BC Controller, and shutdown the engine!
            self.PROCESSING_STATE = bc_status.FAILED #'FAILED'
            self.shutdown = True
            # LOG the issue
            print("UNEXPECTED PROCESSING FAILURE! SHUTTING DOWN ENGINE! "+str(e))

    def _sleep_before_next_batch(self, start_time, end_time):
        """
        Private method that sleeps for some time before requesting a new batch to process.

        If the processing time was longer than the polling interval, then sleep just for
        30 secs. It's likely there are lot's more files to process.

        Otherwise, wait for the polling_interval. It's likely there wasn't anything to do.

        :param start_time: int representing the starting time
        :param end_time: int representing the ending time
        :return:
        """
        work_time = int(end_time - start_time)
        if work_time > self.polling_interval * 60:
            time.sleep(30)  # THERE WAS A LOT OF WORK TO DO, BUT DO SLEEP ANYWAY 30 sec BEFORE THE NEXT INVOCATION!
        else:
            # THERE WASN'T MUCH WORK TO DO, SO WAIT THE CONFIGURED AMOUNT OF MINUTES BEFORE REQUESTING WORK AGAIN!
            time.sleep(self.polling_interval * 60)


if __name__ == '__main__':
    json_file_path = sys.argv[1]
    node_index = int(sys.argv[2])
    eng = BCEngine(json_file_path, node_index)
    eng.work_until_none_left = True
   # eng.optimal_request_size = 15
    eng.begin_working()
