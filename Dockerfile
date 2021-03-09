FROM ubuntu:latest

RUN apt-get update -y && apt-get upgrade -y && apt-get install python3 -y

COPY ./src /app

EXPOSE 8099

ENTRYPOINT python3 -m unittest discover -s app && python3 app/run.py
