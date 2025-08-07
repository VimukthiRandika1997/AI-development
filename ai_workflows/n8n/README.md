# Building No-code AI workflows

The approach works on building AI Workflows using platforms like n8n

## Environment setup

```bash
# 01. Pull the official docker image for n8n
docker pull n8nio/n8n:latest 

# 02. Run the n8n container
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

# Optionally: run with docker-composer
# docker-compose.yml file contains the necessary data
docker compose up -d
```
