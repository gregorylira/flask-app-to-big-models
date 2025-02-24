# Projeto de Mensageria com RabbitMQ

Este projeto demonstra uma arquitetura de microserviços para processamento assíncrono de textos utilizando Flask, RabbitMQ e Docker. Originalmente, o sistema utilizava Redis (com RQ) para o enfileiramento de tarefas, mas foi migrado para RabbitMQ para oferecer uma solução de mensageria mais robusta e escalável.

---

## Sumário

- [Visão Geral](#vis%C3%A3o-geral)
- [Arquitetura](#arquitetura)
- [Requisitos](#requisitos)
- [Como Executar](#como-executar)
- [Endpoints da API](#endpoints-da-api)
- [Frontend Demo](#frontend-demo)
- [Observações](#observa%C3%A7%C3%B5es)

---

## Visão Geral

O projeto consiste em:

- **Web (API Flask):** Fornece endpoints para envio de requisições (`/predict`) e consulta de resultados (`/result/<job_id>`).
- **Worker:** Um serviço que consome mensagens do RabbitMQ, processa os textos utilizando um modelo de geração (via HuggingFace Transformers) e atualiza o status no banco de dados.
- **RabbitMQ:** Broker de mensagens que substitui o Redis utilizado anteriormente.
- **Nginx:** Atua como proxy reverso e servidor de arquivos estáticos (para o frontend demo).
- **Job Store (SQLite):** Armazena os jobs e seus status, compartilhado entre os containers.

---

## Arquitetura

1. **Envio de Tarefas (/predict):**

   - O endpoint gera um ID único para o job, registra o job em um banco de dados SQLite e publica uma mensagem na fila `task_queue` do RabbitMQ.

2. **Processamento Assíncrono (Worker):**

   - O worker consome as mensagens da fila, processa o texto utilizando a função `process_text` (baseada em HuggingFace Transformers) e atualiza o job no banco de dados com o resultado.

3. **Consulta de Resultados (/result/<job_id>):**

   - O endpoint consulta o status do job e retorna o resultado quando o processamento estiver concluído.

4. **Frontend Demo:**
   - Um simples HTML com JavaScript que envia o texto para o endpoint `/predict` e realiza _polling_ no endpoint `/result` para exibir o resultado.

---

## Requisitos

- Docker e Docker Compose

---

## Como Executar

1. **Clonar o repositório:**

   ```bash
   git clone https://github.com/gregorylira/flask-app-to-big-models
   cd flask-app-to-big-models
   ```

2. **Configurar as Variáveis de Ambiente:**

   Crie um arquivo `.env` na raiz do projeto com, por exemplo:

   ```dotenv
    REDIS_URL='redis://redis:6379/0'
    HUGGINGFACE_API_KEY='hf_*****'
    RABBITMQ_HOST="rabbitmq"
   ```

3. **Construir e Iniciar os Containers:**

   Execute o comando:

   ```bash
   docker-compose up --build
   ```

   Isso iniciará os serviços: **web**, **worker**, **rabbitmq** e **nginx**.

4. **Acessar a Aplicação:**

   - **API:** Através do Nginx (proxy reverso), a API estará disponível em `http://localhost/api`.
   - **Frontend Demo:** Acesse `http://localhost/` para visualizar a interface demo.
   - **RabbitMQ Management:** Acesse `http://localhost:15672` (usuário/senha padrão: `guest`/`guest`).

---

## Endpoints da API

- **GET /**  
  Retorna "Hello, World!" (endpoint de teste).

- **POST /api/predict**  
  Envia um JSON com o campo `text`. Exemplo de payload:

  ```json
  { "text": "Olá, você pode me ajudar?" }
  ```

  Retorna um JSON com o `job_id` do processamento.

- **GET /api/result/<job_id>**  
  Consulta o status do job. Se o processamento estiver concluído, retorna o resultado no formato:

  ```json
  {
    "result": {
      "content": "<texto gerado>",
      "role": "assistant",
      "tool_calls": null
    }
  }
  ```

---

## Frontend Demo

O frontend está implementado como um arquivo HTML simples (em `demo-frontend/index.html`). Ele envia a requisição para o endpoint `/api/predict` e realiza _polling_ para o endpoint `/api/result/<job_id>` a cada 2 segundos, exibindo o status e, posteriormente, o resultado.

---

## Observações

- **Transição de Redis para RabbitMQ:**  
  Inicialmente, o sistema utilizava Redis com RQ para o gerenciamento de filas e processamento assíncrono. Porém, a migração para RabbitMQ permitiu uma mensageria mais robusta, com melhor controle e opções avançadas de roteamento e persistência.

- **Compartilhamento do Banco de Dados:**  
  Para que o status dos jobs seja atualizado corretamente e acessível pelo endpoint `/result`, o arquivo SQLite (`jobs.db`) é compartilhado entre os containers **web** e **worker** via volumes no Docker Compose.

- **Logs e Verbosidade:**  
  Avisos do HuggingFace Transformers (como o `pad_token_id`) podem aparecer nos logs. Caso deseje reduzir a verbosidade, ajuste a configuração de log conforme a documentação da biblioteca.

---

Este projeto é uma base para a criação de sistemas de mensageria escaláveis, desacoplando o processamento pesado do fluxo principal da aplicação. Se houver dúvidas ou sugestões, sinta-se à vontade para abrir issues ou contribuir com pull requests.
