FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN pip3 install -r /reruirements

#RUN mkdir /app
#WORKDIR /app
#copy ./app /app
#RUN pip install  psycopg2

