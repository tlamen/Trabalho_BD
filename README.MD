# Projeto final da disciplina Bancos de Dados 

Esse trabalho utilizar o framework de desenvolvimento Flask com ligação com o SGBD PostgreSQL. O desenvolvimento foi feito em um ambiente de desenvolvimento linux, as funcionalidades não foram testadas em outro sistema operacional e adaptações podem ser necessárias. Para rodar o projeto localmente, é necessário seguir as seguintes etapas:

## 1. Criar base de dados postgreSQL e usuário

Após instalar o PostgreSQL (por meio do link: https://www.postgresql.org/download/), é necessário uma série de comandos para criar a base de dados do projeto.

Entre em uma sessão interativa do postgresql:

```bash
sudo -iu postgres psql
```
Crie o banco de dados do projeto:

```bash
CREATE DATABASE flask_db;
```

Depois, crie um usuário para o banco de dados. Utilize uma senha segura:

```bash
CREATE USER sammy WITH PASSWORD 'password';
```

Então conceda acesso para o usuário ao banco de dados:

```bash
GRANT ALL PRIVILEGES ON DATABASE flask_db TO sammy;
```

Para ter certeza de que o processo ocorreu como o esperado, certifique-se que o banco de dados 'flask_db' aparece ao listar os bancos de dados:

```bash
\l
```

## 2. Instalar Flask e psycopg2

Como pré-requisitos, é necessário a instalação do python3 (https://www.python.org/downloads/) e do pip (https://pip.pypa.io/en/stable/cli/pip_install/). Recomendo que ambos sejam instalados nas versões mais recentes.
Com isso, basta instalar o pacote com o comando:

```bash
pip install Flask psycopg2-binary
```

## 3. Preparar a base de dados

Para povoar a base de dados e iniciar o projeto, primeiro verifique que as variáveis de ambiente estão devidamente estabelecidas:

```bash
export DB_USERNAME="sammy"
export DB_PASSWORD="password"
```

Obs.: Caso o resto do programa retorne erro relacionado às variáveis de ambiente, é possível modificar temporariamente as linhas 8 e 9 do arquivo "init_db.py" para colocar as variáveis corretas manualmente, sem uso de variáveis de ambiente. Não é uma prática segura, mas é aplicável em uma execução local.

Em seguida, basta rodar a aplicação Flask e visitar a URL indicada no terminal usando o navegador:

```bash
flask run
```