# Descrição do Microsserviço

Este microsserviço foi desenvolvido em Go para fornecer uma funcionalidade simples de "dump" de banco de dados PostgreSQL via comandos executados em contêiner Docker. O serviço permite que um backup do banco de dados seja gerado através de uma solicitação HTTP.

## Estrutura do Microsserviço

- **Endpoint `/dump`**: Gera um backup (dump) do banco de dados PostgreSQL em um contêiner Docker.

## Principais Funcionalidades

- **Backup de Banco de Dados**: O microsserviço executa o `pg_dump` para gerar um dump do banco de dados PostgreSQL em um contêiner Docker. O arquivo de backup é salvo com um nome que inclui a data e hora atual no formato `backup_db_dd_mm_aaaa_hh_mm_ss.dump`.
- **Execução em Contêiner**: O backup é feito via execução de um comando `docker run` no contêiner oficial do PostgreSQL. Isso garante que o `pg_dump` é executado de forma isolada e com as variáveis de ambiente fornecidas.

## Requisitos

O serviço depende das seguintes variáveis de ambiente para acessar o banco de dados:

- **`PGPASSWORD`**: Senha do banco de dados.
- **`DB_HOST`**: Host do banco de dados.
- **`DB_PORT`**: Porta do banco de dados.
- **`DB_USER`**: Nome do usuário do banco de dados.
- **`DB_NAME`**: Nome do banco de dados.