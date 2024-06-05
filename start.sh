#!/bin/bash

source .venv/bin/activate

export FLASK_APP=backend/service.py

cd frontend

npm run build

cd ..

flask run