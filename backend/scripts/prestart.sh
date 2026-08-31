#! /usr/bin/env bash

set -e
set -x


if [[ "$BACKEND__ENVIRONMENT" == "local" ]] || 
    [[ "$BACKEND__ENVIRONMENT" == "development" ]] || 
    [[ "$BACKEND__ENVIRONMENT" == "staging" ]] ||
    [[ "$BACKEND__ENVIRONMENT" == "production" ]]; then
    echo "Generate JWT certificates"
    ./scripts/create_certs.sh
# elif [[ "$BACKEND__ENVIRONMENT" == "production" ]] || [[ "$BACKEND__ENVIRONMENT" == "staging" ]]; then
#     echo "Verify JWT certificates exist in production"
#     if [[ ! -f "./certificates/jwt-private.pem" ]] || [[ ! -f "./certificates/jwt-public.pem" ]]; then
#         echo "ERROR: JWT keys are missing in production. Please generate them manually." >&2
#         exit 1
#     fi
else
    echo "ERROR: Invalid ENVIRONMENT value: '$BACKEND__ENVIRONMENT'. Expected: local, staging, or production." >&2
    exit 1
fi

# Let the DB start
echo "Waiting for database to start"
python src/backend_pre_start.py

# Run migrations
echo "Run database migrations"
alembic upgrade head

# Create initial data in DB
echo "Create initial data in DB"
python src/initial_data.py
exec "$@"