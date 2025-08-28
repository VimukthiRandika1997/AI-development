#!/usr/bin/env bash
# wait-for-db.sh

set -e

host="$1"
shift
cmd="$@"

echo "Waiting for Postgres at $host..."

until pg_isready -h "$host" -U "postgres"; do
  echo "Postgres is unavailable - sleeping 2s"
  sleep 2
done

echo "Postgres is up - executing command"
exec $cmd
