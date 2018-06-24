import json, os

def load_json_into_dict(filepath):
    with open(filepath) as json_data:
        return json.load(json_data)

def write_to_file(filepath, data):
    # clear and write to file
    with open(filepath, 'w+') as outfile:
        outfile.truncate()
        json.dump(data, outfile)

def load_or_create_file(filepath, initial_structure):
    # create if it doesn't exist
    if not os.path.isfile(filepath):
        _load_initial_json(filepath, initial_structure)
    # definitely exists now. Open and return it
    with open(filepath,'r+') as f:
        return json.load(f)

def _load_initial_json(filepath, initial_structure):
    json_structure = json.dumps(initial_structure)
    with open(filepath, 'w+') as outfile:
        json.dump(initial_structure, outfile)
