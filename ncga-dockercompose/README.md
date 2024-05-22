# Como Consumir Imagens de Packages - ncga-dockercompose

Este projeto apresenta uma configuração do Docker Compose para facilitar o consumo de imagens Docker já disponíveis em um registro privado, neste caso, no GitHub Container Registry (GHCR). Ele utiliza serviços como Nginx, Certbot, Redis, Flask e Celery para exemplificar um ambiente de desenvolvimento e produção.

## Configuração do Docker Compose
```yaml
version: '3.8' # Versão do Docker Compose

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
      - app # Extremamente necessário

  certbot:
    image: certbot/certbot # Imagem do certbot
    container_name: certbot
    command: certonly --webroot -w /var/www/certbot --force-renewal --email seven-renato@gmail.com --agree-tos -d seven-renato.com.br # Comando para gerar o certificado SSL sempre que o container for iniciado
    volumes:
      - .docker/certbot/conf:/etc/letsencrypt
      - .docker/certbot/www:/var/www/certbot
    restart: on-failure
  
  redis:
    image: redis # Imagem do Redis

  app:
    image: ghcr.io/seven-renato/api-devops-example:latest # Imagem da aplicação Flask criada e publicada no GHCR
    environment:
      FLASK_APP: run
      FLASK_DEBUG: 1
    volumes: # Configuração de volumes para o container da aplicação Flask para uso dos arquivos estáticos
      - .docker/nginx/static:/app/static
    ports:
      - "8050:8050"

  celery:
    image: ghcr.io/seven-renato/api-celery-devops-example:latest # Imagem do Celery criada e publicada no GHCR
    environment: 
      FLASK_APP: run
      DATABASE_URL: ${DATABASE_URL}
    depends_on:
      - redis
``` 

Este arquivo Docker Compose configura diferentes serviços para suportar uma aplicação Flask com Celery, incluindo um servidor web Nginx com suporte HTTPS, um serviço Certbot para gerenciamento de certificados SSL, um servidor Redis para armazenamento de dados em cache e filas de mensagens, e os serviços principais da aplicação Flask e Celery. Com ele como base você pode criar o seu próprio para um devido contexto de aplicação, sem necessidade de linguagem, apenas mantendo as configurações estabelecidas pra a aquisição de certificado SSL.




