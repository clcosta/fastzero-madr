# FastZero - Meu Acervo Digital de Romances (MADR)

Este repositório é um projeto de estudo de FastAPI. Ele é proposto pelo [Dunossauro](https://github.com/dunossauro) em seu curso de [FastAPI do Zero](https://github.com/dunossauro/fastapi-do-zero).
O projeto consiste em criar uma API básica porém extremamente completa. Com testes, documentação, autenticação, autorização, etc.

## Decisões técnicas

Algumas escolhas deste projeto foram baseadas na documentação do curso. Porém, algumas escolhas são pessoais de minha preferência. Observando sempre a documentação exigida para o projeto.

### Autenticação

A senha é armazenada no banco de dados como um *hash* e nunca é retornada para o cliente. A principal diferença é que eu utilizo o *bcrypt* para fazer o *hash* da senha. Para ter uma conscistência (caso necessário) entre os hashs eu disponibilizo uma variável de ambiente para o **salt** do *bcrypt*. Não é recomendado setar o **salt** a não ser que você tenha um motivo muito forte para isso. É possível ver todas as variáveis de autenticação [aqui](https://github.com/clcosta/fastzero-madr/blob/master/madr/infra/configs.py#L24).

Além disso, em produção é **PRECISO** setar uma valor **FORTE** para a variável **_SECRET_KEY_**. No código o padrão é uma string de apenas **24 caracteres**.

### Linguagem do Projeto

Apesar de ser um projeto de estudo, por questões de costume e preferência ele é desenvolvido com variáveis e nomeclaturas em **inglês**. Para se aproximar com o domínio em momentos exigidos pela documentação é realizado o uso de aliases em **português**. Em momentos de interação com o usuário as mensagens também estão em **português**.

### Formatação do projeto

Meus formatores estão sinalizados no arquivo de **pre-commit**. Utilizando o pacote **_pre-commit_** para formatar o código antes de subir as alterações. Você pode olhar os detalhes [aqui](https://github.com/clcosta/fastzero-madr/blob/master/.pre-commit-config.yaml).

Da mesma forma, utilizo o **editorconfig** para manter a formatação do código consistente em diferentes editores. Você pode olhar os detalhes [aqui](https://github.com/clcosta/fastzero-madr/blob/master/.editorconfig).

### Organização de pastas

Diferente da abordagem do curso, tenho preferência por utilizar pastas e modulos para me orientar melhor. Também costumo utilizar o **\_\_init\_\_.py** para evitar _imports_ muito longos e simplificar o *start* da aplicação. Segue a estrutura do projeto:

```bash
|-- README.md
|-- alembic.ini
|-- db.sqlite3
|-- docker-compose.yaml
|-- dockerfile
|-- entrypoint.sh
|-- madr
|   |-- __init__.py  # <-- Aqui está um import do meu app (FastAPI)
|   |-- database
|   |   |-- __init__.py
|   |   |-- database.py
|   |   |-- migrations
|   |   |   |-- README
|   |   |   |-- env.py
|   |   |   |-- script.py.mako
|   |   |   `-- versions
|   |   |       `-- 6e9827dc8a01_create_default_tables.py
|   |   `-- models.py
|   |-- infra
|   |   |-- __init__.py
|   |   `-- configs.py
|   |-- server
|   |   |-- __init__.py
|   |   |-- routers
|   |   |   |-- accounts.py
|   |   |   |-- books.py
|   |   |   `-- novelists.py
|   |   |-- schemas
|   |   |   |-- accounts.py
|   |   |   |-- auth.py
|   |   |   |-- base.py
|   |   |   |-- books.py
|   |   |   `-- novelist.py
|   |   `-- services
|   |       |-- account_service.py
|   |       |-- auth_service.py
|   |       |-- book_service.py
|   |       `-- novelist_service.py
|   |-- tests
|   |   |-- conftest.py
|   |   |-- test_accounts.py
|   |   |-- test_auth.py
|   |   |-- test_base_api.py
|   |   |-- test_books.py
|   |   |-- test_database.py
|   |   |-- test_novelists.py
|   |   |-- test_saniteze_string.py
|   |   `-- test_security.py
|   `-- tools
|       |-- hash.py
|       |-- sanitize.py
|       `-- security.py
|-- poetry.lock
`-- pyproject.toml
```

## Instalar e rodar o projeto

Seguindo para a instalção e execução do projeto. Temos algumas opções. Recomendo utilizar o **Docker**.

### Docker

Para rodar o projeto com Docker é necessário ter o Docker e o Docker Compose instalados. Com isso, basta rodar o comando na raiz do projeto:

```bash
$ docker-compose up
```

### Poetry

É necessário ter o [Poetry](https://python-poetry.org/docs/) instalado.

1. Crir um ambiente virtual com o Poetry:

```bash
$ poetry shell
```

2. Instalar as dependências do projeto:

```bash
$ poetry install
```

3. Rodar o projeto:

```bash
$ task run
```
