# 🛒 API de Microserviço para E-commerce com Dashboard

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-316192.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-6-DC382D.svg?style=flat&logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

## 📖 Visão Geral

Este projeto é uma **solução completa de e-commerce** que combina uma **API RESTful de alta performance** (FastAPI) com um **Dashboard Administrativo intuitivo** (Streamlit). A aplicação utiliza **PostgreSQL** para persistência de dados, **Redis** para cache de alta velocidade e é totalmente orquestrada via **Docker Compose**.

O diferencial deste projeto é a união de um backend robusto com uma interface visual moderna, permitindo que qualquer usuário gerencie o catálogo de produtos e categorias sem precisar de conhecimentos técnicos em terminal ou chamadas de API manuais.

---

## 🚀 Tecnologias e Ferramentas

A stack tecnológica foi escolhida para representar o padrão ouro do mercado atual para aplicações Python:

| Tecnologia | Função no Projeto |
| :--- | :--- |
| **FastAPI** | Framework web assíncrono para construção da API robusta e escalável. |
| **Streamlit** | Interface visual (Front-end) desenvolvida 100% em Python para gestão do catálogo. |
| **PostgreSQL** | Banco de dados relacional principal para armazenamento seguro de dados. |
| **Redis** | Camada de cache para otimizar o tempo de resposta em consultas de produtos. |
| **Docker & Compose** | Containerização completa, garantindo que o projeto rode em qualquer máquina. |
| **Pytest & Pytest-Cov** | Suíte de testes automatizados com relatórios visuais de cobertura. |

---

## 🏗️ Arquitetura e Estrutura de Diretórios

O projeto adota uma estrutura modular, separando claramente as responsabilidades:

```text
ecommerce_api/
├── app/                 # Backend (FastAPI)
│   ├── api/             # Endpoints da API
│   ├── crud/            # Lógica de negócio e acesso a dados
│   ├── db/              # Conexões com PostgreSQL e Redis
│   ├── models/          # Entidades do banco de dados
│   ├── schemas/         # Validação de dados (Pydantic)
│   ├── tests/           # Testes automatizados
│   └── main.py          # Ponto de entrada da API
├── dashboard/           # Front-end (Streamlit)
│   ├── app.py           # Código da interface visual
│   └── Dockerfile       # Receita de construção do dashboard
├── .env                 # Variáveis de ambiente
├── Dockerfile           # Receita de construção da API
├── docker-compose.yml   # Orquestração de todos os serviços
└── requirements.txt     # Dependências do projeto
```

---

## ⚙️ Como Executar o Projeto Localmente

### Pré-requisitos
*   [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/) instalados.

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/SEU_USUARIO/ecommerce_api.git
    cd ecommerce_api
    ```

2.  **Configure o arquivo `.env`:**
    ```env
    PROJECT_NAME=EcommerceAPI
    DATABASE_URL=postgresql://user:password@db:5432/ecommerce_db
    REDIS_URL=redis://redis:6379/0
    SECRET_KEY=sua_chave_secreta_aqui
    DEBUG=True
    ```

3.  **Inicie os Serviços:**
    ```bash
    docker-compose up --build -d
    ```

4.  **Acesse as Interfaces:**
    *   **Dashboard Administrativo (Streamlit):** [http://localhost:8501](http://localhost:8501)
    *   **Documentação da API (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Qualidade de Software e Testes

A qualidade do código é garantida por uma suíte de testes que cobre 100% das operações críticas.

### Executando os Testes e Gerando Relatórios

```bash
docker-compose exec app pytest --html=report.html --self-contained-html --cov=app app/tests/
```

---

## 👨‍💻 Autor

Desenvolvido por **[Tiago Luciano/Tigarias]** como parte de um portfólio profissional de Engenharia de Software.
