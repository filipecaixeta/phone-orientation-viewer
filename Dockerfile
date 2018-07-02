FROM python:3.6

MAINTAINER Filipe Caixeta

RUN pip install flask flask_socketio requests eventlet
COPY . /app
WORKDIR /app
CMD ["/app/start.sh"]
