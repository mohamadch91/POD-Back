FROM python:3.10
ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
COPY . /code/

RUN python manage.py makemigrations && python manage.py migrate

RUN ./rabbit.sh

CMD  python manage.py runserver 