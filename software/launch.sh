#!/bin/bash

cd $(dirname $0)
git fetch origin
git checkout origin/master
python3 pager.py

