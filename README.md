# QueryMind AI

**An AI-powered conversational analytics platform for e-commerce data.**

QueryMind AI allows users to interact with structured e-commerce data using natural language. Instead of manually writing SQL queries, users can ask questions in plain English and receive data-driven answers, tables, and visualizations.

## Problem Statement

Traditional data analysis often requires knowledge of SQL, database structures, and visualization tools. This creates a barrier for users who need insights but lack technical expertise.

QueryMind AI aims to simplify this process by connecting natural language questions with database queries and meaningful analytical outputs.

## Proposed Solution

The platform will:

1. Accept natural language questions from users.
2. Interpret the analytical intent.
3. Generate SQL queries.
4. Validate queries before execution.
5. Retrieve results from PostgreSQL.
6. Present results through tables and interactive charts.
7. Generate explanations grounded in the returned data.

## Technology Stack

| Component             | Technology                            |
| --------------------- | ------------------------------------- |
| Frontend              | Streamlit                             |
| Backend API           | FastAPI                               |
| Programming Language  | Python                                |
| Database              | PostgreSQL                            |
| AI Integration        | Provider-independent LLM architecture |
| SQL Validation        | SQLGlot                               |
| Database Connectivity | SQLAlchemy, psycopg                   |
| Data Processing       | Pandas                                |
| Visualization         | Plotly                                |
| Testing               | Pytest                                |
| Version Control       | Git and GitHub                        |

## Dataset

**Brazilian E-Commerce Public Dataset by Olist**

Source: [Kaggle – Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

The dataset contains information about orders, customers, products, sellers, payments, reviews, and deliveries.

It will be used to build and evaluate conversational analytics workflows.

## Core Features (Planned)

* Natural language to SQL generation
* SQL validation and safe query execution
* Conversational analytics
* Interactive charts and tables
* Data-grounded explanations
* Query history
* SQL inspection
* Error handling and query feedback

## Architecture

QueryMind AI will follow a modular monolith architecture, separating frontend, API, business logic, database access, and AI services while keeping development and deployment manageable.

## Development Status

**Phase 1: Environment and Project Setup**

* [x] Python environment setup
* [x] Project directory structure
* [x] Git ignore configuration
* [ ] Database setup
* [ ] Dataset inspection and preparation

Further development will proceed incrementally, with emphasis on correctness, reliability, maintainability, and reproducibility.

## Future Goals

* Improve SQL generation accuracy
* Evaluate AI responses against verified analytical results
* Add robust query safety controls
* Deploy the application
* Document architecture and evaluation results
