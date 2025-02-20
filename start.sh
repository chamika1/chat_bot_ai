#!/bin/bash
python main.py & gunicorn --bind 0.0.0.0:$PORT wsgi:app 