#!/bin/bash

python="python3"
if ! command -v "$python" &>/dev/null; then
    echo "Error: failed to find Python 3 in PATH"
    exit 1
fi

function run(){
    python3 -m venv venv &&
    echo "python virtual environment venv created." &&
    
    . ./venv/bin/activate &&
    echo "virtual environment venv activated." &&
    
    pip install -r ./requirements.txt &&
    echo "installed python package dependencie." &&
    
    python3 utils/create_db.py &&
    echo "created database." &&
    
    python3 utils/populate_db.py &&
    echo "database populated." &&
    
    echo "Auditlog API is running. Please look at the documentation provided to perform curl requests. I hope you like it! -Subin"&&
    python3 app.py
    
}

run
