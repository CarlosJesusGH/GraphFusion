__author__ = 'varun'

from .AlignmentResultsDataStructure import AlignmentResult
import logging

LOGGER = logging.getLogger(__name__)


class AlignmentResultNotFoundForTaskException(Exception):
    pass


def __get_alignment_in_list(alignment):
    result = []
    for pair in alignment.split("\n"):
        if pair:
            nodes = pair.split(" ")
            result.append((nodes[0], nodes[1]))
    return result

