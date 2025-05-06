#!/bin/sh


python3 manage.py makemigrations && python3 manage.py migrate
python3 manage.py loaddata api/fixtures/province.json
python3 manage.py loaddata api/fixtures/city.json

echo -ne '\n'
echo -ne '\n'

# python3 -m grpc_tools.protoc --proto_path=./protos --python_out=./ --grpc_python_out=./ ./protos/base_info.proto