#!/bin/bash

#bash script to setup the project and create a virtual environment
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r req.txt