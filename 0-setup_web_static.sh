#!/usr/bin/env bash
#  Bash script that sets up your web servers for the deployment of web_static

# Install Nginx if it not already installed
sudo apt-get -y update
sudo apt-get -y install -y nginx

# Create the necessary directories
mkdir -p /data/web_static/shared
mkdir -p /data/web_static/releases/test/

# Create a fake HTML file
sudo echo "Hello Ven, Remember to be gentle with yourself❤️" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link
# The -sf option allows to force (overwrite) the creation of the symlink
sudo ln -nfs /data/web_static/releases/test /data/web_static/current

# change owner of the data folder
sudo chown -R ubuntu:ubuntu /data

# Update the Nginx config to serve the content of /data/web_static/current/ to hbnb_static
str="\\\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\tindex index.html 0-index.html 0-index.htm;\n\t}"
sudo sed -i "/^\tserver_name .*;/a ${str}" /etc/nginx/sites-enabled/default

# restart nginx
sudo service nginx restart
