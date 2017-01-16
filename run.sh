#!/bin/bash
cd "$(dirname ${BASH_SOURCE[0]})"
python ./src/main.py > log.txt
