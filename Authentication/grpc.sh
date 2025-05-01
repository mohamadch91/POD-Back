#!/bin/sh
python3 manage.py makemigrations && python3 manage.py migrate


python3 manage.py pubSub > a.txt  2>&1 &
echo -ne '\n'
echo -ne '\n'

