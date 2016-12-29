#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import json
from jsonschema import validate, ValidationError


class bcolors:
    # Colorize console output
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    NC = '\033[0m'

parser = argparse.ArgumentParser()
parser.add_argument('-s', dest='schemapath',
                    required=True,
                    help='set schema file')
parser.add_argument('-d', dest='datapath',
                    required=True,
                    help='set datasource path')
args = parser.parse_args()

# Read schemafile
with open(args.schemapath, 'r') as schemafile:
    schema = json.load(schemafile)

# Read and check file recursive
for filename in os.listdir(args.datapath):
    if filename[filename.rfind('.'):] == '.json':
        with open(args.datapath + filename, 'r') as datafile:
            data = json.load(datafile)
        try:
            validate(data, schema)
            print bcolors.OKGREEN + "[OK] " + bcolors.NC + filename
        except ValidationError as e:
            print bcolors.FAIL + "[ERROR] " + bcolors.NC + filename
            sys.exit(bcolors.FAIL + '--- Check failed! ---' + bcolors.NC)
    else:
        print bcolors.WARNING + "[WARNING] " + bcolors.NC + "Wrong extension in " + filename
