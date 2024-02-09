import json
import os
import shutil
import threading
import time
import uuid
from flask import Flask, request
from collections import namedtuple

BCStatus = namedtuple("BCStatus", ["ASSIGNED", "STARTED", "PROCESSING", "STOPPED", "DONE", "FAILED"])
bc_status = BCStatus("ASSIGNED", "STARTED", "PROCESSING", "STOPPED", "DONE", "FAILED")

class BCBatch:
    """
    Class that represents a batch of fast5 files that have been assigned for processing.

    It consists of:
    - jobid           int assigned to the job
    - job_input_dir   string with the name of the directory RELATIVE TO the guppy server's INPUTDIR that
                      contains symlinks to the fast5 files that need to be processed.
    - job_output_dir  string with the name of the directory RELATIVE TO the guppy server's OUTPUTDIR that
                      will contain the output FASTQ files.
    - guppyid         string identifying the guppy server that was assigned to the processing
    - batch_size      int actual size of the batch, which may differ from the requested size if there weren't
                      enough files to fill the request.
    - batch           list with the actual filenames
    """

    def __init__(self, report_back_period=300, jobid="-1", job_input_dir="", job_output_dir="", bc_engine_id="", batch_size=0, batch=None):
        if batch is None:
            batch = []

        self.report_back_period = report_back_period
        self.jobid = jobid
        self.job_input_dir = job_input_dir
        self.job_output_dir = job_output_dir
        self.bc_engine_id = bc_engine_id
        self.batch_size = batch_size
        self.batch = batch


