---
trigger: always_on
---

# Project instructions for AI coding assistants

You are an AI coding assistant working **inside this repository**.  
Always follow the rules below when generating, editing, or explaining code.

---

## 1. Project overview

This project is a **backend web application** built with **Python + FastAPI**.  
The main purpose is to store and browse **LLM responses (Markdown) and their metadata**:

- Store responses from tools like ChatGPT, Gemini, etc.
- Organize them by **category** and **tags**.
- Expose a clean **HTTP API** that a separate frontend (e.g., React + TypeScript) can consume.
- Follow a **Hexagonal Architecture (Ports & Adapters)** style.

The backend should stay **framework-aware but domain-centric**:
- Business rules live in the **domain** and **application** layers.
- FastAPI, SQLAlchemy, HTTP, and storage concerns are isolated in **adapters**.

---

## 2. Tech stack

- Language: **Python 3.11+** with full type hints.
- Web framework: **FastAPI**.
- Validation / schemas: **Pydantic v2**.
- Persistence:
  - Development: **SQLite** (simple file-based DB).
  - Production-ready design: can switch to **PostgreSQL** later.
- ORM / data access: **SQLAlchemy 2.x style** (or SQLModel if already present).
- Testing: **pytest** (+ httpx for API tests, if needed).

When generating code, assume modern FastAPI + Pydantic v2 and SQLAlchemy 2.x patterns.

---

## 3. High-level architecture

We use a **Ports & Adapters (Hexagonal Architecture)** layout.

At a high level:

- `app/domain`  
  Pure domain layer: entities, value objects, domain services, and **ports** (interfaces).
- `app/application`  
  Application layer: use cases (orchestrating domain operations via ports).
- `app/adapters/inbound`  
  Driving adapters: incoming interfaces such as HTTP APIs (FastAPI).
- `app/adapters/outbound`  
  Driven adapters: implementations of domain ports, e.g., DB repositories, external API clients.
- `app/config`  
  Application settings, logging configuration, dependency wiring helpers.
- `tests`  
  Unit tests for domain + application, integration tests for adapters, and E2E tests for API.

The **dependency direction** must always point **toward the domain**:

- `domain` depends on **nothing** outside `domain`.
- `application` depends only on `domain` (including `domain.ports`).
- `adapters` depend on `application` and `domain`, but **never the opposite**.
- `config` and `main.py` are allowed to wire everything together.

---

## 4. Directory layout (detailed)

Treat the directory structure below as the **source of truth**.  
When generating new files, place them in the correct layer and follow the same naming patterns.

### 4.1 `app/`

- `app/main.py`  
  FastAPI entrypoint. Creates the `FastAPI` app, includes routers, and wires dependencies.

### 4.2 `app/domain/`

Pure domain logic. No FastAPI, no SQLAlchemy, no HTTP specifics.

- `app/domain/models/`  
  - Domain entities and value objects, implemented as regular classes or `dataclass`es.
  - Example: `llm_response.py`, `category.py`, etc.
- `app/domain/services/`  
  - Domain services that implement complex business rules which don’t naturally belong inside a single entity.
- `app/domain/ports/`  
  - **Ports (interfaces)** for outbound dependencies.
  - Example: `LLMResponseRepository`, `CategoryRepository`, storage ports, etc.
  - These are abstract base classes or protocols.
- `app/domain/exceptions.py`  
  - Domain-specific exceptions (business rule violations, not HTTP or DB errors).

### 4.3 `app/application/`

Application (use-case) layer. Orchestrates domain models via ports.

- `app/application/use_cases/`  
  - Each file or class represents a **use case**, e.g.:
    - `CreateLLMResponseUseCase`
    - `ListLLMResponsesUseCase`
    - `UpdateCategoryUseCase`
  - Use cases call ports from `domain.ports` and operate on `domain.models` entities.
  - No FastAPI, no SQLAlchemy here.
- `app/application/dto/` (optional)  
  - Internal DTOs for passing data into/out of use cases.
  - These can be simple `dataclass`es; they do **not** depend on FastAPI or Pydantic.

### 4.4 `app/adapters/inbound/`

Driving adapters: code that receives requests from the outer world and calls use cases.

- `app/adapters/inbound/api/routers/`  
  - FastAPI router modules.
  - They:
    - Define HTTP endpoints and routes.
    - Use Pydantic models from `schemas` for request/response I/O.
    - Call application use cases.
- `app/adapters/inbound/api/schemas/`  
  - Pydantic **API I/O models** (request/response schemas).
  - These map between HTTP JSON payloads and internal use case DTOs or domain models.
