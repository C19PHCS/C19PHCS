FROM python:3.8.2-slim-buster
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install make libpq-dev python3-dev gcc
WORKDIR /app

COPY . .

RUN make install
CMD [ "make", "start" ]
