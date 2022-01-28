# message-service

MessagingService in Python

> message_service.py

## Flask-MongoDB-Docker container environment

### Terminal 1

docker-compose up --build

### Terminal 2

docker inspect msg-service-py-mongo-1

> IP may change when container is run, so need to get from inspect
> Update IP in core_service.py

docker cp message_service.py msg-service-py-mongo-1:/var/www/html

### Terminal 3

docker exec -it msg-service-py-mongo-1 /bin/bash

cd /var/www/html

export FLASK_APP=message_service.py

flask run

### Terminal 4

docker exec -it msg-service-py-mongo-1 /bin/bash


#### Test curl commands 

curl -v http://127.0.0.1:5000/

curl -v http://127.0.0.1:5000/messages

curl -v http://127.0.0.1:5000/messages/new

curl -X POST -H "Content-Type: application/json" -d '{"message":"test message", "recipient":"george costanza"}' http://127.0.0.1:5000/messages/send

curl -X POST -H "Content-Type: application/json" -d '{"recipient":"george costanza"}' http://127.0.0.1:5000/messages/delete/multiple

curl -X POST -H "Content-Type: application/json" -d '{"message":"test message"}' http://127.0.0.1:5000/messages/delete/single




### testing

docker cp core_test.py msg-service-py-mongo-1:/var/www/html

docker exec -it msg-service-py-mongo-1 /bin/bash

cd /var/www/html

python3 core_test.py