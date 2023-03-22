__author__ = 'varun'

import threading

from utils.SystemCall import make_system_call
from .AlignmentRunner import AlignmentRunnerException


class ParallelRunner(threading.Thread):  # this is used to run 2 ncounts in parallel
    def __init__(self, command):
        threading.Thread.__init__(self)
        self.command = command

    def run(self):
        result = make_system_call(self.command)
        if result.return_code != 0:
            raise AlignmentRunnerException("Error while running parallel runner: " + str(result.stderr))