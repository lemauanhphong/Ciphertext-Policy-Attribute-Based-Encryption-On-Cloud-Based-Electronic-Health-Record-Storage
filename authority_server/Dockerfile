FROM python:3.7

RUN curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | bash

RUN apt update -y && \
	apt install bison flex libmariadb3 libmariadb-dev -y
	
RUN wget https://crypto.stanford.edu/pbc/files/pbc-0.5.14.tar.gz && \
	tar -xvf pbc-0.5.14.tar.gz && \
	cd pbc-0.5.14 && \
	./configure --prefix=/usr && \
	make && make install

RUN git clone https://github.com/JHUISI/charm.git && \
	cd charm && \
	./configure.sh && \
	make && make install

WORKDIR /web
COPY ./web/* .

RUN pip install -r requirements.txt

CMD python app.py
