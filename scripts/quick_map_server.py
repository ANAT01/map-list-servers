#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import json
import ConfigParser
import subprocess
import re
import random


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
parser.add_argument('-d', dest='datapath',
                    default='../datasource/',
                    help='set datasource path')
parser.add_argument('-i', dest='imgpath',
                    default='../icons/',
                    help='set iconsource path')
parser.add_argument('-b', dest='buildpath',
                    default='../build/',
                    help='set buildpath path')
args = parser.parse_args()


def findicon(find_name):
    for exist_icon in os.listdir(args.imgpath):
        if exist_icon[:exist_icon.rfind('.')] == find_name:
            return exist_icon
    if find_name.rfind("_") > 0:
        return findicon(find_name[:find_name.rfind("_")])
    else:
        return "default.svg"


def checkdir(directorypath):
    if not os.path.exists(directorypath):
        try:
            os.makedirs(directorypath)
            return True
        except:
            return False

buildpath = {
    "sourcepath": args.buildpath + "data_sources/",
    "grouppath": args.buildpath + "groups/",
}


def dict2string(dictionary, separator):
    tmplist = []
    for tmpkey in dictionary.keys():
        tmplist.append(tmpkey + '=' + dictionary[tmpkey])
    return str(separator).join(tmplist)


# Create new path
for var, path in buildpath.iteritems():
    checkdir(path)

for filename in os.listdir(args.datapath):
    if filename[filename.rfind('.'):] == '.json':
        metadata = ConfigParser.RawConfigParser()
        groupini = ConfigParser.RawConfigParser()

        with open(args.datapath + filename) as data_file:
            data = json.load(data_file)

        newsourcepath = buildpath['sourcepath'] + filename[:filename.rfind('.')]

        metadata_general_id = filename[:filename.rfind('.')]
        if filename.find("_") > 0:
            group = filename[:filename.find("_")]
        else:
            group = filename[:filename.find(".")]
        metadata_ui_group = group
        metadata_ui_alias = data['label']
        existsicon = findicon(filename[:filename.rfind('.')])
        metadata_ui_icon = existsicon[:existsicon.rfind('.')] + ".png"

        # Create [tms] section of metadata.ini
        if 'tms' in data:
            metadata_general_type = 'tms'
            metadata.add_section('tms')
            replacelist = []
            for var in re.findall('\[(\w+)\]', data['tms']['url']):
                if var == 'mirrors' and var in data['tms']:
                    replacelist.append(('[' + var + ']', random.choice(data['tms'][var])))
                if var == 'version' and var in data['tms']:
                    replacelist.append(('[' + var + ']', data['tms'][var][-1]))

            for search, replace in replacelist:
                data['tms']['url'] = data['tms']['url'].replace(search, replace)

            metadata.set('tms', 'url', 'http://' + data['tms']['url'])
            if 'crs' in data['tms']:
                metadata.set('tms', 'crs', data['tms']['crs'])
            if 'proj' in data['tms']:
                metadata.set('tms', 'proj', data['tms']['proj'])

        # Create [tms] section of metadata.ini
        if 'wms' in data:
            metadata_general_type = 'wms'
            metadata.add_section('wms')
            metadata.set('wms', 'url', 'http://' + data['wms']['url'])
            metadata.set('wms', 'params', dict2string(data['wms']['params'], '&'))
            metadata.set('wms', 'layers', ','.join(str(v) for v in data['wms']['layers']))

        # Create [general] section of metadata.ini
        metadata.add_section('general')
        metadata.set('general', 'id', metadata_general_id)
        metadata.set('general', 'type', metadata_general_type.upper())
        metadata.set('general', 'is_contrib', 'False')

        # Create [ui] section of metadata.ini
        metadata.add_section('ui')
        metadata.set('ui', 'group', metadata_ui_group)
        metadata.set('ui', 'alias', metadata_ui_alias)
        metadata.set('ui', 'icon', metadata_ui_icon)

        # Check newsourcepath exists
        checkdir(newsourcepath)

        # convert and copy icon
        subprocess.Popen(
            "convert -background none " + args.imgpath + existsicon + " -resize '24x24' " +
            newsourcepath + '/' + existsicon[:existsicon.rfind('.')] + '.png',
            shell=True
        ).wait()

        # Write metadata to file
        with open(newsourcepath + '/metadata.ini', 'wb') as configfile:
            try:
                metadata.write(configfile)
                print bcolors.OKGREEN + "[OK] Source created: " + bcolors.NC + metadata_general_id
            except:
                print bcolors.FAIL + "[ERROR] " + bcolors.NC + "SOMETHING ERROR"

                # ------------------
        # GROUP CREATING
        if filename.find("_") > 0:
            group = filename[:filename.find("_")]
        else:
            group = filename[:filename.find(".")]
        newgrouppath = buildpath["grouppath"] + group
        if not os.path.exists(newgrouppath):
            checkdir(newgrouppath)

            # Create [general] section for group directory
            groupini.add_section('general')
            groupini.set('general', 'id', group)

            # Create [ui] section for group directory
            groupini.add_section('ui')
            groupini.set('ui', 'alias', group)
            groupini.set('ui', 'icon', group + '.png')

            subprocess.Popen(
                "convert -background none " + args.imgpath + findicon(filename[:filename.find('_')]) +
                " -resize '24x24' " + newgrouppath + '/' + group + '.png',
                shell=True
            ).wait()

            # Write groupini to file
            with open(newgrouppath + '/' + group + '.ini', 'wb') as configfile:
                try:
                    groupini.write(configfile)
                    print bcolors.OKGREEN + "[OK] Group created: " + bcolors.NC + group
                except:
                    print bcolors.FAIL + "[ERROR] " + bcolors.NC + "SOMETHING ERROR"
