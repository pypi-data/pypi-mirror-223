import json
import os
from typing import List


def read_json_file(file):
    f = open(file)
    data = json.load(f)
    f.close()
    return data


def get_all_files(directory, source) -> List[str]:
    file_list = []
    for root, directories, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.basename(file_path)
            if file_name == f"{source}.json":
                file_list.append(file_path)
    return file_list
