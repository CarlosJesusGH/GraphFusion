__author__ = 'carlos garcia-hernandez'  # using as reference: WebServer/CanonicalCorrelationAnalysis/CanonicalAnalysis.py

from TaskFactory.TaskFactorySingleton import Task
from .settings import COMPUTATIONS_DIR, DATA_FUSION_TASK, NAMES_MAPPING_FILE, \
    NAMES_OF_NETWORKS_LIST_FILES, DATA_FUSION_SCRIPT_PATH, PYNMF_SCRIPT_PATH, TEST_SCRIPT_PATH
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
import pickle


LOGGER = logging.getLogger(__name__)


class DataFusionException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class DataFusionAnalysis(Task):
    def __init__(self, facts, net_names, request_FILES, user, task_name, setup, max_iter, delta_min):
        Task.__init__(self, name=task_name, task_id=-1)
        self.user = user
        self.facts = facts
        self.net_names = net_names
        self.setup = setup
        self.request_FILES = request_FILES
        self.task = TaskModel()
        temp = self.__get_fresh_dir()
        self.operational_dir = COMPUTATIONS_DIR + "/" + temp
        self.graph_path = self.operational_dir + "/graphs"
        self.__initialise_operational_directory()
        self.__save_task_began(user=user, task_name=task_name, directory=temp)
        self.task_id = self.task.taskId
        self.nmfif_params = {"setup":setup,}
        self.max_iter = max_iter
        self.delta_min = delta_min

    def __save_task_began(self, user, task_name, directory):
        LOGGER.info("Starting task for DataFusion Analysis " + str(self.task_id))
        self.task.task_type = DATA_FUSION_TASK
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

    def __save_graph(self):
        for net_name in self.net_names:
            blob = self.request_FILES[net_name]
            # print("blob", blob)
            # open("test_fname.txt", 'wb').write(ContentFile(b'new content'))
            # path = default_storage.save("test_fname.txt", ContentFile(blob.read()))
            fs = FileSystemStorage(self.graph_path) #defaults to   MEDIA_ROOT  
            filename = fs.save(net_name, ContentFile(blob.read()))
            if ".csv" not in net_name:
                filepath = self.graph_path + "/" + net_name
                if ".hdf5" in net_name:
                    with h5py.File(filepath, "r") as f:
                        X = np.array(f.get('dataset'))
                    np.savetxt(filepath + ".csv", X, delimiter="\t")
                if ".edgelist" in net_name:
                    X = nx.read_edgelist(filepath)
                    np.savetxt(filepath + ".csv", nx.to_numpy_array(X), delimiter="\t")
        print("self.facts", self.facts)
        pickle.dump(self.facts, open(self.operational_dir + "/facts.pkl", "wb"))
        pickle.dump(self.nmfif_params, open(self.operational_dir + "/nmfif_params.pkl", "wb"))

    def __save_graph_old(self):
        LOGGER.info("Saving graphs for {task_id: " + str(self.task_id) + ", task_name: " + str(self.name) + "}")
        # print("self.facts", self.facts)
        for fact in self.facts:
            print("fact.keys()", fact.keys())
            M_ids = ["M0", "M1", "M1C", "M2", "M3", "M3C"]
            for Mn in M_ids:
                if Mn in fact.keys() and fact[Mn]:
                    print("Mn", Mn)
                    # print("fact[Mn]", fact[Mn])

                    # graph_name = unicodedata.normalize('NFKD', fact[Mn][0]).encode('ascii', 'ignore')
                    graph_name = fact[Mn][0]
                    # graph = unicodedata.normalize('NFKD', fact[Mn][1]).encode('ascii', 'ignore')
                    graph = fact[Mn][1]
                    # graph = fact[Mn][1] unichr(105).encode('utf-8')
                    # graph = unicodedata.normalize('NFKD', fact[Mn][1]).encode('utf-8')
                    print("type(graph)", type(graph))
                    # print("fact[Mn]", fact[Mn])
                    print("graph_name", graph_name)

                    # with open(self.graph_path, "w") as f:
                        # if self.graph.startswith("LEDA.GRAPH"):
                        #     f.write(self.graph)
                        # else:
                        #     f.write(ListToLeda(graph_list=self.graph).convert_to_leda())
                        # f.write(graph)
                    
                    graph_path = self.graph_path + "/" + graph_name
                    # with open(graph_path, "wb") as f:
                        # f.write(graph)
                        # f.write(graph.encode('utf-8').strip())
                        # f.write(u' '.join(graph).encode('utf-8').strip())
                        # f.write(unicodedata.normalize('NFKD', fact[Mn][1]))
                        # f.write(unicodedata.normalize('NFKD', fact[Mn][1]).encode('utf-8', 'ignore'))
                        # f.write(graph.encode("utf=8"))

                    f = open(graph_path, 'w+b')
                    # byte_arr = [120, 3, 255, 0, 100]
                    binary_format = bytearray(graph, 'utf8')
                    f.write(binary_format)
                    f.close()

                    fact[Mn][0] = graph_name
                    fact[Mn][1] = graph_path

                    # f = open(self.operational_dir + "/" + NAMES_MAPPING_FILE, "w")
                    # f.write(str([graph_name]))
                    # f.close()
            print("fact", fact)
        print("self.facts", self.facts)
        pickle.dump(self.facts, open(self.operational_dir + "/facts.pkl", "wb"))
                
    """
    # def __retrieve_annotations(self):
    #     LOGGER.info("Retrieving Annotations for task_id:" + str(self.task_id) + " ,op_dir:" + self.operational_dir)
    #     if self.annotations:
    #         with open(self.operational_dir + "/" + ANNOTATIONS_FILENAME, "w") as f:
    #             f.write(self.annotations)
    #     else:
    #         if self.annotation_type in zip(*ANNOTATIONS_TYPE)[0]:
    #             result = make_system_call(
    #                 PYTHON_PATH + " " +
    #                 ANNOTATIONS_RETRIEVER_SCRIPT_PATH + " " +
    #                 self.graph_path + " " +
    #                 GENE_TO_GO_FILE + " " +
    #                 OBO_FILE + " " +
    #                 self.annotation_type + " " +
    #                 self.operational_dir + "/" + ANNOTATIONS_FILENAME
    #                 , working_dir=self.operational_dir)
    #             LOGGER.info(result.stdout)
    #         else:
    #             raise DataFusionException(
    #                 "Invalid annotation type given: " + self.annotation_type +
    #                 ". Please reload your page and re-submit your analysis.")

    # def __run_orca_for_network(self):
    #     ORCAExecutable(file_path=self.graph_path).run()

    # def __generate_go_matrix(self):
    #     return make_system_call(
    #         PYTHON_PATH + " " +
    #         MAKE_GO_MATRIX_SCRIPT_PATH + " " +
    #         self.graph_path + " " +
    #         self.graph_path + ".res.ndump2 " +
    #         ANNOTATIONS_FILENAME + " " +
    #         GO_MATRIX_FILE_NAME + " "
    #         , working_dir=self.operational_dir)
    """

    def __run_df(self):
        return make_system_call("bash " + PYNMF_SCRIPT_PATH + " " + self.operational_dir + " " + self.max_iter + " " + self.delta_min, working_dir=self.operational_dir)


    """ def __generate_result_figures(self):
        return make_system_call(
            PYTHON_PATH + " " +
            GENERATE_PLOT_SCRIPT_PATH + " " +
            GO_MATRIX_FILE_NAME + "_GO " +
            GO_MATRIX_FILE_NAME + "_GDV " +
            self.operational_dir + " " +
            CCA_RESULT_FILENAME + " " +
            PLOT_FILE_KEEP_VARIABLE
            , working_dir=self.operational_dir) """
    

    @classmethod
    def __get_fresh_dir(cls):
        temp = uuid.uuid4().hex
        while os.path.isdir(COMPUTATIONS_DIR + "/" + temp):
            temp = uuid.uuid4().hex
        return temp

    # def __check_annotations_file(self):
    #     if not os.path.isfile(self.operational_dir + "/" + ANNOTATIONS_FILENAME):
    #         raise DataFusionException(
    #             "Annotations could not be created. " +
    #             "Please make sure that the input network contains Entrez Ids for node labelling.")
    #     elif len(open(self.operational_dir + "/" + ANNOTATIONS_FILENAME, "r").readlines()) == 0:
    #         raise DataFusionException(
    #             "Annotations could not be created. " +
    #             "Please make sure that the input network contains Entrez Ids for node labelling.")

    def run_task(self):
        try:
            self.__save_graph()
            # self.__run_orca_for_network()
            # self.__retrieve_annotations()
            # self.__check_annotations_file()
            # result = self.__generate_go_matrix()
            # if len(result.stderr):
            #     raise DataFusionException(
            #         "Error occurred while computing Gene Ontology Matrix: \n" + result.stderr)
            # LOGGER.info(result)

            result = self.__run_df()
            LOGGER.info(result)
            if len(result.stderr):
                print("len(result.stderr)", len(result.stderr))
                print("result.stderr", result.stderr)
                raise DataFusionException("Error occurred while computing DF: \n\n" + result.stderr)

            # result = self.__generate_result_figures()
            # LOGGER.info(result)
            # if len(result.stderr) and "RuntimeWarning" not in result.stderr:
            #     raise DataFusionException(
            #         "Error occurred while generating result figures: \n\n" + result.stderr)
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