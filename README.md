# 🚀 SenAI CRM – AI-Powered Customer Support Automation Platform

> **An enterprise-grade AI-powered CRM platform that automates customer support email processing using Retrieval-Augmented Generation (RAG), Google Gemini, enterprise knowledge retrieval, intelligent rule-based reasoning, CRM context enrichment, and Human-in-the-Loop approval workflows.**

---

# 📑 Table of Contents

* Overview
* Features
* Project Highlights
* System Architecture
* Technology Stack & Architecture Decisions
* Project Structure
* AI Agent & RAG Workflow
* Email Processing Lifecycle
* Frontend Workflow
* Setup Guide
* Environment Variables
* Database, Alembic & Schema
* Knowledge Base
* API Documentation
* Performance, Trade-offs & Security
* Scalability Strategy
* Assessment Coverage
* Known Limitations & Future Enhancements
* Repository Deliverables
* License

---

# 📌 Overview

SenAI CRM is an intelligent customer support automation platform designed to reduce manual effort while maintaining enterprise-grade reliability, transparency, and compliance.

The system automatically ingests incoming customer emails, reconstructs conversation threads, enriches customer context, retrieves relevant organizational knowledge using Retrieval-Augmented Generation (RAG), classifies customer intent, generates policy-aware response drafts, recommends execution plans, estimates confidence, and escalates critical cases for human review.

Instead of relying solely on a Large Language Model, SenAI combines deterministic business rules with AI reasoning and knowledge retrieval, ensuring responses remain accurate, explainable, and grounded in company policies.

The platform follows a modular layered architecture that separates presentation, business logic, persistence, AI services, and knowledge retrieval, making the system scalable and maintainable.

---

# ✨ Features

## AI Features

* 🤖 AI-powered Email Classification
* 📝 AI-generated Response Drafts
* 📄 Executive Thread Summaries
* 🎯 Confidence Scoring
* 🧠 Explainable Reasoning Trace
* ⚙️ Execution Plan Generation
* 🚨 Escalation Recommendation
* 👨 Human-in-the-Loop Approval
* 🔒 Dry-Run Agent Execution

## RAG Features

* 📚 Retrieval-Augmented Generation
* 🔍 Semantic Knowledge Search
* 📄 Enterprise Policy Citation
* 🧩 Intelligent Document Chunking
* 🧠 Local MiniLM Embeddings
* 🗄️ ChromaDB Vector Storage
* 📖 Knowledge Explorer
* 🔬 RAG Debug View

## CRM Features

* 👤 Customer Profile Enrichment
* 💬 Thread Reconstruction
* 📈 Churn Prediction
* ⭐ VIP Customer Detection
* 📊 Customer Health Monitoring
* 📅 Renewal Tracking

## Analytics Features

* 📊 Dashboard Analytics
* 📈 Category Distribution
* 😊 Sentiment Distribution
* 🚨 Escalation Metrics
* 📬 Email Volume Analytics
* 🤖 AI Confidence Metrics
* 👥 Human Intervention Metrics
* 📚 Knowledge Retrieval Metrics

## Engineering Features

* ⚡ FastAPI Backend
* 🛢️ PostgreSQL Database
* 🔄 Alembic Migrations
* 🧩 SQLAlchemy ORM
* 📜 OpenAPI Specification
* 📝 Audit Logging
* 🏛️ Layered Architecture
* 🔧 Dependency Injection

---

# ⭐ Project Highlights

* Hybrid Rule Engine + LLM Architecture
* Explainable AI Decisions
* Enterprise Knowledge Retrieval
* Human-in-the-Loop Governance
* Policy-Cited Responses
* CRM Context Awareness
* Audit Trail Generation
* Version-Controlled Database Schema
* Modular Service Architecture
* Production-Oriented Design

---

# 🏗️ System Architecture

The system follows a layered architecture: presentation, API, business/service, repository, ORM, and database layers, with dedicated AI and knowledge-retrieval subsystems.

