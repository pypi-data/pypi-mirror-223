#!/usr/bin/env python3

import os
import argparse


def clean_project(path):

    # check the existence of the path and files to make sure clean the right path
    if not os.path.exists(path):
        raise FileNotFoundError(f'Path {path} not found!')

    for folder in ['fig', 'par', 'dat', 'mod', 'fwi']:
        if not os.path.exists(f'{path}/{folder}'):
            print('It seems that the path is not a project path!')
            print('Or the project files have been cleaned!')
            return

    print(f'Clean files in {os.path.abspath(path)} ...')
    os.system(f'rm -rf {path}/fig')
    os.system(f'rm -rf {path}/par')
    # os.system(f'rm -rf {path}/dat/obs')
    # os.system(f'rm -rf {path}/dat/syn')
    # os.system(f'rm -rf {path}/dat/fwi')
    os.system(f'rm -rf {path}/dat')
    os.system(f'rm -rf {path}/mod')
    os.system(f'rm -rf {path}/fwi')
    os.system(f'rm -rf {path}/*.log')
    print('Clean done!')


if __name__ == '__main__':
    ''' Clean the project files

    Usage:
        python clean.py path
    '''

    parser = argparse.ArgumentParser(description='Clean the project files')
    parser.add_argument('path', type=str, default='.', help='Project path to clean')

    args = parser.parse_args()

    # clean the project files
    clean_project(args.path)
