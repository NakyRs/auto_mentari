import json

def readFileJson(file):
        with open(file, 'r') as f:
            return json.loads(f.read())

    # return data

def writeFileJson(obj, file):
    jsonObj = json.dumps(obj, indent=4)

    with open(file, "w") as outfile:
        outfile.write(jsonObj)