#!/bin/sh
python3 manage.py makemigrations && python3 manage.py migrate
echo -ne '\n'
echo -ne '\n'

