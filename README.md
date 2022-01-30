# Message Service

A simple message handling service built with python, flask, and mongodb

# Create docker container to test the service

cd msg-service

docker-compose up --build

---

# Running the service

## Open new terminal and login to environment

docker exec -it msg-service-py-mongo-1 /bin/bash

## Run with Flask

export FLASK_APP=message_service.py

flask run

---

# API

## Open new terminal to test API

docker exec -it msg-service-py-mongo-1 /bin/bash

---

## Read root

curl -v http://127.0.0.1:5000/

## Get all messages

curl -v http://127.0.0.1:5000/messages

## Get new messages

curl -v http://127.0.0.1:5000/messages/new

---

## Send message samples

curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/messages/send -d '{"message":"test message", "recipient":"george costanza"}'

curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/messages/send -d '{"message":"giddyup!", "recipient":"george costanza"}'

curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/messages/send -d '{"message":"I know what you did last summer", "recipient":"112233445566"}'

curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/messages/send -d '{"message":"Good morning!", "recipient":"kk@gmail.com"}'

---

## Delete multiple messages (using recipient key)

curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/messages/delete/multiple -d '{"recipient":"george costanza"}'

---
## Delete a single message (using message key)

curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/messages/delete/single -d '{"message":"Good morning!"}'

---

# Limitations

See limitations.txt file.


# Development environment

Ubuntu 18.04.5 LTS  (WSL2)

Docker Engine 20.10.12

Docker Compose v2.2.3



