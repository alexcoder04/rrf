#!/bin/sh

. ./venv/bin/activate
python3 main.py >>./applog 2>&1

