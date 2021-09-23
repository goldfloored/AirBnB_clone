#!/usr/bin/env bash
# set up web servers for deployment of web_static
# install nginx if not already installed
sudo apt-get -y update
sudo apt-get -y install nginx
# create folder /data/web_static/shared/ if it doesn't already exist
sudo mkdir -p /data/web_static/shared/
# create folder /data/web_static/releases/test/ if it doesn't already exist
sudo mkdir -p /data/web_static/releases/test/
# puts something into a fake HTML file /data/web_static/releases/test/index.html
echo -e "<html>\n\t<head>\n\t</head>\n\t<body>\n\t\tHolberton School\n\t</body>\n</html>" | sudo tee /data/web_static/releases/test/index.html
# creates symbolic link /data/web_static/current linked to
# /data/web_static/releases/test/ folder, if link already exists it is deleted
# and recreated each time the script is run
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
# give ownership of /data/ folder to ubuntu user and group,should be recursive
sudo chown -R ubuntu:ubuntu /data/
# update nginx configuration to serve content of /data/web_static/current/ to
# hbnb_static
content="\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n"
sudo sed -i "38i\ $content" /etc/nginx/sites-enabled/default
# restart nginx web server
sudo service nginx reload
sudo service nginx restart
