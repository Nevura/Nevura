#!/bin/bash
set -e
apt-get update
apt-get install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
systemctl enable libvirtd
systemctl start libvirtd