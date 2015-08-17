#!/bin/sh
cd "$(dirname "$0")" || exit 1
source venv/bin/activate
exec python2 main.py
