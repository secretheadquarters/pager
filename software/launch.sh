#!/bin/bash

BRANCH=$(hostname)

cd $(dirname $0)
git fetch origin
git checkout origin/$BRANCH
python3 pager.py

