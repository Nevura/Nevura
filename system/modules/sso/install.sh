#!/bin/bash
set -e
apt-get update
apt-get install -y keycloak
systemctl enable keycloak
systemctl start keycloak