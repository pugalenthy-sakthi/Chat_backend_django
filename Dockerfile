FROM python:3.12

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE djangochat.settings

WORKDIR /code

COPY . /code/

RUN pip install -r requirements.txt 

EXPOSE 8000

EXPOSE 3307

