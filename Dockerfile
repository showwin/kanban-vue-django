FROM python:3.6.4-jessie
MAINTAINER showwin <showwin.czy@gmail.com>

RUN apt-get -y update && \
    apt-get -y install vim-tiny 

EXPOSE 3000
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

WORKDIR /app

ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ADD . /app
