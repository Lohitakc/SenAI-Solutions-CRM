# SenAI Solutions CRM

SenAI Solutions CRM is a production-oriented AI CRM platform designed to help teams manage customer relationships, organize operational knowledge, and prepare for AI-assisted workflows.

This repository is currently in the initial development setup phase. The project structure, documentation, and dependency boundaries are being established before business logic, APIs, database models, frontend implementation, or AI functionality are added.

## Architecture Overview

The system is planned as a modular full-stack application with clear separation between backend services, frontend user experience, CRM data, AI agent orchestration, and knowledge-base assets.

Planned architectural boundaries:

- Backend API layer for HTTP interfaces and request handling.
- Backend service layer for business workflows and orchestration.
- Backend model layer for future database entities and persistence.
- Core backend utilities for configuration, security, and shared infrastructure.
- AI agent boundary for future agent workflows and automation.
- Knowledge base boundary for future retrieval-ready CRM content.
- Frontend boundary for the future customer-facing application interface.

## High-Level Features

Planned capabilities include:

- Contact and customer relationship management.
- Sales and activity tracking.
- AI-assisted CRM workflows.
- Knowledge-base powered assistance.
- PostgreSQL-backed persistence.
- Future vector search support for retrieval workflows.
- Maintainable backend and frontend separation.

Implementation details will be added incrementally as the project evolves.

## Technology Stack

Planned development stack:

- Python for backend application development.
- FastAPI for future backend APIs.
- SQLAlchemy for future database access.
- PostgreSQL 16 for relational persistence.
- pgvector for future vector similarity search.
- Alembic for future database migrations.
- sentence-transformers for future embedding generation.
- React or a comparable frontend framework for the future UI.

## Current Development Status

Current phase: initial repository setup.

Completed:

- Repository scaffold.
- Git ignore rules.
- Project documentation baseline.

Not implemented yet:

- Backend application logic.
- API routes.
- Database models.
- Frontend application code.
- AI agent workflows.
- Retrieval-augmented generation.
- Docker configuration.
- CI/CD pipelines.
- Automated tests.

## Repository Structure

```text
SenAI-Solutions-CRM/
+-- backend/
|   +-- app/
|       +-- agent/
|       +-- api/
|       +-- core/
|       +-- models/
|       +-- services/
+-- frontend/
+-- knowledge_base/
+-- architecture/
+-- data/
+-- tests/
+-- .gitignore
+-- README.md
```

## Future Setup

The setup process will be documented as implementation begins.

Planned setup steps:

1. Create and activate a Python virtual environment.
2. Install backend dependencies.
3. Configure environment variables.
4. Connect to PostgreSQL.
5. Initialize database migrations.
6. Start backend and frontend development servers.

Detailed commands will be added once the corresponding implementation files exist.

## Backend Environment

Create a local backend environment file at `backend/.env` before running the API:

```text
DATABASE_URL=postgresql://postgres:password@localhost:5432/senai_crm
GEMINI_API_KEY=your_key
LLM_PROVIDER=gemini
SECRET_KEY=your_secret
APP_ENV=development
```

Never commit `backend/.env`. It contains local credentials and machine-specific configuration. Commit `backend/.env.example` instead because it documents the required variable names without exposing real secrets.

## Backend Troubleshooting

- `ModuleNotFoundError`: Activate the virtual environment and run commands from `backend/` when importing `app.*` modules.
- `ImportError`: Reinstall dependencies with `..\venv\Scripts\python.exe -m pip install -r requirements.txt` from `backend/`.
- `python-dotenv` issues: Confirm `python-dotenv` is installed and `backend/.env` exists with valid `KEY=value` lines.
- `pydantic-settings` issues: Confirm `pydantic-settings` is installed and environment variable names match `backend/.env.example`.
- `SQLAlchemy` issues: Verify `DATABASE_URL` starts with `postgresql://` and that PostgreSQL 16 is running.
- Port `8000` already in use: Stop the existing process or temporarily change the port in `backend/run.py` during local debugging.
- Virtual environment activation problems: Run `.\venv\Scripts\Activate.ps1` from the repository root and fix PowerShell policy with `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` if needed.
- Missing environment variables: Create `backend/.env` from `backend/.env.example` and fill required local values.
- Incorrect PostgreSQL URL: Check username, password, host, port, and database name; create the database before using it in later phases.

## Database Architecture

The backend uses SQLAlchemy 2.x typed ORM models with PostgreSQL 16. Database infrastructure lives in `backend/app/db/`, while ORM entities live in `backend/app/models/`.

Core decisions:

- Shared base model provides `id`, `created_at`, and `updated_at` across tables for consistency.
- Engine and session setup stay outside ORM models to keep persistence lifecycle separate from entity definitions.
- Each ORM model has its own file to keep ownership clear as the CRM domain grows.
- PostgreSQL enums are used for status and priority values to avoid fragile magic strings.
- `backend/init_db.py` initializes tables explicitly; schema creation is never triggered by import side effects.

Tables:

- `contacts`: Stores CRM contacts and links each contact to their conversation threads.
- `threads`: Groups related emails by conversation and tracks status and priority.
- `emails`: Stores individual email records inside a thread.
- `classifications`: Stores one future classification result per email.
- `actions`: Stores future recommended or executed actions linked to emails.
- `knowledge_chunks`: Stores knowledge-base metadata only; embeddings are added in a later phase.
- `audit_logs`: Records system events for traceability and operational auditing.

Initialize the local schema from `backend/`:

```powershell
..\venv\Scripts\python.exe init_db.py
```

## Development Principles

This project will prioritize:

- Small, atomic commits.
- Clear module boundaries.
- Minimal dependencies.
- Maintainable architecture.
- Secure handling of secrets and environment configuration.
- Incremental implementation with verification at each step.
