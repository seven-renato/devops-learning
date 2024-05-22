# Como ter HTTPS no Localhost - localhost-https
Este guia irá ajudá-lo a configurar HTTPS no localhost utilizando Docker e Nginx. Vamos criar um certificado SSL auto-assinado, configurar o Nginx para utilizá-lo e mapear os volumes no Docker Compose.

## Passos

### 1. Gerar Certificados SSL Auto-Assinados

Primeiro, vamos criar o diretório para armazenar os certificados SSL:
```sh
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout .docker/nginx/certs/nginx-selfsigned.key -out .docker/nginx/certs/nginx-selfsigned.crt
```

### 2. Configurar o Docker Compose e seus Volumes
O arquivo docker-compose.yml deve ser configurado para mapear os volumes dos certificados SSL:

```yaml
services:
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - .docker/nginx/nginx.conf:/etc/nginx/nginx.conf
      - .docker/nginx/html:/usr/share/nginx/html
      - .docker/nginx/html/static:/usr/share/nginx/html/static
      - .docker/nginx/certs:/etc/nginx/certs # Definição do volume para os certificados SSL do Nginx auto-assinados
    restart: unless-stopped
    depends_on:
      - ghrcapi # Se for apenas para gerar o certificado essa parte não importa, no caso seriam os containers chamados no arquivo de configuração, nginx.conf
    networks:
      - internet

  redis:
    image: redis
    networks:
      - internet

  ghrcapi:
    image: ghcr.io/seven-renato/api-devops-example:latest
    environment:
      FLASK_APP: run
      FLASK_DEBUG: 1
    volumes:
      - .docker/nginx/html/static:/app/static
    ports:
      - "8050:8050"
    networks:
      - internet

  ghrc-celery-server:
    image: ghcr.io/seven-renato/api-celery-devops-example:latest
    environment:
      FLASK_APP: run
      DATABASE_URL: ${DATABASE_URL}
    depends_on:
      - redis
    networks:
      - internet

networks:
  internet:
    external: true
```

### 3. Configurar o NGINX
Edite o arquivo .docker/nginx/nginx.conf para configurar o Nginx a utilizar os certificados SSL:

```nginx
events {
    worker_connections 1024;
}

http {
    server_tokens off;
    charset utf-8;
    sendfile on;
    client_max_body_size 200M;

    server {
        listen 80 default_server; # Configuração para todo a chamada na porta 80 ser redirecionada a porta 443 (SSL)
        server_name localhost;

        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl;
        ssl_certificate /etc/nginx/certs/nginx-selfsigned.crt; # Colocar os arquivos gerados
        ssl_certificate_key /etc/nginx/certs/nginx-selfsigned.key; # De configuração para gerar os certificados
        server_name localhost;
        root /var/www/html;
        index index.php index.html index.html;

        location / {
            root /usr/share/nginx/html;  
            index index.html;  
        }
        
        location /api/ {
            proxy_pass http://ghrcapi:8050/;   # Proxy reverso para o container da API
        }
        
        location /static {
            root /usr/share/nginx/html; # Serviço de arquivos estáticos, para poder acessar imagens localmente através do localhost
            autoindex on;
        }
    }
}
```

### 4. Iniciar os serviços
Execute o Docker Compose para iniciar os serviços com o comando:

```sh
docker-compose up -d
```
