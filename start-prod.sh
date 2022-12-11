#!/bin/bash -e

source .prod_env
python manage.py collectstatic
gunicorn --certfile=certificate.crt --keyfile=private.key -b '0.0.0.0:8001' system.wsgi
