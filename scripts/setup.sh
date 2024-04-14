#!/bin/sh
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
./venv/bin/python -m spacy download ru_core_news_lg