```text
┌──────────────────────────────────────────────────────────────┐
│                      React Frontend                          │
│  Dashboard │ Inbox │ Thread Workspace │ AI Analysis │        │
│  Customers │ Knowledge Explorer │ Analytics │ Settings       │
└───────────────────────────┬──────────────────────────────────┘
                             │ REST API (Axios → OpenAPI)
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                      FastAPI Backend (API Layer)             │
└───────────────────────────┬──────────────────────────────────┘
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                     Service Layer                            │
│   AI │ Email │ Customer │ Analytics │ Knowledge │ Agent      │
└─────────────┬─────────────────────────────┬──────────────────┘
              ▼                             ▼
┌───────────────────────────┐   ┌───────────────────────────────┐
│ Repository Layer          │   │ Gemini Provider               │
│ (SQLAlchemy 2.x ORM)      │   └──────────────┬────────────────┘
└─────────────┬─────────────┘                  ▼
              ▼                      ┌───────────────────────────┐
┌───────────────────────────┐        │ RAG Retrieval             │
│ PostgreSQL Database       │        └──────────────┬────────────┘
│ (Alembic-managed schema)  │                       ▼
└───────────────────────────┘          ┌──────────────────────────┐
                                       │ ChromaDB Vector Store    │
                                       └──────────────────────────┘
```

This separation of concerns minimizes coupling, improves testability, and enables future extension without impacting unrelated modules.

---

# 🛠️ Technology Stack & Architecture Decisions

| Layer           | Technology                            | Why it was chosen                                                                  |
| --------------- | ------------------------------------- | ---------------------------------------------------------------------------------- |
| Frontend        | React 19 + Vite                       | Fast dev experience, modular components, optimized production builds               |
| Styling         | TailwindCSS                           | Rapid, consistent UI styling                                                       |
| Routing         | React Router                          | Standard client-side routing                                                       |
| HTTP Client     | Axios                                 | Simple, consistent REST integration                                                |
| Charts          | Recharts                              | Analytics dashboard visualizations                                                 |
| Backend         | FastAPI                               | High-performance async framework with automatic OpenAPI generation & DI            |
| ORM             | SQLAlchemy 2.x                        | Type-safe ORM with clean repository abstraction                                    |
| Validation      | Pydantic                              | Request/response schema validation                                                 |
| Database        | PostgreSQL 16                         | ACID-compliant relational database suitable for transactional CRM workloads        |
| Migrations      | Alembic                               | Version-controlled, reproducible schema migrations                                 |
| Vector Store    | ChromaDB                              | Lightweight local vector database for semantic retrieval without external services |
| Embedding Model | sentence-transformers/all-MiniLM-L6-v2| Local embedding generation — eliminates API costs and improves privacy             |
| LLM Provider    | Google Gemini (swappable provider)    | Future extensibility via provider abstraction                                      |
| Configuration   | python-dotenv                         | Environment-based secret management                                                |
| AI Pattern      | Custom Workflow Agent (ReAct-inspired)| Controlled reasoning with human approval rather than autonomous execution          |

Additional architectural choices:

| Decision               | Rationale                                                                                |
| ---------------------- | ---------------------------------------------------------------------------------------- |
| **Repository Pattern** | Decouples persistence logic from business services                                       |
| **Service Layer**      | Separates business logic from API endpoints for maintainability                          |
| **Human-in-the-Loop**  | Prevents unsafe autonomous actions in legal, compliance, or security-sensitive scenarios |
| **Hybrid Rule + LLM**  | Combines deterministic rules with AI reasoning for improved reliability                  |

---

# 📂 Project Structure

```text
SenAI-CRM/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── ingest_knowledge.py
│   ├── init_db.py
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── pages/
│       ├── components/
│       ├── services/
│       └── assets/
├── knowledge_base/
│   ├── api_docs.md
│   ├── compliance.md
│   ├── compliance_faq.md
│   ├── escalation.md
│   ├── escalation_matrix.md
│   ├── faq.md
│   ├── pricing_policy.md
│   ├── refund_policy.md
│   └── sla_policy.md
├── data/
│   ├── customer_support_dataset.csv
│   └── supporting_crm_data.json
├── docs/
│   ├── architecture_diagram.png
│   ├── er_diagram.png
│   ├── openapi.json
│   └── swagger.yaml
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── tests/
├── alembic.ini
├── requirements-lock.txt
└── README.md
```

