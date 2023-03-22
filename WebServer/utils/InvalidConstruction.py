__author__ = 'varun'


class InvalidConstructionError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)