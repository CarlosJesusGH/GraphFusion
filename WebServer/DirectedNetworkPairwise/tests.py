from django.test import TestCase
from .DirectedNetworkPairwise import DirectedNetworkPairwise
import os
from django.contrib.auth.models import User

FILE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../NetworkAlignment/resources/test"


class SimpleTest(TestCase):
    def test_analysis(self):
        user = User.objects.create_user(username="test", password="world", email="hello@world.com",
                                        first_name="hello",
                                        last_name="world")
        user.save()

        a = ("KSHV", open(FILE_DIR + "/KSHV.txt").read())
        b = ("EBV", open(FILE_DIR + "/EBV.txt").read())
        c = ("mCMV", open(FILE_DIR + "/mCMV.txt").read())
        d = ("VZV", open(FILE_DIR + "/VZV.txt").read())
        e = ("HSV-1", open(FILE_DIR + "/HSV-1.txt").read())
        p = DirectedNetworkPairwise(graphs=[a, b, c, d, e], user=user, task_name="test")
        p.run_analysis()
