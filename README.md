\# Sistema de Detecção de Fraudes com Apache Kafka



\## Descrição

Projeto acadêmico de processamento de transações financeiras utilizando Apache Kafka, Python e SQLite. O sistema recebe transações, analisa possíveis fraudes e armazena os registros em um banco de dados.



\## Tecnologias

\- Python

\- Apache Kafka

\- Docker

\- SQLite

\- unittest



\## Regras de detecção

\- \*\*ALTO\_VALOR:\*\* transações com valor igual ou superior a R$ 10.000.

\- \*\*TEMPO\_60s:\*\* quatro ou mais transações do mesmo cliente em menos de 60 segundos.

\- \*\*GEO\_10m:\*\* transações do mesmo cliente em cidades diferentes dentro de 10 minutos.



\## Execução

1\. Inicie o Kafka com Docker Desktop e o arquivo `docker-compose.yml`.

2\. Execute o consumidor em um terminal:



&#x20;  `py src/consumer.py`



3\. Execute o produtor em outro terminal:



&#x20;  `py src/producer.py`



O produtor gera transações simuladas a cada três segundos.



\## Testes

Execute:



`py -m unittest discover -s tests -v`



\## Banco de dados

As transações são armazenadas localmente em `transacoes.db`, que não é enviado ao Git.



\## Observação

Projeto desenvolvido para fins acadêmicos.



