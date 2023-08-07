import yaml
import json
import numpy as np

def load_sg(filename, nt):
    '''
    '''
    sg = np.fromfile(filename, dtype=np.float32).reshape(-1, nt)

    return sg


def save_sg(filename, sg):
    '''
    '''
    # save as float32
    sg.astype(np.float32).tofile(filename)


def save_json(filename, data):
    ''' Save JSON file
    '''

    with open(filename, 'w') as f:
        json.dump(data, f)

def load_json(filename):
    ''' Load JSON file
    '''

    with open(filename, 'r') as f:
        data = json.load(f)

    return data


def load_yaml(filename):
    ''' Load YAML file

    Parameters
    ----------
        filename : str
            file name
    '''
    with open(filename) as f:
        config = yaml.safe_load(f)

    return config


def save_yaml(filename, config):
    ''' Save YAML file

    Parameters
    ----------
        filename : str
            file name
        config : dict
            configuration dictionary
    '''
    with open(filename, 'w') as f:
        yaml.dump(config, f, sort_keys=False)
