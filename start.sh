#!/bin/sh

. ./venv/bin/activate
python3 main.py >"./log-$(date +%Y%m%d%H%M%S)" 2>&1

