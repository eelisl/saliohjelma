#!/bin/bash

if [ ! -f .env ]; then
    echo ".env file not found."
    echo "Please copy .env.example to .env and update the necessary configuration values."
    exit 1
fi

pip install -r requirements.txt

if [[ "$1" == "--dev" ]]; then
    export FLASK_DEBUG=1
fi

flask run