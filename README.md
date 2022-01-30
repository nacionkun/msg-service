# message-service

MessagingService in Python

> message_service.py

## Flask-MongoDB-Docker container environment

### Terminal 1

docker-compose up --build

docker inspect msg-service-py-mongo-1

docker cp message_service.py msg-service-py-mongo-1:/app

docker exec -it msg-service-py-mongo-1 /bin/bash

export FLASK_APP=message_service.py

flask run

docker exec -it msg-service-py-mongo-1 /bin/bash


#### Test curl commands 

curl -v http://127.0.0.1:5000/

curl -v http://127.0.0.1:5000/messages

curl -v http://127.0.0.1:5000/messages/new

curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/messages/send -d '{"message":"test message", "recipient":"george costanza"}'

curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/messages/delete/multiple -d '{"recipient":"george costanza"}'

curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/messages/delete/single -d '{"message":"test message"}'

