FROM python:3.11.0-slim AS builder
ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code


COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt


FROM python:3.11.0-slim
ENV PYTHONUNBUFFERED 1


RUN mkdir /code
WORKDIR /code
RUN pip install gunicorn

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . /code/






