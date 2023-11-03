#!/bin/sh

# Run database migration
flask db upgrade

# Run webserver
exec gunicorn --bind 0.0.0.0:80 "app:create_app()"
