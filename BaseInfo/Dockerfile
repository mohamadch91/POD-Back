FROM python:3.9
ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY requirments.txt /code/

RUN pip install -r requirments.txt
COPY . /code/

RUN python manage.py makemigrations && python manage.py migrate
RUN python3 manage.py loaddata api/fixtures/province.json
RUN python3 manage.py loaddata api/fixtures/city.json


CMD  python manage.py runserver 