class BCWorkloadState:
    """
    Class that represents the state of the basecalling processing, as well as
    providing methods for operating on it.

    Essentially all the raw output from the Oxford Nano Pore sequencing machine
    consists of .FAST5 files that the machine writes to a specific directory we'll
    refer to as INPUT_DIR.

    Each raw file, is the recording of the electrical signal corresponding to the
    particular DNA chunk that was sequenced. The chunks are known as frags, while the
    recordings are also called squibbles because of the shape of the resulting graph.
    Basically this raw data represents electrical current/potential over time.

    For each file, a corresponding .FASTQ file must be produced and stored in
    OUTPUT_DIR.

    This is the basecalled file: a very long string of 4 letters representing the
    biological bases, G A T C, that translates the raw electrical signals.

    The actual basecalling functionality is carried out by a different software/system,
    i.e. the GUPPY system. But there are also other systems such as BONITO that can be used.
    This software is needed because the algorithms involved in basecalling make use of
    neural networks in order to translate the electrical signals, and so are rather
    specialised for the task requiring also the availability of GPUs.

    Several instances of the GUPPY servers are expected to be available: at least one for each
    GPU in the infrastructure. Moreover, each GUPPY server is designed to work on multiple files
    which it expects to be present in a specified directory.

    The class allows raw files to be assigned to one of the GUPPY server for processing. This
    will be reflected in the filesystem by the presence of the following structure:

    INPUT_DIR
        |- JOB-ID1_GUPPY-SERVER-NAME_inputdir
            |- file1.fast5   (ATTENTION! IT WILL BE A SYMLINK!)
            |- file2.fast5   (ATTENTION! IT WILL BE A SYMLINK!)
            |- file3.fast5   (ATTENTION! IT WILL BE A SYMLINK!)
    """

    def __init__(self):
        conf_file_path = "BCConfiguration.json"
        with open(conf_file_path, 'r') as file:
            Conf = json.load(file)

        self.INPUTDIR = Conf["BCManagement"]["mngt_inputdir"]
        self.OUTPUTDIR = Conf["BCManagement"]["mngt_outputdir"]
        self.unassigned_bc = []
        self.default_batch_size = Conf["BCManagement"]["mngt_batch_size"]
        self.assigned_batches = {}

    def update(self):
        """
        Method used to tell this BCWorkloadStatus to read the filesystem and update itself
        accordingly.

        In case of any errors, false is returned and empty data structures are filled in.

        The intended use case is scanning for the presence of new fast5 files to process, as
        well as reconstruct the internal state in case of a crash, based on what it finds in
        the filesystem.

        :return: boolean with the result of the operation.
        """

        # find all processed files i.e. get  list of all .FASTQ files
        fastq_files = []
        passoutputdir = os.path.join(self.OUTPUTDIR, "pass")
        failoutputdir = os.path.join(self.OUTPUTDIR, "fail")
        for dir_entry in (passoutputdir, failoutputdir):
            for entry in os.scandir(dir_entry):
                if entry.is_file():
                    str_name = entry.name
                    if (len(str_name)>6) & (str_name[-6:].lower() == ".fastq"):
                        fastq_files.append(str_name[:-6])
        # find all raw files that do not have a FASTQ counterparty,
        # as well as all files that have been assigned for processing
        potential_files = [] # fast5 files for which there is no fastq counterparty
        assigned_files = [] # fast5 files assigned for basecalling
        for entry in os.scandir(self.INPUTDIR):
            if entry.is_dir():
                # It's a dir: it should contain symlinks to assigned files that are being worked on
                str_dirname = entry.name
                if (len(str_dirname)>8 & (str_dirname[:8]=="ASSIGNED")) | (len(str_dirname)>6 & (str_dirname[:6]=="FAILED")):
                    for assignment in os.scandir(entry):
                        # check assigned file is a symlink!
                        if assignment.is_symlink():
                            # check it ends with .fast5
                            str_assignment = assignment.name
                            if len(str_assignment)>5 & (str_assignment[-5:].lower() == ".pod5"):
                                # add it to the list
                                assigned_files.append(str_assignment[:-5])
            elif entry.is_file():
                # It's a file: it should be a fast5 file that potentially needs to be processed unless already assigned
                str_name = entry.name
                if len(str_name)>5 & (str_name[-5:].lower() == ".pod5"):
                    str_name = str_name[:-5]
                    if str_name not in fastq_files:
                        potential_files.append(str_name)
        # filter assigned_files from potential_files
        final_list = []
        for entry in potential_files:
            if entry not in assigned_files:
                final_list.append(entry+".pod5")
        # update this instance
        self.unassigned_bc = final_list
        #TO DO: reconstruct assigned_batches after crash?

    def assign_work_to(self, bc_engine_id="default-engine", batch_size=0):
        """
        Method invoked to assign work to the supplied guppy_server. By default, the guppy_server's
        inbuilt desired batch size will be used; but optionally this can be overriden through the
        batch_size parameter.

        Note that if there aren't enough pending files to meet the required batch size, the request
        is still successful and the guppy_server will be assigned all available ones.

        Finally, a zero or negative value of batch_size will automatically imply the use of the
        guppy_server's inbuilt default batch size.

        :param guppy_server: a BCSvc
        :param batch_size: optional int for the desired batch size
        :return: BCBatch with the details of the assigned work
        """

        # if there is nothing left to process, return an EMPTY BCBatch
        if len(self.unassigned_bc) == 0:
            return BCBatch()
        # use default batch_size if no batch_size is specified
        if batch_size <= 0:
            batch_size = self.default_batch_size
        # set batch_size to the min between the desired batch size and available files
        batch_size = min(batch_size, len(self.unassigned_bc))
        # get the files
        batch = [self.unassigned_bc.pop(0) for x in range(batch_size)]
        # choose a new jobid
        jobid = str(uuid.uuid4().int)
        # prepare the input dir name for the job
        job_input_dir = "_".join(["ASSIGNED", str(jobid), bc_engine_id])
        # transactionally create in one go the dir and symlinks
        # TO DO! TRANSACTION !!!
        dirfullpath = os.path.join(self.INPUTDIR, job_input_dir)
        os.mkdir(dirfullpath)
        for fl in batch:
            os.symlink(os.path.join(self.INPUTDIR, fl), os.path.join(dirfullpath, fl))
        # prepare temporary output dir
        job_output_dir = "_".join(["TMPOUTPUT", str(jobid), bc_engine_id])
        outputdirfullpath = os.path.join(self.OUTPUTDIR, job_output_dir)
        os.mkdir(outputdirfullpath)
        # return the BCBatch
        bc_work = BCBatch(jobid=jobid, job_input_dir=job_input_dir, job_output_dir=job_output_dir, bc_engine_id=bc_engine_id, batch_size=batch_size, batch=batch)
        self.assigned_batches[jobid] = bc_work
        return bc_work

    def completed_work(self, jobid="", jobstate=""):
        # MAKE IT A TRANSACTION IN CASE OF CRASH
        bc_work = self.assigned_batches.pop(jobid)
        full_job_input_dir = os.path.join(self.INPUTDIR, bc_work.job_input_dir)
        full_job_output_dir = os.path.join(self.OUTPUTDIR, bc_work.job_output_dir)
        if jobstate == bc_status.FAILED:
            # rename inputdir to FAILED so it can be excluded from reassignment until manual intervention
            failed_full_job_input_dir = os.path.join(self.INPUTDIR, bc_work.job_input_dir.replace("ASSIGNED","FAILED"))
            failed_full_job_output_dir = os.path.join(self.OUTPUTDIR, bc_work.job_output_dir.replace("TMPOUTPUT","FAILEDOUTPUT"))
            os.rename(full_job_input_dir, failed_full_job_input_dir)
            os.rename(full_job_output_dir, failed_full_job_output_dir)
        elif jobstate == bc_status.DONE:
            passdir = os.path.join(full_job_output_dir,'pass')
            destpassdir = os.path.join(self.OUTPUTDIR, 'pass')
            if os.path.exists(passdir) & os.path.exists(destpassdir):
                for entry in os.scandir(passdir):
                    str_name = entry.name
                    dst = os.path.join(destpassdir, str_name)
                    os.rename(entry.path, dst)  # it will move the fastq file to the final destination
            faildir = os.path.join(full_job_output_dir,'fail')
            destfaildir = os.path.join(self.OUTPUTDIR, 'fail')
            if os.path.exists(faildir) & os.path.exists(destfaildir):
                for entry in os.scandir(faildir):
                    str_name = entry.name
                    dst = os.path.join(destfaildir, str_name)
                    os.rename(entry.path, dst)  # it will move the fastq file to the final destination
            shutil.rmtree(full_job_input_dir)
            log_full_job_output_dir = os.path.join(self.OUTPUTDIR, bc_work.job_output_dir.replace("TMPOUTPUT", "LOGOUTPUT"))
            os.rename(full_job_output_dir, log_full_job_output_dir)
        else:
            print("ATTENTION! UNKNOWN STATE FROM CLIENT! " + jobstate)
            unknown_full_job_input_dir = os.path.join(self.INPUTDIR, bc_work.job_input_dir.replace("ASSIGNED","UNKNOWN"))
            unknown_full_job_output_dir = os.path.join(self.OUTPUTDIR, bc_work.job_output_dir.replace("TMPOUTPUT","UNKNOWNOUTPUT"))
            os.rename(full_job_input_dir, unknown_full_job_input_dir)
            os.rename(full_job_output_dir, unknown_full_job_output_dir)




