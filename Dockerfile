FROM python:3.7.3-slim-stretch

WORKDIR /data/flywheel

COPY . /data/flywheel/


RUN apt-get update --assume-yes

RUN pip3 install --upgrade pip \
 && pip3 install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/data/flywheel
