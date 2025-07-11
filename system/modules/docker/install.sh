#!/bin/bash
set -e
apt-get update
apt-get install -y docker.io docker-compose
systemctl enable docker
systemctl start docker