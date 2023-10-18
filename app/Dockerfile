FROM python:3.11.4-slim-buster

RUN mkdir -p /home/app/
RUN mkdir -p /home/app/static/

WORKDIR /home/app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
