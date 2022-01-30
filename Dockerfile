FROM mongo:latest

COPY message_service.py /app

WORKDIR /app

# install Python 3
RUN apt-get update && apt-get install -y python3 python3-pip python3-flask curl

RUN pip3 install pymongo mockupdb

EXPOSE 27017