class BCController:
    """
    Class that represents a RESTful Service listening for Basecalling work requests from Basecalling Engines.
    """

    def __init__(self):
        self.lock = threading.Lock()
        self.tracker = {} # dict of job_id -> [last_ack_time, state, report_back_period]
        self.bc_state = BCWorkloadState()
        self.bc_state.update()
        self.app = Flask(__name__)
        a = self.app

        # /assignwork
        @a.route("/assignwork", methods=["GET"])
        def get_assignwork():
            req_batchsize = int(request.args['batchsize'])
            req_engineid = request.args['engineid']
            with self.lock:
                assignment_reply = self.bc_state.assign_work_to(req_engineid, req_batchsize)
                assignment_reply.report_back_interval = 90 # maximum seconds that will be waited for keep alive from client
                self.tracker[assignment_reply.jobid] = [time.time(), bc_status.ASSIGNED, 90]
            return json.dumps(assignment_reply.__dict__)

        # /keepalive
        @a.route("/keepalive", methods=["GET"])
        def get_keepalive():
            req_job_id = request.args['job_id']
            req_job_state = request.args['job_state']
            with self.lock:
                entry = self.tracker[req_job_id].copy()
                right_now = time.time()
                entry[0] = right_now
                entry[1] = req_job_state
                # entry[2] stays the same
                self.tracker[req_job_id] = entry
            return json.dumps({"late": False})

        # /completed
        @a.route("/completed", methods=["GET"])
        def get_completed():
            req_job_id = request.args['job_id']
            req_job_state = request.args['job_state']
            with self.lock:
                #
                # THIS SHOULD BE A TRANSACTION
                # if the req_job_id does not exist it is an unexpected error: inform client? how to handle it?
                del self.tracker[req_job_id]
                self.bc_state.completed_work(req_job_id, req_job_state)
            # NOTHING TO RETURN
            return json.dumps({"ok": True})
            
