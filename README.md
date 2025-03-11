# Pipeline ETL para Extração e Carga de Dados

Este projeto implementa um pipeline ETL (Extract, Transform, Load) para extrair dados de PDFs e planilhas, transformar esses dados e carregar em uma base de dados central.


## Instalação

Siga estes passos para configurar o ambiente virtual e instalar as dependências:

1.  **Crie um ambiente virtual:**

    ```shell
    python -m venv .venv
    ```

2.  **Ative o ambiente virtual:**

    -   **No Windows:**

        ```shell
        .venv\\Scripts\\activate
        ```

    -   **No Linux/macOS:**

        ```shell
        source .venv/bin/activate
        ```

3.  **Instale as dependências:**

    ```shell
    pip install -r requirements.txt
    ```

## Configuração

1.  **Arquivo `config/config.ini`:**

    Este arquivo contém as configurações necessárias para o pipeline. Edite-o para configurar os diretórios de entrada e as credenciais do banco de dados.

    ```ini
    [directories]
    pdf_dir = data/pdfs
    spreadsheet_dir = data/spreadsheets

    [database]
    host = localhost
    port = 5432
    dbname = seu_banco_de_dados
    user = seu_usuario
    password = sua_senha
    table_name = sua_tabela
    ```

    Substitua os valores com as informações do seu ambiente.

2.  **Diretórios de Entrada:**

    Crie os diretórios `data/pdfs` e `data/spreadsheets` e adicione os arquivos de entrada (PDFs e planilhas) nesses diretórios.

## Execução

Para executar o pipeline ETL, execute o seguinte comando:

```shell

.venv/Scripts/activate
>> python src/main.py

Este comando irá:

Extrair os dados dos PDFs e planilhas nos diretórios configurados.
Transformar os dados extraídos.
Carregar os dados transformados na base de dados especificada.

Detalhes da Implementação
Extração de Dados de PDFs
A extração de dados de PDFs é feita utilizando a biblioteca PyPDF2 para ler o conteúdo dos arquivos PDF. A abordagem consiste em:

Listar os arquivos PDF: A função process_pdfs_from_dir lista todos os arquivos com extensão .pdf no diretório especificado.
Extrair o texto: Para cada arquivo PDF, a biblioteca PyPDF2 é utilizada para extrair o texto de cada página.
Retornar os dados: O texto extraído é retornado como uma lista de strings, onde cada string representa o conteúdo de um arquivo PDF.

Leitura e Tratamento de Dados de Planilhas
A leitura e tratamento de dados de planilhas é feita utilizando a biblioteca pandas para ler os arquivos Excel (xlsx). A abordagem consiste em:

Listar os arquivos de planilha: A função process_spreadsheets_from_dir lista todos os arquivos com extensão .xlsx no diretório especificado.
Ler os dados: Para cada arquivo de planilha, a biblioteca pandas é utilizada para ler os dados em um DataFrame.
Converter para dicionário: O DataFrame é convertido em uma lista de dicionários, onde cada dicionário representa uma linha da planilha.
Retornar os dados: A lista de dicionários é retornada.

Unificação, Validação e Transformação dos Dados

Unificação: Os dados extraídos dos PDFs e planilhas são combinados em uma única lista.

Transformação: A função transform_data realiza as seguintes etapas:

Extrai os nomes das colunas da primeira linha da planilha e remove o prefixo "Unnamed: ".
Transforma as linhas subsequentes em dicionários, utilizando os nomes das colunas extraídos.
Para as linhas onde o número de valores não corresponde ao número de colunas, os valores faltantes são preenchidos com None.



Carga dos Dados na Base de Dados
A carga dos dados na base de dados é feita utilizando a biblioteca psycopg2 para interagir com o PostgreSQL. A abordagem consiste em:

Conectar ao banco de dados: A classe DatabaseLoader utiliza as configurações do banco de dados (host, port, dbname, user, password) para estabelecer uma conexão com o banco de dados.
Criar a tabela: A função create_table cria uma tabela no banco de dados, caso ela não exista. Os nomes das colunas da tabela são extraídos dos dados transformados.
Inserir os dados: A função insert_data insere os dados transformados na tabela.

Estrutura do Projeto
├── config/
│   └── config.ini                  # Arquivo de configuração
├── data/
│   ├── pdfs/                       # Diretório para os arquivos PDF
│   └── spreadsheets/              # Diretório para os arquivos de planilha
├── src/
│   ├── extract/
│   │   ├── pdf_extractor.py        # Módulo para extrair dados de PDFs
│   │   └── spreadsheet_extractor.py # Módulo para extrair dados de planilhas
│   ├── load/
│   │   └── database_loader.py      # Módulo para carregar os dados no banco de dados
│   ├── transform/
│   │   ├── data_transformer.py     # Módulo para transformar os dados
│   │   └── data_validator.py       # Módulo para validar os dados
│   ├── main.py                     # Script principal para executar o pipeline ETL
│   └── utils/
│       └── logger.py               # Módulo para configurar o logging
├── .venv/                          # Ambiente virtual
├── requirements.txt                # Lista de dependências
└── README.md                       # Documentação do projeto


