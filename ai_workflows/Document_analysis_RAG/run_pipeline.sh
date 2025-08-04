#!/bin/bash

# 01. Create emebeddings and save them to vector DB
python3 populate_database.py

# 02. Run eval
pytest -s