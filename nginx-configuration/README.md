# Configuração de Servidor HTTPS com Nginx
Este repositório contém arquivos de configuração e instruções para configurar um servidor web seguro utilizando Nginx com suporte HTTPS.

## Descrição
O servidor web Nginx é configurado para lidar com conexões HTTP e HTTPS, redirecionando automaticamente solicitações HTTP para HTTPS. Ele também inclui configurações para servir conteúdo estático, proxy reverso para uma API e configurações para certificados SSL gerados pelo Certbot.

## Estrutura do Projeto
- nginx.conf: Arquivo de configuração principal do servidor Nginx, contendo as configurações para HTTP, HTTPS e outras rotas.
- .docker: Pasta contendo os arquivos de configuração para Docker.
    - certbot: Pasta com arquivos de configuração do Certbot.
        - conf: Pasta contendo configurações para o Certbot.
        - www: Pasta para armazenar arquivos temporários do Certbot.
    - nginx: Pasta contendo arquivos de configuração do Nginx.
        - html: Pasta para armazenar arquivos HTML e estáticos servidos pelo Nginx.
        - nginx.conf: Arquivo de configuração do Nginx.

## Funcionalidades
- Facilitação da utilização de Proxy Reverso;
- Uso de arquivos estáticos e definições de pastas;
- Definição de qualidade e segurança da aplicação;

## Definição de docker-compose para gerar o certificado SSL
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:latest
    ports:
      - "80:80" # Porta HTTP
      - "443:443" # Porta HTTPS
    volumes: # Mapeamento de volumes para o container NGINX, onde os arquivos de configuração e os arquivos estáticos são montados
      - .docker/nginx/nginx.conf:/etc/nginx/nginx.conf
      - .docker/nginx/html:/usr/share/nginx/html
      - .docker/nginx/html/static:/usr/share/nginx/html/static # Mapeamento do volume para os arquivos estáticos
      - .docker/certbot/conf:/etc/letsencrypt # Volumes de configuração do certbot para o NGINX
      - .docker/certbot/www:/var/www/certbot 
    restart: unless-stopped
    depends_on: # Dependência do container NGINX para que o container certbot seja iniciado antes 
      - certbot 

  certbot:
    image: certbot/certbot # Imagem do certbot
    container_name: certbot
    command: certonly --webroot -w /var/www/certbot --force-renewal --email example@email.com --agree-tos -d seven-renato.com.br # Comando para gerar o certificado SSL sempre que o container for iniciado
    # Com esse comando se torna possivel adquirir o certificado para o dominio devido, além de possuir também outros parâmetros possiveis de serem colocados para configuração de DNS e subdomínios
    volumes:
      - .docker/certbot/conf:/etc/letsencrypt
      - .docker/certbot/www:/var/www/certbot
    restart: on-failure
```

## Exemplo de Nginx.conf para utilização do HTTPs gerado pelo Certbot

```bash
events {
    # Limite de conexões simultâneas
    worker_connections 1024;
}

http {
    # Configurações iniciais do Web Server
    server_tokens off;
    charset utf-8;

    # Redirecionamento de HTTP para HTTPS
    server {
        listen 80 default_server;
        server_name seven-renato.com.br; # Nome do domínio
        
        # Configuração de certificado SSL, rota para validação de certificado
        location ~ /.well-known/acme-challenge/ { 
            root /var/www/certbot;
        }

        return 301 https://$host$request_uri;
    }

    # Configuração de rotas HTTPS do Web Server
    server {
        listen 443 ssl http2; 
        ssl_certificate /etc/letsencrypt/live/seven-renato.com.br/fullchain.pem; # Chaves de certificação SSL
        ssl_certificate_key /etc/letsencrypt/live/seven-renato.com.br/privkey.pem;
        server_name seven-renato.com.br; # Nome do domínio
        root /var/www/html;
        index index.php index.html index.html; # Página inicial do site, configuração de HTML que ira aparecer ao conectar no domínio sem especificar a página

        location / { # Configuração de rota base do site
            root /usr/share/nginx/html;  
            index index.html;  
        }

        location ~ /.well-known/acme-challenge/ { # Configuração de rota para validação de certificado
            root /var/www/certbot;
        }

        location /api/ { # Proxy reverso para a API do site que deve pertencer ou a mesma Network do Web Server ou ao mesmo Docker Compose
            proxy_pass http://api:8050/;  
        }
        
        location /static { # Configuração de rota para arquivos estáticos do site
            root /usr/share/nginx/html; 
            autoindex on;
        }
    }
}
```


## Comentários
Os arquivos presentes nesta pasta de exemplo, possuem comentários com o intuito de facilitar a compreensão da configuração do seu servidor!
