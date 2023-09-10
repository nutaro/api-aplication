## Rodar aplicacao local
necessário **docker-compose, docker, makefile**
```sh
make build
make up
make migrations
make tests
```

## Deploy
acesse o cluster kubernetes
```sh
kubectl apply -f lask_app.yml
```
assim que as pods subirem acesse a pod do flask 
```sh
kubectl exec --stdin --tty pod/flask_pod -- /bin/bash
apt install vim
vim alembic.ini
```
edite a *linha 53 sqlalchemy.url* colocando os dados da base
```sh
alembic upgrade head
exit
```

## Requests
```sh
curl --location --request POST 'http://{address}:{port}/user' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "victor",
    "email": "nutaro@protonmail.com",
    "role": "admin"
}'
curl --location --request GET 'http://{address}:{port}/user/{user_id}/role'
```

## Query
dentro do arquivo *query.sql*

## Problema 6
provavelmente dentro do modulo *core.settings* a constante WALLET_X_TOKEN_MAX_AGE não foi setada

## Problema 7
dentro do arquivo *code_review.sql*

## Problema 8
Adapter
**intent**
Convert the interface of a class into another that the client expects. Adapter lets classes work together that coudn't otherwise because of incompatible interfaces
Bridge
**Intent**
Decouple an abstraction from its implementation so that the two ca vary independetily
**comentários**
No exemplo citado eu teria um sender definindo uma interface comum para envios e suas implementações envios de e-mails, sms, etc...