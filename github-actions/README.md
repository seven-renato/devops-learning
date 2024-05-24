# Configurando o GitHub Actions para Construir e Publicar Imagens Docker

Este repositório demonstra como configurar o GitHub Actions para automatizar a construção e publicação de imagens Docker em um registro privado do GitHub Container Registry (GHCR).

## Estrutura do Diretório

.github/
├── workflows/
│   └── deploy-image.yml


O diretório `.github` contém os arquivos de configuração do GitHub Actions. O subdiretório `workflows` contém os arquivos YAML que definem os workflows do GitHub Actions. O arquivo `deploy-image.yml` define o workflow para construir e publicar as imagens Docker.

## Workflow `deploy-image.yml`

Este workflow é acionado sempre que há um push para a branch principal (`main`). Ele executa as seguintes etapas:

1. **Checkout do Repositório:** Clona o repositório no runner do GitHub Actions.
2. **Login no GHCR:** Autentica no GHCR usando o token de acesso do GitHub.
3. **Extração de Metadados:** Extrai metadados das imagens Docker, como tags e rótulos.
4. **Construção e Publicação da Imagem Flask:** Constrói a imagem Docker do Flask usando o `Dockerfile.flask`. Publica a imagem Docker no GHCR com a tag extraída na etapa 3.
5. **Construção e Publicação da Imagem Celery:** Constrói a imagem Docker do Celery usando o `Dockerfile.celery`. Publica a imagem Docker no GHCR com a tag extraída na etapa 3.

## Variáveis de Ambiente

O workflow utiliza as seguintes variáveis de ambiente:

- `REGISTRY`: URL do GHCR (ex: `ghcr.io`).
- `REPO`: Nome do repositório no GHCR (ex: `seu-usuario/seu-repositorio`).
- `FLASK_IMAGE_NAME`: Nome da imagem Docker do Flask (ex: `api-flask`).
- `CELERY_IMAGE_NAME`: Nome da imagem Docker do Celery (ex: `api-celery`).

## Exemplo de Uso

Para utilizar este workflow, siga estas etapas:

1. Crie um token de acesso pessoal no GitHub com as permissões `packages:write` e `contents:read`.
2. Adicione o token secreto criado (exemplo: `ghp_XkdpPTG0dwapldwa321030dawokadw`) ao seu repositório como um Secret do GitHub, substituindo-a pelo seu token de acesso assim como seria feito em uma variável de ambiente.
3. Defina as variáveis de ambiente `REGISTRY`, `REPO`, `FLASK_IMAGE_NAME` e `CELERY_IMAGE_NAME` no seu workflow.
4. Faça um push para a branch principal (`main`) para acionar o workflow.

## Observações

- Este é apenas um exemplo de workflow. Você pode adaptá-lo às suas necessidades específicas.
- Certifique-se de ter o Docker instalado no runner do GitHub Actions.
- Substitua os valores das variáveis de ambiente pelas suas informações.
- JAMAIS coloque seu token de acesso de forma exposta no seu repositório, isso pode gerar danos ao projeto além de acessos a sua conta de invasores.

## Melhorias Adicionais

- **Gerenciamento de Dependências:** Utilize o comando `docker-compose` para instalar as dependências antes de construir as imagens.
- **Testes Automatizados:** Adicione testes automatizados ao workflow para garantir a qualidade do código.
- **Deploy Automático:** Utilize o GitHub Actions para automatizar a implantação das imagens Docker em um ambiente de produção.

## Integração com API de Exemplo

O workflow também demonstra como integrar a API de exemplo com o Redis para filas de processamento. A API utiliza o Celery para enviar tarefas para uma fila Redis, onde são processadas em segundo plano.

## Código para subir imagens buildadas em Packages

```bash
docker build -f Dockerfile.celery  -t api-celery-devops-example --build-arg DATABASE_URL=postgresql://user:hashdb.com/github-actions .
# Enviar build-arg pois precisamos de um arquivo .env contudo estamos tratando com Dockerfile

docker build -f Dockerfile.flask -t api-devops-example .

docker tag api-celery-devops-example ghcr.io/seven-renato/api-celery-devops-example:latest # Dando uma tag com o intuito de...
docker tag api-devops-example ghcr.io/seven-renato/api-devops-example:latest

echo "ghp_XkdpPTG0dwapldwa321030dawokadw"  | docker login ghcr.io -u seven-renato --password-stdin # Conectar ao ghcr para fazer o push no container lembrar de colocar permissão para criação de packages e remoção na chave

docker push ghcr.io/seven-renato/api-celery-devops-example
docker push ghcr.io/seven-renato/api-devops-example
```