---

# 🤖 AI Agent & RAG Workflow

The AI subsystem is implemented as a **custom workflow agent inspired by ReAct principles**. Rather than autonomously executing actions, the agent performs controlled reasoning — combining rule-based logic, CRM context, and RAG-retrieved knowledge — and recommends actions for human approval. It operates in **Dry-Run Mode**, meaning it never autonomously executes customer-facing operations.

```text
┌─────────────────────────────────────────────────────────────────┐
│                       Incoming Email                            │
└───────┬─────────────────────┬─────────────────────┬─────────────┘
        ▼                     ▼                     ▼
┌────────────────┐     ┌────────────────┐     ┌────────────────────┐
│ Rule Engine    │     │ CRM Context    │     │ Thread History     │
└───────┬────────┘     └───────┬────────┘     └─────────┬──────────┘
        └─────────────────────┬┴──────────────────────┘
                               ▼
                  ┌──────────────────────────────┐
                  │ RAG Knowledge Retrieval      │
                  │  (chunking → MiniLM →        │
                  │   ChromaDB → top-K context)  │
                  └──────────────┬───────────────┘
                                  ▼
                  ┌───────────────────────────────┐
                  │ Prompt Builder                │
                  └──────────────┬────────────────┘
                                  ▼
                  ┌───────────────────────────────┐
                  │ Gemini Provider               │
                  └──────────────┬────────────────┘
                                  ▼
                  ┌────────────────────────────────┐
                  │ AI Agent Service               │
                  │ (Thought → Action →            │
                  │  Observation → Decision)       │
                  └──────────────┬─────────────────┘
                                  ▼
        ┌─────────────────────────┼─────────────────────────────┐
        ▼                         ▼                             ▼
┌──────────────────────┐   ┌─────────────────────┐       ┌─────────────────────┐
│ Classification       │   │ Policy-Cited Reply  │       │ Execution Plan      │
│                      │   │ Draft               │       │ + Escalation Plan   │
└──────────┬───────────┘   └──────────┬──────────┘       └───────────┬─────────┘
           └────────────────────────┬┴──────────────────────────────┘
                                     ▼
                       ┌───────────────────────────────┐
                       │ Confidence Score +            │
                       │ Reasoning Trace               │
                       └───────────────────────────────┘
```

---

# 📧 Email Processing Lifecycle

The platform supports replaying historical email datasets (from `data/`) to simulate a real production support inbox, enabling deterministic testing of AI reasoning, escalation logic, analytics, and knowledge retrieval.

```bash
python replay_dataset.py
```

or via API:

```text
POST /api/emails/replay
```

End-to-end flow from ingestion through to the dashboard:

```text
┌────────────────────────┐
│ Incoming Email Payload │
└──────────┬─────────────┘
           ▼
┌────────────────────────┐
│ Payload Validation     │
└──────────┬─────────────┘
           ▼
┌────────────────────────┐
│ Duplicate Detection    │
└──────────┬─────────────┘
           ▼
┌────────────────────────┐
│ Thread Reconstruction  │
└──────────┬─────────────┘
           ▼
┌───────────────────────────────────────────────────┐
│ CRM Enrichment │ Rule Engine │ Thread History     │
└──────────────────────┬────────────────────────────┘
                       ▼
┌─────────────────────────┐
│ AI Agent & RAG Pipeline │   (see above)
└──────────┬──────────────┘
           ▼
┌────────────────────────┐
│ Human-in-the-Loop      │
│ Approval               │
└──────────┬─────────────┘
           ▼
┌────────────────────────┐
│ Database Persistence   │
│ + Audit Logging        │
└──────────┬─────────────┘
           ▼
┌────────────────────────┐
│ Dashboard & Analytics  │
└────────────────────────┘
```

---

# 🌐 Frontend Workflow

