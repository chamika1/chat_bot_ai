#!/bin/bash
gunicorn --worker-class=gthread --threads=4 --bind 0.0.0.0:$PORT wsgi:app 