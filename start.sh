#!/bin/bash

set -e

BASEDIR="$(realpath "$(dirname "${0}")")"

"$BASEDIR/backend/start.sh" &
BACKEND_PID=$!

# "$BASEDIR/frontend/start.sh" &
# FRONTEND_PID=$!

trap "echo 'Terminating...'; kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT

wait $BACKEND_PID $FRONTEND_PID

trap - SIGINT
