import json
import os
from pprint import pprint

from coursescheduler import generate_schedule


def obj_to_json_file(object, output_name):
    if not (os.path.exists("./output_json_files")):
        os.mkdir("./output_json_files")
    json_filename = 'output_json_files/' + output_name + '.json'
    with open(json_filename, 'w') as outfile:
        json.dump(object, outfile, indent=6)


if __name__ == "__main__":
    result = generate_schedule(None, None, None, True)
    obj_to_json_file(result, "schedule_output")
    pprint(result)
