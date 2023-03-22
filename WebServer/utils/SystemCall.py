__author__ = 'varun'

from subprocess import Popen, PIPE
import logging

LOGGER = logging.getLogger(__name__)


class SystemCallException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class SystemCallResult:
    return_code = -1
    stderr = ""
    stdout = ""

    def __str__(self):
        return "Return Code: " + str(self.return_code) + \
               '\nSTDErr:' + str(self.stderr) + \
               "\nSTDOut:" + str(self.stdout)

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()


class SystemCall:
    def __init__(self, command, working_dir=None):
        if isinstance(command, basestring):
            self.args = command.split(" ")
        else:
            self.args = command
        self.result = SystemCallResult()
        self.working_dir = working_dir

    def run(self):
        if self.working_dir:
            p = Popen(self.args, stdin=PIPE, stdout=PIPE, stderr=PIPE,
                      cwd=self.working_dir)
        else:
            p = Popen(self.args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        self.result.stdout, self.result.stderr = p.communicate("")
        self.result.return_code = p.returncode
        return self.result


def make_system_call(command, working_dir=None):
    LOGGER.info("Making sys call: " + str(command))
    if "&&" in command:
        raise SystemCallException("You should not be making chained calls using this method")
    system_call = SystemCall(command, working_dir=working_dir)
    system_call.run()
    return system_call.result
