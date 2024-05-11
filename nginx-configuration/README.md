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

## Comentários
Os arquivos presentes nesta pasta de exemplo, possuem comentários com o intuito de facilitar a compreensão da configuração do seu servidor!