FROM python:3.7-stretch

RUN apt-get update

COPY ./src /src
COPY requirements.txt /src/requirements.txt

RUN pip install -r /src/requirements.txt

# CMD scrape