# Test task, Socketio chat + FastAPI REST
## Realised features:
 - Base API methods with auth through OAuth2 + JWT
 - Loading, crop and pictures saving in Database
 - Methods for chats: creating and deletion
 - Partitial functional of chats based on SocketIO (one socket for message proccessing, other for chat joining)
 - Pytest
 - Conterization of Backend and DB
 - Custom Swagger

## Things to do:
 - Realise chat based on built-in FastApi websockets
 - Conf files (deploy or local)
 - Increase test coverage
 - Mount sockets to web app (I couldn't)
 - Conf file for Kubernetes
 - Custom logging

## Run
docker compose build && docker compose up 

(sockets weren't containerized)
