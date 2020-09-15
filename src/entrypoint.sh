#!/bin/sh

echo RUNNING_ENTRYPOINT ====================
sleep 2
python manage.py migrate
sleep 1
echo RUNNING_TESTS ===================
python manage.py test src.library_backend.tests

exec "$@"
