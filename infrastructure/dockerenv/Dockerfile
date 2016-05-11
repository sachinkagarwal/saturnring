#FROM python:2.7
FROM ubuntu:xenial
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD saturn-requirements.txt /code/
COPY django-admin-changelist-stats-0.2.tar.gz /code/
RUN apt-get update -yqq
RUN apt-get install gcc python-pip -y
RUN apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev -y
RUN apt-get install libpq-dev -y
RUN apt-get install libsqlite3-dev -y
RUN pip install --index-url=http://pypi.python.org/simple/ --trusted-host pypi.python.org  -r saturn-requirements.txt
RUN pip install --no-index --find-links=file:///code/django-admin-changelist-stats-0.2.tar.gz django-admin-changelist-stats==0.2
#RUN mkdir -p /data/saturnringlog/
#RUN mkdir -p /data/saturnringconfig/
RUN echo "cryptokey_pleasechange" > /data/saturnringconfig/saturnkey
#ADD . /code/
