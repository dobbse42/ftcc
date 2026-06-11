#!/bin/bash

# $1 holds name of the compilation run
$REQS_NAME="requirements_$1.txt"
# $2 holds whether or not to activate the new venv

# create the venv and install requirements using uv
uv venv .venv $1
uv pip install --python $1 -r $REQS_NAME
