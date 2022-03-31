FROM python:3.8-slim-buster
MAINTAINER Brandon Spendlove <brandon-spendlove@hotmail.co.uk>

ARG HOST
ARG PORT

WORKDIR /code
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ADD opencoa_api/ /code/opencoa_api
RUN ls /code

CMD uvicorn opencoa_api.main:app --host=${HOST} --reload