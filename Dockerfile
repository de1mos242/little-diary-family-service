FROM python:3.8
MAINTAINER Denis Yakovlev de1m0s242@gmail.com

RUN apt-get update && apt-get install -y \
  libpq-dev \
  python-dev

RUN mkdir /code
WORKDIR /code

COPY requirements.txt setup.py ./
RUN pip install -r requirements.txt
RUN pip install -e .

COPY family_api family_api/
COPY migrations migrations/

EXPOSE 5000
