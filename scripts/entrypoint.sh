#!/usr/bin/env bash

set -e

RUN_MANAGE_PY='poetry run python -m blackshakara.manage'

echo 'Reading supervisor configuration...'
supervisorctl reread

echo 'Updating supervisor...'
supervisorctl update

echo 'Waiting for database...'
$RUN_MANAGE_PY wait_for_db

echo 'Making migrations...'
$RUN_MANAGE_PY makemigrations --noinput

echo 'Running migrations...'
$RUN_MANAGE_PY migrate --noinput

echo 'Collecting static files...'
$RUN_MANAGE_PY collectstatic --noinput

echo 'Starting supervisor...'
exec supervisord -c /opt/project/supervisord.conf
