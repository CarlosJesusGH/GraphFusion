__author__ = 'carlos garcia-hernandez'  # using as reference: WebServer/CanonicalCorrelationAnalysis/CanonicalAnalysis.py

from TaskFactory.TaskFactorySingleton import Task
from .settings import *
from utils.SystemCall import make_system_call
from TaskFactory.models import Task as TaskModel
from datetime import datetime
from django.db import connection
from WebServer.settings import PYTHON_PATH
import traceback
import uuid
import os
import logging
import unicodedata
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from TaskFactory.ParallelComputationExecutor import Runnable
# from django.template import Context
# from django.template.loader import get_template


LOGGER = logging.getLogger(__name__)

class VisualizeSEException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class VisualizeSEAnalysis(Task):
    def __init__(self, net_names, directed, request_FILES, user, task_name):
        Task.__init__(self, name=task_name, task_id=-1)
        self.user = user
        self.net_names = net_names
        self.directed = directed
        self.request_FILES = request_FILES
        self.task = TaskModel()
        temp = self.__get_fresh_dir()
        self.operational_dir = COMPUTATIONS_DIR + "/" + temp + "/"
        self.graph_path = self.operational_dir
        self.__initialise_operational_directory()
        self.__save_task_began(user=user, task_name=task_name, directory=temp)
        self.task_id = self.task.taskId

    def __save_task_began(self, user, task_name, directory):
        LOGGER.info("Starting task for " + str(self.task_id))
        self.task.task_type = VISUALIZESE_TASK
        self.task.taskName = task_name
        self.task.user = user
        self.task.operational_directory = directory
        self.task.save()

    def __save_task_finished(self):
        LOGGER.info("Task Finished, id:" + str(self.task_id) + " ,op_dir:" + str(self.operational_dir))
        connection.close()
        self.task.finished_at = datetime.now()
        self.task.finished = True
        self.task.save()

    def __initialise_operational_directory(self):
        LOGGER.info("Initialising directory for task: " + self.operational_dir)
        make_system_call("mkdir " + self.operational_dir)
        make_system_call("mkdir " + self.graph_path)

    def __save_graphs(self):
        for network_name, network_data in self.net_names:
            edgelist_path = self.graph_path + network_name
            f = open(edgelist_path, "w")
            f.write(network_data)
            f.close()

    def __save_file_to_dir(self, directory, filename, filedata):
        print("save_file_to_dir for file:", filename)
        print("result_remove_file", make_system_call("rm -f " + directory + filename))
        blob = filedata
        fs = FileSystemStorage(directory) #defaults to   MEDIA_ROOT  
        filename_res = fs.save(filename, ContentFile(blob.read()))
        print("filename_res", filename_res)

    def __save_files(self):
        for request_file in REQUEST_FILES:
            self.__save_file_to_dir(self.operational_dir, request_file, self.request_FILES[request_file])


    def __run_task(self):
        # return make_system_call("ls " + self.operational_dir, working_dir=self.operational_dir)
        return make_system_call("bash " + BASH_SCRIPT_PATH + " " + self.net_names[0][0] + " " + self.directed + " " + self.operational_dir, working_dir=self.operational_dir)
        # return make_system_call("bash " + PSB_MATCOMP_SCRIPT_PATH + " " + op_dir + " " + fact_name + " " + PSB_MATCOMP_OUT_FILES[0] + " " + PSB_MATCOMP_OUT_FILES[1] + " " + PSB_MATCOMP_ENTITYLIST_ROWS + " " + PSB_MATCOMP_ENTITYLIST_COLS, working_dir=op_dir)
    
    @classmethod
    def __get_fresh_dir(cls):
        temp = uuid.uuid4().hex
        while os.path.isdir(COMPUTATIONS_DIR + "/" + temp):
            temp = uuid.uuid4().hex
        return temp

    def run_task(self):
        try:
            self.__save_graphs()
            self.__save_files()
            result = self.__run_task()
            LOGGER.info(result)
            if len(result.stderr):
                print("len(result.stderr)", len(result.stderr))
                print("result.stderr", result.stderr)
                raise VisualizeSEException("Error occurred while computing task: \n\n" + result.stderr)
            self.__save_task_finished()
        except Exception as e:
            connection.close()
            LOGGER.error(e)
            LOGGER.error(traceback.format_exc())
            self.task.error_occurred = True
            self.task.error_text = e.message
            self.task.finished = True
            self.task.finished_at = datetime.now()
            self.task.save()
