#!/bin/bash
set -e
apt-get update
apt-get install -y slapd ldap-utils
systemctl enable slapd
systemctl start slapd