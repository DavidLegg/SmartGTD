import json

def cfg(filename, *attrs):
    '''Retrieves the value in the given config file specified by the path of attribute names.'''
    if filename.split('.')[-1] != 'json':
        filename += '.json'
    filename = 'config/' + filename
    with open(filename) as f:
        obj = json.load(f)
        for a in attrs:
            obj = obj[a]
        return obj