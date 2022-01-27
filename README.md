# message-service

MessagingService in Python

> message_service.py

## Flask-MongoDB-Docker container environment

### Terminal 1

docker-compose up --build

### Terminal 2

docker inspect message-service-py-mongo-1

> IP may change when container is run, so need to get from inspect
> Update IP in core_service.py

docker cp message_service.py message-service-py-mongo-1:/var/www/html

### Terminal 3

docker exec -it message-service-py-mongo-1 /bin/bash

export FLASK_APP=message_service.py

flask run

### Terminal 4

docker exec -it message-service-py-mongo-1 /bin/bash

curl -v http://127.0.0.1:5000/

curl -v http://127.0.0.1:5000/messages/

curl -v http://127.0.0.1:5000/messages/new

curl -v http://127.0.0.1:5000/messages/send

cd /var/www/html

python3 core_test.py