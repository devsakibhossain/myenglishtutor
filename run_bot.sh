#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv .venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
else
    source .venv/bin/activate
fi

python3 bot.py
