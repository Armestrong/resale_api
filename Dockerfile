FROM python:3.7-alpine
MAINTAINER Resale API Ltd

ENV PYTHONUNBUFFERED 1

# TO COPY MY LIBS AND CREATE A NEW-ONE
COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

# TO RUN MY APPLICATION
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# FOR SECURITY

RUN mkdir -p /staticfiles
RUN adduser -D user
RUN chown -R user:user /staticfiles/
RUN chmod -R 755 /staticfiles
USER user
