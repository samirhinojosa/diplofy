FROM python:latest

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

ADD requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD . /usr/src/app/