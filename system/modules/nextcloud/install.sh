#!/bin/bash
set -e
docker pull nextcloud
mkdir -p /opt/nextcloud
cd /opt/nextcloud
docker run -d --name nextcloud -p 8080:80 -v nextcloud:/var/www/html nextcloud