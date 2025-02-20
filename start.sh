#!/bin/bash
gunicorn --worker-class=gevent --workers=1 --threads=4 --bind 0.0.0.0:$PORT wsgi:app 