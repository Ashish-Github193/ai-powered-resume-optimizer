#!/bin/bash

cd ./deploy/local

mkdir -p ./data/main/shared

docker compose -f docker-compose.yml up -d \
    --remove-orphans
