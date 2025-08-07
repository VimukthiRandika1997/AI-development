#!/bin/bash

# 01. Pull the docker latest n8n docker image
docker pull n8nio/n8n:latest 

# 02. Run the docker image by mounting a directory
mkdir n8n_data || true

export N8N_BASIC_AUTH_USER="admin"     # set your username
export N8N_BASIC_AUTH_PASSWORD="admin" # set your secure password

docker run -it --rm \
-p 5678:5678 \
-e N8N_BASIC_AUTH_ACTIVE=true \
-e N8N_BASIC_AUTH_USER=$N8N_BASIC_AUTH_USER \
-e N8N_BASIC_AUTH_PASSWORD=$N8N_BASIC_AUTH_USER \
-v n8n_data:/home/node/.n8n \
n8nio/n8n