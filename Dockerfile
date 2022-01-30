FROM mongo:latest

COPY . /app

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip python3-flask curl

RUN pip3 install pymongo mockupdb

EXPOSE 27017
