__author__ = 'varun'

import json
import unicodedata


def parse_json_form_data(form_string):
    data = json.loads(unicodedata.normalize('NFKD', form_string).encode('ascii', 'ignore'))
    response = {}
    for pair in data:
        response[pair["name"]] = pair["value"]
    return response