#!/bin/sh
source ./venv/bin/activate
./venv/bin/uvicorn core.main:app --reload