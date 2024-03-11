FROM python:3.9

RUN mkdir code

WORKDIR /code

RUN ls
COPY requirements.txt /code/

RUN pip install -r requirements.txt
COPY . /code/

RUN python manage.py makemigrations && python manage.py migrate

CMD  python manage.py runserver 