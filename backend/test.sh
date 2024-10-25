#!/bin/bash

set -e

BASEDIR="$(realpath "$(dirname "${0}")")"
source "$BASEDIR/venv/bin/activate"
source "$BASEDIR/settings.env"

BASE_URL="http://$BIND_IP:$BIND_PORT" pytest "$BASEDIR/tests"/*
