#!/bin/sh

export build_type="local"
cd fastapi-server/src && sh scripts/docker.build.sh && cd - || exit
cd resume_opt/src && sh scripts/docker.build.sh && cd - || exit
