#!/bin/sh


python3 manage.py makemigrations && python3 manage.py migrate
python3 manage.py loaddata api/fixtures/province.json
python3 manage.py loaddata api/fixtures/commerce_brand.json
python3 manage.py loaddata api/fixtures/commerce_category.json
python3 manage.py loaddata api/fixtures/service_brand.json
python3 manage.py loaddata api/fixtures/service_category.json
python3 manage.py loaddata api/fixtures/city.json
python3 manage.py loaddata api/fixtures/sale_method.json
python3 manage.py loaddata api/fixtures/delivery_method.json
python3 manage.py collectstatic

echo yes
echo yes
echo yes


python3 manage.py pubSub > a.txt  2>&1 &
echo -ne '\n'
echo -ne '\n'

