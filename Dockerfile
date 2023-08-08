FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirments.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirments.txt
COPY ./core /app