#Launching the flask server
#app.run decide on which host (0.0.0.0 means all) and port to listen
if __name__ == '__main__':
    RESTFulAPI = BCController()
    RESTFulAPI.app.run(host='0.0.0.0', port=40765)


### NOTES:
# what if the keepalive arrived late?
# missing entry?
# active deleting thread?
# multiple requests for same jobid?
# try:
# MAKE A DEFENSIVE COPY OF THE WHOLE ENTRY: we have a deleting thread in the background that operates on it!
#
# AS PER BEST PRACTICE, EACH THREAD NEVER WORKS DIRECTLY IN THE ENTRY, BUT MAKES FIRST A DEFENSIVE COPY AND
# THEN MODIFIES IT, BEFORE ASSIGNING IT BACK TO THE DICTIONARY. SO THE COPY IS SAFE AS NO DATA CHANGES.
#
# THIS ONLY GUARANTEES THE LOGICAL CONSISTENCY OF ANY DECISION/OPERATION MADE ON THE RETRIEVED DATA, WHICH IS
# GUARANTEED FREE OF INTERLEAVING OF "PARTIAL CHUNKS" AS THE OTHER THREAD OPERATES ON THE DATA.
#
# IT DOES _NOT_ GUARANTEE ABSENCE OF RACE CONDITION / STALE READS! FOR THAT YOU STILL NEED SYNCHRONIZATION OF
# SOME SORT.
#
# INDEED, THE RELEVANT SCENARIO IS WHEN WE GET A REFERENCE TO THE ENTRY, WHICH GETS REPLACED IMMEDIATELY AFTER
# WE OBTAIN IT. WE'LL THEN GO ON TO MAKE A LOGICALLY CONSISTENT DECISION BASED ON THE DATA IN THE ENTRY, WHICH
# IS NOW CLEARLY STALE/OLD. IN GENERAL WHETHER WE CAN TOLERATE OPERATION ON STALE DATA, OR WHETHER WE REALLY NEED
# TO FORCE THE OTHER THREAD TO WAIT FOR US TO COMPLETE, WILL DEPEND ON THE ACTUAL PROBLEM DOMAIN. :-)
#    entry = self.tracker[req_job_id].copy()
#
#    last_time = entry[0]
#    report_back_period = entry[2]
#    right_now = time.time()
#    if right_now <= last_time + report_back_period:
# OK: keep alive arrived before expiry
#        entry[0] = right_now
#        entry[1] = req_job_state
# entry[2] stays the same
#        self.tracker[req_job_id] = entry
#        return json.dumps({"late": False})
#    else:
# BAD: keepalive arrived late
#        print("WARNING! NOT IMPLEMENTED YET! keepalive arrived too late: client should shutdown, and work be re-assigned!")
# remove from tracking ?
# clear state so old work can be reassigned?
# tell client it was late?
# interaction with deleting thread and other threads?
#        return json.dumps({"late": True})
# except KeyError:
# ENTRY DOES NOT EXIST! EITHER IT WAS DELETED BY THE DELETING THREAD BECAUSE IT WAS EXPIRED, OR IT NEVER EXISTED.
# INFORM CLIENT! AS PER PROTOCOL, IT SHOULD STOP PROCESSING AND INITIATE A SHUTDOWN.
#    print("WARNING! NOT IMPLEMENTED YET! keepalive arrived for non-existant jobid!")
# tell client?
#    return json.dumps({"late": True})
