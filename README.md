# Festa IFC - Sistema de organização

Aplicação em Streamlit para auxiliar a organização de uma festa no IFC Campus Blumenau. O sistema permite registrar:

- alimentos a serem vendidos
- fornecedores dos insumos
- insumos doados
- pessoas que vão trabalhar na festa (alunos, pais de alunos e servidores)
- preços de venda dos alimentos

## Tecnologias utilizadas

- Streamlit
- SQLAlchemy
- SQLite para testes locais
- MySQL em ambiente de produção
- uv como gerenciador de pacotes

## Estrutura do projeto

```text
.
├── README.md
├── .gitignore
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── database.py
│   └── models.py
└── data/
```

## Requisitos

- Python 3.12+
- uv instalado

## Configuração inicial

1. Instale as dependências:

```bash
uv sync
```

2. Para uso local com SQLite, basta executar:

```bash
uv run streamlit run src/app.py
```

3. Para uso em produção com MySQL, defina a variável de ambiente `MYSQL_URL` e configure o ambiente para produção:

```bash
export APP_ENV=production
export MYSQL_URL="mysql+pymysql://usuario:senha@host:3306/festa_ifc"
uv run streamlit run src/app.py
```

No Windows PowerShell:

```powershell
$env:APP_ENV = "production"
$env:MYSQL_URL = "mysql+pymysql://usuario:senha@host:3306/festa_ifc"
uv run streamlit run src/app.py
```

## Como o sistema funciona

A aplicação usa SQLAlchemy para manter as entidades em banco de dados. O SQLite é usado para testes locais e o MySQL é usado em produção, conforme a organização da festa.

As páginas de CRUD permitem:

- criar registros
- listar registros
- atualizar registros
- excluir registros

para as entidades principais do projeto.

## Observações

- Os insumos são tratados como itens doados, com a possibilidade de indicar o fornecedor responsável.
- A gestão de pessoas considera os papéis de aluno, pai de aluno e servidor.
- O preço de venda dos alimentos é calculado e armazenado junto ao cadastro do item.
