__author__ = 'carlos garcia-hernandez'

from .settings import *
from fnmatch import fnmatch

def get_all_downloadable_results(task):
    results = []
    op_dir = COMPUTATIONS_DIR + "/" + task.operational_directory
    for r_file in RESULT_FILES:
        if r_file.endswith("*"):
            pattern = r_file
            for path, _, files in os.walk(op_dir):
                for name in files:
                    if fnmatch(name, pattern):
                        results.append((name, open(os.path.join(path, name)).read()))
        else:
            file_path = COMPUTATIONS_DIR + "/" + task.operational_directory + "/" + r_file
            if os.path.isfile(file_path):
                results.append([r_file, open(file_path).read()])
    return results