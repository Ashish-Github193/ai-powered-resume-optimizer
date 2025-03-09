#!/usr/bin/env bash

PROJECT_NAME="fastapi-server"
DOCKER_IMAGE_NAME="$PROJECT_NAME"

echo "Running: docker build \
    -t $DOCKER_IMAGE_NAME \
    . \
    || exit
    "

docker buildx build  \
    -t "$DOCKER_IMAGE_NAME" \
    . \
    || exit

if ! command -v slim >/dev/null 2>&1; then
    echo "slim not found"
    exit 1
fi

#slim build \
#    --include-shell \
#    --include-path /usr/local \
#    --include-path /home/appuser \
#    --include-path /usr/lib/x86_64-linux-gnu \
#    "$DOCKER_IMAGE_NAME":latest \
#    || exit
