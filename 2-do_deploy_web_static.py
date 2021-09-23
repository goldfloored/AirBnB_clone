#!/usr/bin/python3
"""
this module contains do_deploy function which distributes an archive
to my web servers
"""

import os
import re
from fabric.api import *
env.hosts = ['35.227.63.107', '35.243.218.35']


def do_deploy(archive_path):
    """deploys the archive to my web servers"""
    if os.path.exists(archive_path) is False:
        return False
    ar_path_split = re.split('[\. | _ | /]', archive_path)
    time_str = ar_path_split[-2]

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/web_static_{}/".format(
                    time_str))
        run("tar -xzf /tmp/web_static_{}.tgz -C \
                /data/web_static/releases/web_static_{}/\
                ".format(time_str, time_str))
        run("rm /tmp/web_static_{}.tgz".format(time_str))
        run("mv /data/web_static/releases/web_static_{}/web_static/* \
                /data/web_static/releases/web_static_{}/\
                ".format(time_str, time_str))
        run("rm -rf /data/web_static/releases/web_static_{}/web_static\
                ".format(time_str))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/web_static_{}/ \
                /data/web_static/current".format(time_str))
        return True
    except Exception:
        return False
