#!/bin/sh
python parseworker.py data/mls001/data.xml

python parseworker.py data/mls002/feed.json

python parseworker.py data/mls003/agents.csv
python parseworker.py data/mls003/offices.csv
python parseworker.py data/mls003/listings.csv

python dataworker.py
