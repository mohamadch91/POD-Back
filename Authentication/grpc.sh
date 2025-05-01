#!/bin/sh
python3 manage.py makemigrations && python3 manage.py migrate

echo -ne '\n'
echo -ne '\n'



# python3 -m grpc_tools.protoc --proto_path=./protos --python_out=./ --grpc_python_out=./ ./protos/user.proto