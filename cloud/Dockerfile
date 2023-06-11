FROM python:3.7

RUN curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | bash

RUN apt update -y && \
	apt install bison flex libmariadb3 libmariadb-dev -y

COPY ./web /web
WORKDIR /web

RUN pip install -r requirements.txt

CMD python app.py