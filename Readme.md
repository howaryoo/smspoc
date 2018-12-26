# SMS Service 

Implementation in Python using a micro-services architecture including:

 * Restful API (https://github.com/kennethreitz/responder)
 * message queue (rabbitMQ)
 * Workers (rabbitMQ listeners)

Plain tokens are used for authentication in the API

# Usage

# requirements

 * docker (v 18+)
 * docker-compose
 * make utility

## Set nexmo credentials

    in file: projects/sms/docker/COMPOSE.env
    
    edit the environment variables:
    
    
    NEXMO_KEY=**************
    NEXMO_SECRET=*******************

## Build docker images
    ~/projects/sms⟫ make build

## Run
    ~/projects/se⟫ make up

the services are then available from localhost:

 * API: http://localhost:5000/docs?url=http://localhost:5000/static/schema.yml
 * Database: (ArangoDB) http://localhost:8529/_db/SMS/_admin/aardvark/index.html#login
 * RabbitMQ: http://localhost:15672/#/
        
# Limitations

 * Some function calls are BLOCKING
 * No transactions used, race conditions possible
 * tokens have no TTL

# Flow example

## Auth

### register
    curl -X POST "http://localhost:5000/auth/register" \
        -H "accept: */*" -H "Content-Type: application/json" \
        -d "{\"login\":\"me\",\"password\":\"secret\",\"mobile\":\"15141122334\"}"

### login

    curl -X POST "http://localhost:5000/auth/login" \
        -H "accept: */*" -H "Content-Type: application/json" \
        -d "{\"login\":\"me\",\"password\":\"secret\"}"

The plain token is returned 

### verify received SMS code

The plain token is used as a header param

    curl -X POST "http://localhost:5000/auth/verify" \
        -H "accept: */*" -H "sms-token: uO00Bjw3-ac" \
        -H "Content-Type: application/json" -d "{\"confirmation\":\"rXw5\"}"


## Send SMS


The SMS service can be used.

    curl -X POST "http://localhost:5000/sms/queue" \
        -H "accept: */*" -H "sms-token: uO00Bjw3-ac" \
        -H "Content-Type: application/json" \
        -d "{\"to\":\"15141122334\",\"message\":\"done!\"}"
