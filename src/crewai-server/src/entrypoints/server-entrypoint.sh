#!/bin/bash

echo "> ============================="
echo "> Environment Settings"
echo "> ============================="
env
echo "> ============================="
echo "..."

echo "> ============================="
echo "> Activating Python Environment"
echo "> ============================="
source venv/bin/activate
echo "> Done"
echo "..."

echo "> ============================="
echo "> Starting FastAPI Server"
echo "> ============================="
python="/home/appuser/venv/bin/python"
uvicorn="/home/appuser/venv/bin/uvicorn"

$python $uvicorn resume_opt.main:app --host 0.0.0.0 --port 5000 --workers 1
