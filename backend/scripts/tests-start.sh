#! /usr/bin/env bash
set -e
set -x

python src/backend_pre_start.py

bash scripts/test.sh "$@"
