#!/usr/bin/python3
"""
Write a Fabric script that generates a .tgz archive from the contents
"""
from fabric.api import run, put, local, env
from datetime import datetime
import os.path

env.hosts = ['54.167.111.147', '34.138.251.101']


def do_pack():
    """ pack files into .tgz archive """
    # tar -czvf file.tar.gz directory
    time = datetime.utcnow().strftime('%Y%m%d%H%M%S')

    path = "versions/web_static_{}.tgz".format(time)
    cmd = "tar -cvzf {} web_static".format(path)
    local("mkdir -p  versions")
    local(cmd)
    if os.path.exists(path):
        return (path)
    else:
        None


def do_deploy(archive_path):
    """
    - Upload the archive to the /tmp/ directory of the web server
    - Uncompress the archive to the folder /data/web_static/releases/<archive
    filename without extension> on the web server
    - Delete the archive from the web server
    - Delete the symbolic link /data/web_static/current from the web server
    - Create a new the symbolic link /data/web_static/current on the web
    server, linked to the new version of your code
    (/data/web_static/releases/<archive filename without extension>)
    """
    if not (os.path.exists(archive_path)):
            return False
    archive_name = archive_path.split('/')[1]
    archive_name_without_ext = archive_path.split('/')[1].split('.')[0]
    release_path = '/data/web_static/releases/' + archive_name_without_ext
    upload_path = '/tmp/' + archive_name
    put(archive_path, upload_path)
    run('mkdir -p ' + release_path)
    run('tar -xzf ' + upload_path + ' -C ' + release_path)
    run('rm ' + upload_path)
    run('mv ' + release_path + '/web_static/* ' + release_path + '/')
    run('rm -rf ' + release_path + '/web_static')
    run('rm -rf /data/web_static/current')
    run('ln -s ' + release_path + ' /data/web_static/current')
    return True
