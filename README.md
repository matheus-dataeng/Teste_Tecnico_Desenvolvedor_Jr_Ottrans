# Teste Técnico Ottrans — Análise de Demanda de Passageiros

Projeto de ETL e análise de dados públicos de demanda do transporte coletivo. Os dados de janeiro e fevereiro de 2022 são processados com Python e pandas, armazenados no PostgreSQL e apresentados em um dashboard Streamlit. O Airflow organiza a execução do pipeline, e o Docker Compose reúne o ambiente local.

As seis análises apresentam demanda total, quantidade de linhas, média diária, evolução temporal, ranking das linhas com maior demanda e demanda de estudantes. O banco PostgreSQL já está hospedado no Neon, com os dois meses carregados.

| Acesso | Endereço ou situação |
| --- | --- |
| Apresentação do projeto | [Landing page no GitHub Pages](https://matheus-dataeng.github.io/Teste_Tecnico_Desenvolvedor_Jr_Ottrans/) |
| Dashboard local | <http://127.0.0.1:8501> |
| Airflow local | <http://127.0.0.1:8080> |
| Dashboard público | [Abrir dashboard no Streamlit](https://testetecnicodesenvolvedorjrottrans-ayckexyhjqnut4hwzaepar.streamlit.app/) |
| Banco remoto | PostgreSQL 16 no Neon, com as duas tabelas mensais carregadas. |
| Repositório | [GitHub — Teste Técnico Ottrans](https://github.com/matheus-dataeng/Teste_Tecnico_Desenvolvedor_Jr_Ottrans) |

## Arquitetura

```mermaid
flowchart LR
    A["Fonte pública"] -->|Download manual| B["CSVs de janeiro e fevereiro"]
    B --> C["Airflow: extração, testes, transformação e carga"]
    C --> D[(PostgreSQL local ou Neon)]
    D -->|Consultas SQL| E[Streamlit]
    E --> F["Indicadores, gráficos e dados detalhados"]
```

O ambiente local possui três serviços principais: PostgreSQL, Airflow e Streamlit. O serviço de testes é executado sob demanda.

O Streamlit consulta o PostgreSQL diretamente. A entrada do ETL utiliza os CSVs da fonte oficial armazenados em `data/`, conforme as instruções de preparação dos arquivos. A implantação remota utiliza o Neon para armazenar os dados e o Streamlit Community Cloud para o dashboard. A landing page é publicada no GitHub Pages.

### Fluxo do ETL

A DAG `Teste_Tecnico_Ottrans`, em [dags_airflow/dags.py](dags_airflow/dags.py), executa:

```text
extract → test_transform → transform → load
```

1. **extract:** lê os dois CSVs e retorna os DataFrames.
2. **test_transform:** executa os seis testes das funções de transformação com dados pequenos criados em memória.
3. **transform:** padroniza os nomes das colunas, remove duplicatas completas, trata textos, converte códigos numéricos e padroniza datas.
4. **load:** abre uma transação e carrega as duas tabelas no PostgreSQL. Quando a tabela já existe, seu conteúdo é substituído com `TRUNCATE` seguido de inserção em lotes de 5.000 registros.

Os DataFrames passam entre as tarefas por XCom. A conexão com o banco é criada na tarefa de carga e liberada ao final. Uma exceção na carga desfaz as operações da transação. A falha de uma tarefa interrompe as tarefas seguintes nessa sequência.

A execução é manual (`schedule=None`), com `catchup=False`. O Airflow funciona em modo `standalone`: seus metadados ficam em SQLite no volume `airflow_data`. Na configuração local, os dados de negócio ficam no PostgreSQL, no volume `postgres_data`; na configuração remota, a carga é direcionada ao Neon.

### Estrutura do banco

Cada arquivo mensal corresponde a uma tabela no schema `public`:

| Campo de janeiro — `demanda_janeiro_2022` | Campo de fevereiro — `demanda_fevereiro_2022` | Significado |
| --- | --- | --- |
| `data_movimento_jan` | `data_movimento_fev` | Data do registro |
| `codigo_linha_jan` | `codigo_linha_fev` | Código da linha de ônibus |
| `nome_linha_jan` | `nome_linha_fev` | Nome da linha |
| `tipo_passageiro_jan` | `tipo_passageiro_fev` | Código da categoria de passageiro |
| `nome_passageiro_jan` | `nome_passageiro_fev` | Descrição da categoria de passageiro |
| `demanda_jan` | `demanda_fev` | Volume de demanda informado no registro |

Um registro contém uma combinação de data, linha e categoria de passageiro. A demanda representa o volume registrado; não permite identificar pessoas únicas.

As páginas usam aliases SQL para receber nomes de colunas iguais nos resultados dos dois meses. Ao selecionar ambos os meses, os resultados são concatenados em memória. As tabelas mensais permanecem separadas no banco.

## Tecnologias e dependências

| Tecnologia | Uso |
| --- | --- |
| Python | ETL, testes e dashboard |
| pandas | Leitura e transformação dos dados |
| PostgreSQL | Persistência e consultas SQL |
| SQLAlchemy | Conexão, transações e carga |
| psycopg | Driver do PostgreSQL |
| python-dotenv | Leitura de variáveis de ambiente pelo código |
| Apache Airflow | Orquestração das tarefas |
| Streamlit | Interface e visualizações |
| pytest | Testes automatizados |
| Docker Compose | Execução dos serviços locais |

As dependências de cada imagem ficam em `docker/requirements.*.txt`. O Airflow utiliza as constraints oficiais da sua versão. `logging`, `os` e `pathlib` fazem parte da biblioteca padrão do Python.

O `requirements.txt` da raiz reúne dependências de desenvolvimento. A execução por Docker instala as dependências de cada serviço automaticamente; não exige instalar o Airflow no Windows.

## Organização do projeto

```text
.
├── .github/workflows/
│   └── github-pages.yml          # Publicação da landing page
├── consultas_analiticas/          # Consultas SQL dos indicadores
├── dags_airflow/
│   └── dags.py                   # DAG do pipeline
├── data/                         # CSVs locais, ignorados pelo Git
├── docker/                       # Dependências por serviço
├── landing_page/                 # Apresentação estática em HTML e CSS
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── utils/log_config.py
├── streamlit_app/
│   ├── Home.py
│   ├── assets/
│   ├── pages/
│   │   ├── 1_Demanda_por_Linha.py
│   │   └── 2_Dados_Detalhados.py
│   └── secrets.toml              # Configuração local, não versionada
├── tests/test_transform.py
├── Dockerfile.airflow
├── Dockerfile.streamlit
├── Dockerfile.tests
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
└── README.md
```

## Fonte e qualidade dos dados

A fonte indicada no desafio é o conjunto [Demanda, no Portal Brasileiro de Dados Abertos](https://dados.gov.br/dados/conjuntos-dados/demanda). Os recursos originais são publicados pela ETUFOR no [Fortaleza Dados Abertos](https://dados.fortaleza.ce.gov.br/dataset/demanda). O recorte utilizado contém os arquivos de janeiro e fevereiro de 2022.

Na implementação atual, os arquivos são baixados manualmente e colocados em `data/`. A extração usa separador `;` e codificação UTF-8.

### Problemas encontrados, tratamentos e impactos

A conferência dos dois arquivos locais identificou os seguintes problemas reais:

| Problema | Evidência na base | Tratamento implementado | Impacto |
| --- | --- | --- | --- |
| Ausência de cabeçalho em janeiro | Janeiro começa diretamente com dados; fevereiro possui cabeçalho. A leitura padrão de janeiro retorna 86.033 registros, enquanto a leitura correta retorna 86.034. | `extract.py` utiliza `header=None` e informa os seis nomes de colunas para janeiro. | Preserva o primeiro registro e sua demanda, evitando que ele seja interpretado como cabeçalho. Também permite acessar corretamente os campos na transformação. |
| Formatos de data diferentes entre os meses | Janeiro utiliza `AAAA-MM-DD`; fevereiro utiliza `DD/MM/AAAA`. Uma data como `01/02/2022` é ambígua sem um formato explícito. | `validate_dates` usa `%Y-%m-%d` para janeiro e `%d/%m/%Y` para fevereiro, com conversão para datas por `.dt.date`. | Evita trocar dia e mês, mantém os registros no período correto e permite agrupamento e ordenação temporal consistentes. |
| Espaços nas extremidades dos nomes de linhas | 61.987 registros de janeiro e 58.015 de fevereiro possuem espaços no início ou no fim de `NomeLinha`: 120.002 registros ao todo. | As validações de texto aplicam `.str.strip()` aos nomes das linhas. | Padroniza os nomes exibidos e evita diferenças artificiais em buscas, comparações e agrupamentos pelo nome da linha. O tratamento preserva os valores de demanda. |

Além desses tratamentos, o código possui regras preventivas:

- Remoção de registros completamente duplicados com `drop_duplicates`.
- Preenchimento de nomes nulos com `Dado não informado`.
- Conversão dos códigos de linha e categoria para números com `errors="coerce"`, registrando avisos quando aparecem nulos após a conversão.
- Conversão de datas inválidas para valores ausentes, com teste automatizado desse comportamento.
- Padronização da capitalização dos textos com `.str.title()`.

Na conferência dos arquivos utilizados, foram encontrados zero nulos nos seis campos, zero duplicatas completas e zero datas inválidas após a conversão com os formatos explícitos. Os testes exercitam essas situações com dados sintéticos. A capitalização dos textos segue a regra `.str.title()`.

### Valores de referência

Os arquivos conferidos apresentam estes totais:

| Período | Registros | Demanda total | Códigos de linha distintos | Dias com registros |
| --- | ---: | ---: | ---: | ---: |
| Janeiro/2022 | 86.034 | 12.495.749 | 333 | 31 |
| Fevereiro/2022 | 80.548 | 13.548.408 | 332 | 28 |
| Ambos | 166.582 | 26.044.157 | 341 | 59 |

A contagem de linhas em ambos os meses considera códigos distintos no conjunto combinado. Ela não é a soma das contagens mensais, pois vários códigos aparecem nos dois períodos.

## Instalação e execução local

### 1. Preparar o ambiente e os arquivos

Requisitos: Docker Desktop iniciado em modo de containers Linux, Docker Compose v2 e acesso à internet para baixar as imagens e dependências. Os comandos abaixo devem ser executados na raiz do repositório.

Baixe os recursos oficiais de [janeiro](https://dados.fortaleza.ce.gov.br/dataset/19d1d365-46b7-4434-9b8d-43ad8ab21a3b/resource/6e0b1c22-b9e1-4f18-aa1e-a3cb5e968ea1/download/demanda_202201.csv) e [fevereiro](https://dados.fortaleza.ce.gov.br/dataset/19d1d365-46b7-4434-9b8d-43ad8ab21a3b/resource/7372315d-55a8-4b3e-8036-84a5bc2a2df3/download/demanda_202202.csv) e salve-os com estes nomes:

```text
data/demanda_202201.csv
data/demanda_202202.csv
```

A pasta `data/` é ignorada pelo Git. Quem obtiver o repositório deve criá-la e fornecer os arquivos antes de iniciar o ETL.

### 2. Criar o arquivo `.env.docker`

Crie `.env.docker` na raiz com a configuração abaixo. A senha é um exemplo para substituir por um valor definido no seu ambiente; se o arquivo já existir, preserve sua configuração.

```dotenv
POSTGRES_DB=ottrans
POSTGRES_USER=ottrans
POSTGRES_PASSWORD=defina_uma_senha_local
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_HOST_PORT=5433
AIRFLOW_PORT=8080
STREAMLIT_PORT=8501
ARQUIVO_JANEIRO_2022=/app/data/demanda_202201.csv
ARQUIVO_FEVEREIRO_2022=/app/data/demanda_202202.csv
```

Os serviços leem as variáveis do arquivo por meio de `env_file: .env.docker`. O argumento `--env-file .env.docker` também permite ao Compose usar os valores na configuração das portas publicadas. Na execução local, use `POSTGRES_HOST=postgres`, nome do serviço na rede interna, e `POSTGRES_PORT=5432`. `POSTGRES_HOST_PORT=5433` é a porta publicada para ferramentas no Windows. Os caminhos dos CSVs ficam em `/app/data/`.

| Origem da conexão | Host | Porta padrão |
| --- | --- | --- |
| Ferramenta no Windows | `127.0.0.1` | `5433` |
| Airflow e Streamlit dentro do Compose | `postgres` | `5432` |

As variáveis de inicialização do PostgreSQL criam banco e usuário quando o volume é inicializado pela primeira vez. Alterar o arquivo depois não modifica automaticamente um banco, usuário ou senha já gravados no volume.

### 3. Configurar a conexão do Streamlit

Crie o arquivo local `streamlit_app/secrets.toml`:

```toml
[connections.postgresql]
dialect = "postgresql"
driver = "psycopg"
host = "postgres"
port = "5432"
database = "ottrans"
username = "ottrans"
password = "defina_uma_senha_local"
```

Use o mesmo banco, usuário e senha definidos no seu `.env.docker`. O host e a porta acima são os da rede interna do Compose. As páginas acessam essa seção usando `st.connection("postgresql", type="sql")`.

O Compose monta esse arquivo em `/app/.streamlit/secrets.toml`. `.env.docker` e `secrets.toml` são ignorados pelo Git e pelo contexto de build das imagens. Configure-os localmente antes de iniciar os serviços.

### 4. Iniciar PostgreSQL e Airflow

```powershell
docker compose --env-file .env.docker config --quiet
docker compose --env-file .env.docker up --build -d postgres airflow
docker compose --env-file .env.docker ps
```

A primeira construção pode demorar devido ao download das imagens e das bibliotecas. Aguarde os serviços ficarem saudáveis antes de disparar a DAG.

Abra <http://127.0.0.1:8080>. O usuário local é `admin`; a senha configurada no ambiente pode ser consultada no arquivo local do Airflow:

```powershell
docker compose --env-file .env.docker exec airflow cat /opt/airflow/simple_auth_manager_passwords.json.generated
```

Na interface, localize `Teste_Tecnico_Ottrans`, habilite a DAG e dispare uma execução manual. Acompanhe as tarefas `extract`, `test_transform`, `transform` e `load` até a conclusão. A carga cria as tabelas quando ainda não existem.

### 5. Iniciar o dashboard

Depois de concluir a primeira carga:

```powershell
docker compose --env-file .env.docker --profile apps up --build -d streamlit
docker compose --env-file .env.docker --profile apps ps
```

Acesse <http://127.0.0.1:8501>. Os endereços usam as portas padrão; se personalizar as portas no `.env.docker`, ajuste as URLs.

O código e os CSVs são montados como somente leitura nos containers. Mudanças nos arquivos Python aparecem no ambiente sem reconstruir as imagens; alterações de dependências ou Dockerfiles exigem novo build. As consultas do dashboard ficam em cache por dez minutos, portanto uma nova carga pode não aparecer imediatamente na tela.

### Logs e encerramento

```powershell
docker compose --env-file .env.docker logs --tail 100 airflow
docker compose --env-file .env.docker --profile apps logs --tail 100 streamlit
docker compose --env-file .env.docker --profile apps stop
```

Os logs de cada tarefa também ficam disponíveis na interface do Airflow. `stop` preserva os volumes e os dados para a próxima execução.

## Dashboard

- **Home:** apresenta o projeto, o período e a fonte dos dados. A fotografia ilustrativa da frota OT Trans possui o crédito de origem na página.
- **Análise da demanda:** oferece filtro de janeiro, fevereiro ou ambos, três indicadores e dois gráficos.
- **Dados detalhados:** apresenta os seis campos dos registros, filtros de mês e código da linha, contagem de registros e datas no formato `DD/MM/AAAA`.

| Indicador ou visualização | Cálculo |
| --- | --- |
| Demanda total | Soma da demanda no período selecionado |
| Linhas com registros | Quantidade de códigos de linha distintos |
| Média diária de demanda | Demanda total dividida pelas datas distintas com registros; valor exibido arredondado |
| Evolução diária | Soma da demanda de todas as linhas por data |
| Ranking das dez linhas | Soma da demanda por código de linha, em ordem decrescente |

## Consultas SQL analíticas

Os seis arquivos abaixo organizam as análises SQL, com consultas separadas para janeiro e fevereiro. As consultas utilizam agregações, agrupamentos, ordenação temporal e filtro por tipo de passageiro.

| Arquivo | Análise |
| --- | --- |
| [01_demanda_total.sql](consultas_analiticas/01_demanda_total.sql) | Demanda total por período |
| [02_quantidade_linhas.sql](consultas_analiticas/02_quantidade_linhas.sql) | Quantidade de nomes de linha distintos |
| [03_media_diaria_demanda.sql](consultas_analiticas/03_media_diaria_demanda.sql) | Média diária da demanda |
| [04_demanda_por_dia.sql](consultas_analiticas/04_demanda_por_dia.sql) | Evolução temporal da demanda |
| [05_ranking_linhas.sql](consultas_analiticas/05_ranking_linhas.sql) | Ranking de demanda por linha |
| [06_demanda_por_categoria_linha.sql](consultas_analiticas/06_demanda_por_categoria_linha.sql) | Demanda de estudantes, com filtro pelo tipo de passageiro 3 |

Execute os arquivos em um editor SQL conectado ao banco de destino. Para o PostgreSQL local, use `127.0.0.1:5433`; para o Neon, use o host remoto, a porta `5432` e a conexão SSL fornecida pelo serviço. Os valores de referência e os indicadores do dashboard permitem conferir os resultados.

## Testes automatizados

Os seis testes de [tests/test_transform.py](tests/test_transform.py) utilizam DataFrames sintéticos e verificam:

1. Remoção de duplicatas nos dois meses.
2. Limpeza dos textos e conversão dos códigos de janeiro.
3. Limpeza dos textos e conversão dos códigos de fevereiro.
4. Conversão correta dos dois formatos de data.
5. Conversão de datas inválidas para valores ausentes.
6. Erro quando falta uma coluna obrigatória no renomeamento.

Para executar pelo pytest em um container independente:

```powershell
docker compose --env-file .env.docker --profile tests run --rm --build --no-deps -T tests
```

O serviço de testes utiliza os dados sintéticos definidos no arquivo e pode ser executado independentemente do banco, do Airflow e dos CSVs reais. Na DAG, as mesmas funções são chamadas pela tarefa `test_transform`. Para visualizar o relatório completo do pytest, utilize o comando acima.

## Principais decisões técnicas

- **pandas para os dois arquivos:** os CSVs somam aproximadamente 13 MB, permitindo uma implementação simples em memória para este recorte.
- **PostgreSQL:** oferece persistência, transações e consultas relacionais para os indicadores, além de permitir compartilhar a base com o dashboard.
- **Neon:** disponibiliza o PostgreSQL remoto para que o dashboard publicado possa consultar os dados sem depender do computador de desenvolvimento.
- **Uma tabela por mês:** mantém a correspondência entre arquivo de origem e tabela, facilitando a identificação do período de cada conjunto de registros.
- **Substituição completa na carga:** reaplicar os mesmos arquivos substitui o conteúdo anterior, evitando acumular registros de execuções passadas. A abordagem atende ao recorte fixo; não implementa carga incremental.
- **Funções separadas por etapa:** extração, transformação e carga podem ser compreendidas e revisadas individualmente.
- **Docker Compose:** reúne os serviços e evita depender de um PostgreSQL instalado no Windows. As imagens possuem dependências separadas por responsabilidade.
- **Airflow com execução manual:** permite acompanhar a sequência e os logs das tarefas durante o desenvolvimento.
- **Streamlit com acesso direto ao banco:** simplifica a apresentação dos dados para este único consumidor.

## Limitações do projeto

- **Recorte temporal:** a implementação contempla janeiro e fevereiro de 2022. Novos períodos exigem a inclusão dos arquivos, tabelas e consultas correspondentes.
- **Processamento em memória:** os CSVs e os resultados detalhados são carregados integralmente. Os DataFrames também passam por XCom. Volumes maiores exigem rever a leitura em lotes e o transporte entre tarefas.
- **Carga completa:** cada execução substitui os dados das tabelas mensais. O processo trabalha com a recarga integral dos arquivos.
- **Conversões inválidas:** datas e códigos que não podem ser convertidos permanecem como valores ausentes, com avisos nos logs.
- **Ambiente local:** o Airflow utiliza `standalone`, metadados SQLite e acionamento manual da DAG, conforme o escopo de desenvolvimento deste projeto.

## Publicação

### Banco de dados no Neon

O PostgreSQL 16 está hospedado no Neon, com as tabelas `public.demanda_janeiro_2022` e `public.demanda_fevereiro_2022`. A carga foi conferida com os totais de referência: 86.034 registros de janeiro e 80.548 de fevereiro, preservando as colunas de data como `DATE`.

Para direcionar o ETL ao Neon, configure no `.env.docker` o host, banco, usuário e senha fornecidos pelo serviço. Use `POSTGRES_PORT=5432`, `PGSSLMODE=require` e `PGCHANNELBINDING=require`. Depois aplique as variáveis somente ao Airflow:

```powershell
docker compose --env-file .env.docker up -d --no-deps --force-recreate airflow
```

Dispare a DAG pela interface para executar a carga. O serviço PostgreSQL local usa os mesmos nomes de variáveis na inicialização; configure-o com suas credenciais locais ao iniciar esse ambiente.

### Landing page no GitHub Pages

A apresentação estática utiliza os arquivos de `landing_page/`. O workflow [.github/workflows/github-pages.yml](.github/workflows/github-pages.yml) publica essa pasta quando ela é alterada na branch `main`, ou quando o workflow é executado manualmente. HTML, CSS, imagem e fonte são servidos pelo GitHub Pages.

Os botões de acesso ao dashboard abrem a aplicação publicada no Streamlit Community Cloud.

### Dashboard no Streamlit Community Cloud

O [dashboard público](https://testetecnicodesenvolvedorjrottrans-ayckexyhjqnut4hwzaepar.streamlit.app/) está publicado no Streamlit Community Cloud e conectado ao PostgreSQL do Neon. Foram conferidas as três páginas, os indicadores e os dois gráficos nos três períodos, além dos filtros de mês e código da linha nos dados detalhados. Os resultados foram comparados com os valores de referência do banco.

Para reproduzir a publicação do dashboard:

1. Conferir as dependências utilizadas pelo dashboard no repositório publicado.
2. Criar a aplicação no Community Cloud, selecionando o repositório, a branch `main` e `streamlit_app/Home.py` como arquivo de entrada, com Python 3.12.
3. Nas configurações de Secrets, cadastrar a seção `[connections.postgresql]` com host, porta e credenciais reais do Neon e os parâmetros SSL. O host interno `postgres` serve apenas para o Compose local. O arquivo de segredos não deve ser enviado ao repositório.
4. Testar o acesso público, as três páginas, os filtros e os totais, comparando os resultados com os valores de referência deste README.

Modelo para os Secrets do Community Cloud, substituindo os valores indicados:

```toml
[connections.postgresql]
dialect = "postgresql"
driver = "psycopg"
host = "SEU_HOST_DO_NEON"
port = "5432"
database = "neondb"
username = "neondb_owner"
password = "SUA_SENHA_DO_NEON"

[connections.postgresql.query]
sslmode = "require"
channel_binding = "require"
```

O Community Cloud utiliza os arquivos de dependências do repositório; ele não inicia os serviços de `docker-compose.yml`. A orientação de configuração está na [documentação de deploy](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app), com detalhes sobre [dependências](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies) e [Secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management).

## Referências

- [Fonte de dados indicada no desafio](https://dados.gov.br/dados/conjuntos-dados/demanda)
- [Código de extração](src/extract.py), [transformação](src/transform.py) e [carga](src/load.py)
- [Configuração dos serviços](docker-compose.yml)
- [Crédito da fotografia ilustrativa da OT Trans](https://ottrans.com.br/nova-frota-de-onibus-da-ot-trans-amplia-renovacao-do-transporte-publico-de-salvador/)
