#!/bin/bash
set -e

# Load .env file if it exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

PORT=${PORT:-8000}

echo "Starting MkDocs on port $PORT..."
mkdocs serve --dev-addr=0.0.0.0:$PORT
