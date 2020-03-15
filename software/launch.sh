#!/bin/bash

BRANCH=$(hostname)

cd $(dirname $0)
git fetch origin
git checkout origin/$BRANCH
source venv/bin/activate
pip install -r ../requirements.txt
python3 pager.py

