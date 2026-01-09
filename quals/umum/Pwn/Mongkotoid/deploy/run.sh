#!/bin/bash
cd $(dirname $0)

if /home/pwn/pow; then
    python3 runner.py
else 
    echo "Incorrect POW"
fi

