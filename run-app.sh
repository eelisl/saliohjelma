#!/bin/bash

pip install -r requirements.txt

for arg in "$@"; do
    case $arg in
        --dev)
            export FLASK_DEBUG=1
            echo "Debug enabled."
            ;;
        --init)
            if [ -f ./database.db ]; then
                echo "Database found. Delete existing database first to initialise new."
                continue
            fi
            if [ ! -f ./database/schema.sql ]; then
                echo "Schema file ./database/schema.sql not found."
                exit 1
            fi
            if [ ! -d ./database ]; then
                mkdir -p ./database
            fi
            sqlite3 database.db < ./database/schema.sql
            sqlite3 database.db < ./database/init.sql
            echo "Database initialised."
            ;;
    esac
done

flask run