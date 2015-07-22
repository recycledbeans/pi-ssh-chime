#!/bin/sh

BASEDIR=$(dirname $0)

cd BASEDIR
sudo python ssh.py &
cd /
