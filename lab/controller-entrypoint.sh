#!/bin/sh
set -eu

mkdir -p /root/.ssh

cp /run/ansible_lab /root/.ssh/ansible_lab
chmod 0600 /root/.ssh/ansible_lab

exec "$@"