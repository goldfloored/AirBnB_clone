#!/usr/bin/python3
"""
this module contains do_pack function which generates a .tgz archive from
the contents of web_static folder
"""

from datetime import datetime
from fabric.api import *


def do_pack():
    """
    compresses a folder to a .tgz archive
    """
    date_string = datetime.now().strftime('%Y%m%d%H%M%S')
    local('mkdir -p versions/')
    try:
        local("tar -cvzf versions/web_static_{}.tgz web_static".format(
                    date_string))
        return "versions/web_static_{}.tgz".format(date_string)
    except Exception:
        return None
