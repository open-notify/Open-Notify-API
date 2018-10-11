FROM python:2-alpine

RUN apk update && apk add musl-dev gcc && rm -rf /var/cache/apk/*

COPY . /open-notify
WORKDIR /open-notify

RUN cd /open-notify && pip install -r requirements.txt
CMD python app.py