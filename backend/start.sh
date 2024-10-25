#!/bin/bash

set -e

BASEDIR="$(realpath "$(dirname "${0}")")"
source "$BASEDIR/venv/bin/activate"
source "$BASEDIR/settings.env"

cd "$BASEDIR/src"
uvicorn main:app --reload --host $BIND_IP --port $BIND_PORT --env-file "$BASEDIR/settings.env"
