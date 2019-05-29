FROM python:latest

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

RUN pip install --upgrade pip

ADD /requirements/development.txt ./requirements/
ADD /requirements/requirements.txt ./requirements/
RUN pip install --no-cache-dir -r ./requirements/development.txt

ADD . /usr/src/app/