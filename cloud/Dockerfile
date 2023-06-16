FROM python:3.7-bullseye

RUN curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | bash

RUN apt update -y && \
	apt install libmariadb3 libmariadb-dev -y

COPY ./web /web
WORKDIR /web

RUN pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:2809 wsgi:app