- `app/adapters/inbound/api/dependencies.py`  
  - FastAPI dependency-injection factories.
  - Responsible for building use case instances with required ports/repositories.

### 4.5 `app/adapters/outbound/`

Driven adapters: implementation of domain ports using concrete technologies.

- `app/adapters/outbound/persistence/`  
  - Database-related code (repositories, unit-of-work).
- `app/adapters/outbound/persistence/sqlalchemy/`  
  - SQLAlchemy ORM models and repository implementations.
  - Responsible for mapping between ORM objects and domain entities.
- `app/adapters/outbound/external_services/`  
  - HTTP clients or SDK wrappers for external services (if any).
  - Implement ports defined in `app/domain/ports`.

### 4.6 `app/config/`

- `app/config/settings.py`  
  - Global configuration using `pydantic-settings` or environment variables.
  - DB URL, log level, etc.
- `app/config/logging.py`  
  - Central logging configuration (formatters, handlers, log levels).

---

## 5. Domain: core data model (LLM responses)

The primary domain in this project is:

- **LLMResponse**
  - Fields: id, title, prompt, content_md (Markdown), model, provider, category_id, tags, summary, created_at, updated_at, storage_location, storage_path, etc.
- **Category**
  - Fields: id, name, description, created_at, updated_at.
- Optional: **Tag** entities or tag strings saved in a JSON column.

When generating new code in the domain or application layers:

- Keep entities **persistence-agnostic** (they should not know about SQLAlchemy, FastAPI, or HTTP).
- Keep business rules inside domain entities/services, not in API or ORM code.

---

## 6. Layering & dependency rules (hard constraints)

When generating code, you **must** respect the following rules:

1. **No framework imports in domain or application layers**
   - Do **not** import FastAPI, Starlette, SQLAlchemy, Pydantic, or HTTP clients inside:
     - `app/domain/**`
     - `app/application/**`
2. **Domain does not depend on adapters**
   - Domain (`app/domain`) must not import anything from `app/adapters` or `app/config`.
3. **Application depends only on domain**
   - `app/application` may import from `app/domain`, but not from `app/adapters`.
4. **Adapters are allowed to depend on application & domain**
   - `app/adapters/**` can import from `app/application` and `app/domain`.
5. **main/config wires everything together**
   - Dependency injection and composition happen in `app/main.py` and `app/config/**`.

If you need to introduce a new external dependency (DB, API, etc.):

- First: define a **port interface** in `app/domain/ports/`.
- Then: implement it in `app/adapters/outbound/**`.
- Finally: wire it into use cases in `app/adapters/inbound/api/dependencies.py` or similar factories.

---

## 7. Coding style & conventions

When generating Python code:

- Use **PEP8** style and type hints everywhere.
- Prefer modern language features (`match`, `|` unions, dataclasses where appropriate).
- Avoid `from module import *`.
- For FastAPI:
  - Use async endpoints: `async def`.
  - Use Pydantic v2-compatible models (`BaseModel`) with `model_config = ConfigDict(from_attributes=True)` when mapping from ORM objects.
- For SQLAlchemy:
  - Use **2.x style** with `DeclarativeBase` or similar.
  - Keep ORM models in the outbound persistence layer, not in the domain.

Testing:

- Unit tests for domain and application layers should not require a real database.
- Integration tests for adapters can use a real DB (e.g., SQLite in memory).
- E2E tests for FastAPI can use `TestClient` + test database.

---

## 8. Behaviors specific to AI coding agents

When acting as an AI agent (e.g., GitHub Copilot, Google Antigravity):

- **Respect the architecture**:
  - Place new files in the correct layer and directory.
  - Do not mix concerns (e.g., no HTTP logic in repositories, no SQL in routers).
- **Prefer small, focused functions and classes** over large monoliths.
- **Preserve existing patterns and naming conventions** when editing or adding code.
- **Do not execute destructive shell commands** (like `rm -rf`, bulk deletion outside this repository, or touching non-project directories).
- Assume that another frontend (React/TypeScript) may call this API in the future, so:
  - Keep API contracts stable.
  - Use clear and explicit request/response schemas.

Whenever you are unsure about where to put new code, follow this rule of thumb:

- **Domain rule / invariant?** → `app/domain/**`
- **Use case / application flow?** → `app/application/use_cases/**`
- **HTTP or CLI interface?** → `app/adapters/inbound/**`
- **DB or external service integration?** → `app/adapters/outbound/**`
- **Configuration / wiring / startup?** → `app/config/**` or `app/main.py`
