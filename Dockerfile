FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
#RUN pip3 install -r /reruirements
#RUN pip install django_cleanup
#RUN pip install Pillow
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
    && pip install Pillow
#RUN pip install psycopg2
RUN mkdir /app
WORKDIR /app
copy ./app /app