```text
┌──────────────────────────────────────────────────────────────┐
│                     React Frontend                           │
└───┬─────────┬───────────────┬────────────┬──────────┬────────┘
    ▼         ▼               ▼            ▼          ▼
┌─────────┐ ┌────────┐ ┌───────────────────┐ ┌─────────┐ ┌──────────┐
│Dashboard│ │ Inbox  │ │ Thread Workspace  │ │Customers│ │Analytics │
└─────────┘ └────────┘ └───────────────────┘ └─────────┘ └──────────┘
    └─────────┴───────────────┴────────────┴──────────┘
                              ▼
                  ┌───────────────────────────┐
                  │ Axios HTTP Client         │
                  └──────────────┬────────────┘
                                  ▼
                  ┌────────────────────────────┐
                  │ FastAPI Backend            │
                  └────────────────────────────┘
```

---

# ⚙️ Setup Guide

## Clone the Repository

```bash
git clone <repository-url>
cd SenAI-CRM
```

## Backend Setup

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Start Backend

```bash
cd backend
python run.py
```

| Endpoint              | URL                                      |
| --------------------- | ---------------------------------------- |
| Backend server        | `http://127.0.0.1:8000`                  |
| Swagger UI            | `http://127.0.0.1:8000/docs`             |
| OpenAPI JSON          | `http://127.0.0.1:8000/openapi.json`     |

---

# 🔐 Environment Variables

Create `backend/.env`:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/senai_crm
GEMINI_API_KEY=your_gemini_api_key
LLM_PROVIDER=gemini
SECRET_KEY=your_secret_key
APP_ENV=development
```

Never commit `.env`, API keys, or credentials — commit only `.env.example`.

---

# 🗄️ Database, Alembic & Schema

The application uses **PostgreSQL** as its primary relational database and **SQLAlchemy 2.x** as the ORM. Schema evolution is managed using **Alembic**, ensuring version-controlled migrations and reproducible deployments.

**PostgreSQL Tables:** contacts, threads, emails, classifications, actions, audit_logs, agent_reasoning_logs, knowledge_chunks

**Vector Store:** ChromaDB with MiniLM embeddings for semantic retrieval

## Migration Commands

```bash
# Generate a migration
alembic revision --autogenerate -m "migration message"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

Alembic automatically synchronizes the PostgreSQL schema with SQLAlchemy metadata, providing a safe and maintainable migration workflow.

---

# 📚 Knowledge Base

The platform implements a **RAG pipeline** to ensure AI-generated responses are grounded in verified enterprise policies rather than relying solely on the language model. The knowledge base consists of Markdown documents covering organizational policies, escalation procedures, pricing information, compliance guidelines, FAQs, and API documentation (see `knowledge_base/` in the Project Structure above).

## Seed the Knowledge Base

```bash
python backend/ingest_knowledge.py
```

The ingestion process:

* Reads all Markdown files
* Splits documents into semantic chunks
* Generates embeddings using `all-MiniLM-L6-v2`
* Stores vectors in ChromaDB and metadata in PostgreSQL
* Prevents duplicate chunk insertion (idempotent)

```text
┌──────────────────────────┐
│ Markdown Documents       │
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│ Document Chunking        │
└────────────┬─────────────┘
             ▼
┌───────────────────────────┐
│ MiniLM Embeddings         │
└────────────┬──────────────┘
             ▼
┌───────────────────────────┐
│ ChromaDB Vector Store     │
│ + PostgreSQL Metadata     │
└───────────────────────────┘
```

---

# 📖 API Documentation

FastAPI automatically generates an OpenAPI specification.

| Resource              | URL                                            |
| ---------------------- | --------------------------------------------- |
| Interactive docs        | `http://localhost:8000/docs`                 |
| OpenAPI JSON            | `http://localhost:8000/openapi.json`         |
| Static specs             | `docs/openapi.json`, `docs/swagger.yaml`    |

The specification documents Email, Thread, Customer, AI, Agent, RAG, Analytics, and Health APIs, including request models, response schemas, validation rules, and status codes.

---

# 📊 Performance, Trade-offs & Security

## Performance Optimizations

* Idempotent email ingestion with duplicate message detection
* Cached embedding model loading
* Persistent ChromaDB vector storage, separated from relational storage
* Repository abstraction to avoid duplicate queries
* Service-layer orchestration with dependency-injected database sessions
* Modular AI provider abstraction

## Design Trade-offs

