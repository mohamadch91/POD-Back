#!/bin/sh
python3 manage.py pubSub > /dev/null  2>&1 &
echo -ne '\n'
echo -ne '\n'

