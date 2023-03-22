from django.test import TestCase
from django.contrib.auth.models import User
import os
from NetworkAlignment.AlignmentRunner import COMPUTATIONS_DIR

FILE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../"


class TestAlignmentRunner(TestCase):
    graph_1_filepath = ""
    graph_2_filepath = ""
    graph_1_name = ""
    graph_2_name = ""
    aligner = None

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="world", email="hello@world.com",
                                             first_name="hello",
                                             last_name="world")
        self.user.save()

    @classmethod
    def get_file_as_text(cls, file_path):
        return open(file_path).read()

    def set_computations_dir(self):
        self.aligner.operational_dir = COMPUTATIONS_DIR + "/test/" + str(self.aligner.task.operational_directory)
        self.aligner.result.operational_dir = self.aligner.operational_dir

    def test_aligner(self):
        if self.aligner is not None:
            # self.set_computations_dir()
            self.aligner.run_task()
            self.aligner.delete_operational_dir()
            print self.aligner.result
            self.assertTrue(self.aligner.result.error == "", "Error Occurred: " + str(self.aligner.result.error))
