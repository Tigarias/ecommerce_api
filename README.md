# 👁️ Eyes on Technology - Gestão de Inventário de Hardware

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-316192.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-6-DC382D.svg?style=flat&logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

## 📖 Visão Geral

O **Eyes on Technology** é um sistema corporativo de gestão de inventário desenvolvido para uma empresa fictícia especializada em hardware e componentes de computador de alto desempenho. A solução combina um backend robusto em **FastAPI** com um dashboard administrativo intuitivo em **Streamlit**, permitindo o controle total de estoque, categorias e análise financeira do inventário.

Este projeto demonstra a aplicação de tecnologias modernas para resolver problemas reais de negócio, focando em **performance (Redis)**, **escalabilidade (Docker)** e **qualidade de software (Pytest)**.

---

## 🚀 Funcionalidades de Negócio

*   **Dashboard de KPIs**: Visualização em tempo real do total de produtos, itens em estoque e valor total do inventário.
*   **Monitoramento de Estoque Avançado**: Nova área dedicada para monitorar a disponibilidade de itens, com filtros por status (Em Estoque, Estoque Crítico, Esgotado).
*   **Gestão de Ciclo de Vida**: Funcionalidades completas de **Criação, Leitura e Exclusão (CRUD)** para categorias e produtos diretamente pela interface visual.
*   **Alertas Inteligentes**: Sistema que destaca automaticamente componentes com menos de 5 unidades, facilitando a reposição e evitando rupturas de estoque.
*   **Busca e Filtros**: Ferramenta de pesquisa rápida para localizar componentes específicos no inventário.
*   **Cache de Alta Performance**: Uso de Redis para garantir que as consultas ao catálogo sejam instantâneas.

---

## 🏗️ Arquitetura do Sistema

O projeto adota uma estrutura modular seguindo os princípios de **Clean Architecture**:

*   **Backend (FastAPI)**: API RESTful assíncrona responsável pela lógica de negócio e persistência.
*   **Frontend (Streamlit)**: Interface visual 100% em Python para gestão administrativa, com formulários inteligentes e feedback visual.
*   **Banco de Dados (PostgreSQL)**: Armazenamento relacional seguro e íntegro com suporte a exclusões em cascata controladas.
*   **Cache (Redis)**: Camada de aceleração para consultas frequentes.
*   **Infraestrutura (Docker)**: Orquestração completa de serviços para fácil implantação.

---

## ⚙️ Como Executar o Projeto

### Pré-requisitos
*   [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/) instalados.

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/SEU_USUARIO/eyes-on-technology.git
    cd eyes-on-technology
    ```

2.  **Inicie os Serviços:**
    ```bash
    docker-compose up --build -d
    ```

3.  **Acesse as Interfaces:**
    *   **Dashboard Administrativo:** [http://localhost:8501](http://localhost:8501)
    *   **Documentação da API (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Qualidade e Testes

A robustez do sistema é garantida por testes automatizados com 100% de cobertura nas rotas críticas.

```bash
docker-compose exec app pytest --html=report.html --self-contained-html --cov=app app/tests/
```

---

## 👨‍💻 Autor

Desenvolvido por **[Seu Nome/Usuário]** como um projeto de portfólio profissional em Engenharia de Software.
