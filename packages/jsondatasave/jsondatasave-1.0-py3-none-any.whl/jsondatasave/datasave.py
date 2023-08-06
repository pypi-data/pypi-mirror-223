import json
import hashlib


def load(FileName):
    with open(FileName, 'r') as file:
        Save_Data = json.load(file)
    return Save_Data


def save(Data, Filename):
    with open(Filename, "w") as dump:
        json.dump(Data, dump)
    return Data
