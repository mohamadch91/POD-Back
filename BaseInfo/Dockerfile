FROM python:3.11
ENV PYTHONUNBUFFERED 1

RUN mkdir code

WORKDIR /code

COPY . /code/

RUN pip install --upgrade pip

COPY requirements.txt /code/

RUN pip install -r requirements.txt

RUN python manage.py makemigrations && python manage.py migrate
RUN python3 manage.py loaddata api/fixtures/province.json
RUN python3 manage.py loaddata api/fixtures/commerce_brand.json
RUN python3 manage.py loaddata api/fixtures/commerce_category.json
RUN python3 manage.py loaddata api/fixtures/service_brand.json
RUN python3 manage.py loaddata api/fixtures/service_category.json
RUN python3 manage.py loaddata api/fixtures/city.json



