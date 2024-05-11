# devops-learning
Repositório que foca em salvar aprendizados relacionados ao estudo de Devops, aprendidos durante as experiências profissionais e estudos.

# Projetos Demonstrados
Este repositório contém uma série de projetos e exemplos que abordam diferentes aspectos de desenvolvimento e operações (DevOps). Abaixo está um resumo de cada projeto presente neste repositório:

## Configuração de Servidor HTTPS com Nginx - nginx-configuration
Este projeto demonstra como configurar um servidor web seguro utilizando o Nginx com suporte HTTPS. Ele inclui arquivos de configuração para o Nginx e Docker, bem como instruções sobre como configurar certificados SSL com o Certbot. O servidor é configurado para lidar com conexões HTTP e HTTPS, redirecionando automaticamente solicitações HTTP para HTTPS. Além disso, inclui configurações para servir conteúdo estático e proxy reverso para uma API.

## GitHub Actions para Construir e Publicar Imagens Docker - github-actions
Neste projeto, é demonstrado como configurar o GitHub Actions para automatizar a construção e publicação de imagens Docker em um registro privado do GitHub Container Registry (GHCR). O workflow definido no arquivo deploy-image.yml é acionado sempre que há um push para a branch principal. Ele utiliza variáveis de ambiente para definir a URL do GHCR, o nome do repositório, o nome das imagens Docker do Flask e do Celery, entre outras configurações. O workflow extrai metadados das imagens Docker, constrói e publica as imagens no GHCR.

## Como consumir Imagens de Packages - ncga-dockercompose
Neste projeto, é demonstrado utilizando o Docker Compose formas de utilizar as imagens já buildadas, facilitando assim o processo de deploy da aplicação além de ajudar a manter os códigos sem inconsistências entre diferentes versões. O exemplo é dado utilizando NGINX contudo pode ser utilizado outro Web Server como Apache por exemplo, dado que está tudo utilizando Docker para implementar.