| Design Choice           | Benefit                   | Trade-off                           |
| ----------------------- | ------------------------- | ----------------------------------- |
| Local Embeddings        | Zero API cost             | Higher local CPU usage              |
| ChromaDB                | Lightweight deployment    | Separate storage engine             |
| Markdown Knowledge Base | Easy maintenance          | Manual updates required             |
| Rule + LLM Hybrid       | Higher reliability        | Increased architectural complexity  |
| Human Approval          | Enterprise safety         | Reduced automation                  |
| Dry-Run Agent           | Prevents unsafe execution | Requires manual intervention        |
| Provider Abstraction    | Future extensibility      | Additional abstraction layer        |
| Local Vector Store      | Offline capability        | Not horizontally distributed        |

## Security Considerations

* Environment variables for secrets
* Separation of business logic and persistence
* Human approval required for sensitive actions
* Audit logging for all AI recommendations
* No autonomous execution of critical workflows
* Policy-grounded AI responses with confidence-based escalation
* Least-privilege data access principles

---

# 📈 Scalability Strategy

The architecture is designed for future horizontal scaling. Potential enhancements include:

* Redis caching
* Background task queues
* WebSocket event streaming
* Distributed vector databases
* Multi-agent orchestration
* Multi-tenant deployment
* RBAC authentication
* External email provider integration

---

# ✅ Assessment Coverage

| Requirement                     | Status  |
|---------------------------------|---------|
| AI Email Classification         | ✅      |
| Retrieval-Augmented Generation  | ✅      |
| Enterprise Knowledge Retrieval  | ✅      |
| Explainable AI Reasoning        | ✅      |
| Human-in-the-Loop Workflow      | ✅      |
| Confidence Scoring              | ✅      |
| Escalation Recommendation       | ✅      |
| Audit Logging                   | ✅      |
| CRM Context Enrichment          | ✅      |
| Churn Prediction                | ✅      |
| Executive Summaries             | ✅      |
| Knowledge Explorer              | ✅      |
| Analytics Dashboard             | ✅      |
| SQLAlchemy ORM                  | ✅      |
| PostgreSQL Schema               | ✅      |
| Alembic Migrations              | ✅      |
| OpenAPI Specification           | ✅      |
| React Frontend                  | ✅      |
| FastAPI Backend                 | ✅      |
| RAG Pipeline                    | ✅      |

---

# ⚠️ Known Limitations & 🚀 Future Enhancements

| Current Limitation                                                    | Planned Enhancement                                                |
| --------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Authentication and RBAC are not implemented                           | Role-Based Access Control (RBAC)                                   |
| Email ingestion is dataset/API-driven rather than IMAP/SMTP based     | Live IMAP/SMTP email integration                                   |
| ChromaDB configured for local persistence, not distributed deployment | Distributed vector databases                                       |
| Knowledge base updates require re-ingestion                           | Continuous knowledge synchronization                               |
| Human approval remains mandatory for critical actions                 | Active learning from human edits; fine-tuning from HITL approvals  |
| Background task processing is synchronous                             | Background job queues; real-time WebSocket streaming               |
| No continuous web intelligence integration                            | Live web intelligence integration                                  |
| Prototype assumes trusted internal deployment                         | Multi-agent orchestration architecture; multi-tenant deployment;      automatic prompt optimization |

---

# 📦 Repository Deliverables

All required assessment artifacts are included in the repository (see Project Structure):

* ✅ Complete Source Code (Backend + Frontend)
* ✅ Setup Documentation
* ✅ Architecture & Entity Relationship Diagrams
* ✅ Alembic Migration Files
* ✅ OpenAPI & Swagger Specifications
* ✅ Knowledge Base Documents
* ✅ SQLAlchemy Models & PostgreSQL Schema
* ✅ RAG Pipeline & AI Agent Workflow
* ✅ React Frontend & Analytics Dashboard

---

# 📄 License

This project was developed as a **technical assessment submission** to demonstrate proficiency in AI system design, Retrieval-Augmented Generation (RAG), LLM integration, backend engineering, database design, modern frontend development, enterprise software architecture, explainable AI, human-centered AI workflows, and production-oriented software engineering.

It showcases a modular, extensible, and maintainable AI-powered CRM platform built using modern software engineering principles and industry best practices.