#!/bin/bash

set -exo pipefail

pip freeze

python src/manage.py migrate --noinput
python src/manage.py collectstatic --noinput

if [[ -z ${DEVELOPMENT} ]]; then
	gunicorn src.config.asgi:application -k src.config.server.UvicornWorker
else
	python src/manage.py runserver 0.0.0.0:8000
fi
