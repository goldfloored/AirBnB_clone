#!/usr/bin/python3
"""
this module contains do_clean function which deletes out-of-date archives
"""

import os
from fabric.api import *
env.hosts = ['35.227.63.107', '35.243.218.35']


def do_clean(number=0):
    """deletes out of date archives, number is number of archives to keep"""
    # going to put list of archive names here
    filenames = []
    local("ls -1 versions | sort -r > versionfiles")
    with open('versionfiles') as f:
        fileslines = f.read()
    for fileline in fileslines:
        if len(fileline) == 29 and fileline[:11] == "web_static_" and \
                          fileline[-4:] == ".tgz":
            filenames.append(fileline)

    if number < 2:
        if len(filenames) <= 1:
            return
        del_after_index = 1
    else:
        if number <= len(filenames):
            return
        del_after_index = number
    for i in range(del_after_index, len(filenames)):
        local("rm versions/{}".format(filenames[i]))
        run("rm -rf /data/web_static/releases/{}".format(filenames[i][:-4]))
