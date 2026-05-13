# file-scan

A **Retrieval-Augmented Generation (RAG)** API for asking natural-language questions about PDF documents. Built with FastAPI, PostgreSQL + pgvector, OpenAI, and Docker.

---

## What it does

1. Upload a PDF.
2. Ask a question about it in plain English.
3. Get an answer — generated from the most relevant sections of the document, not the whole thing.

Behind the scenes, the app splits the PDF into chunks, generates a vector embedding for each chunk, and stores them in Postgres. When you ask a question, the question itself is embedded and pgvector finds the chunks closest in meaning. Only those chunks are sent to the LLM — keeping responses fast, cheap, and accurate even for very long documents.

---

## Architecture

```
┌─────────┐    ┌───────┐    ┌─────────┐    ┌─────────┐    ┌──────────────┐
│ /upload │ -> │ PDF   │ -> │ Chunker │ -> │ OpenAI  │ -> │ Postgres     │
│         │    │ text  │    │ (500ch) │    │ embed   │    │ (pgvector)   │
└─────────┘    └───────┘    └─────────┘    └─────────┘    └──────────────┘

┌─────────┐    ┌──────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────┐
│  /ask   │ -> │ OpenAI   │ -> │ pgvector     │ -> │ Concat top  │ -> │ LLM  │
│         │    │ embed Q  │    │ cosine top-K │    │ K chunks    │    │      │
└─────────┘    └──────────┘    └──────────────┘    └─────────────┘    └──────┘
```

### Data model

```
User  ──1:N──>  Document  ──1:N──>  Chunk
                                      └─ embedding: Vector(1536)
```

---

## Tech stack

| Layer | Choice | Why |
|---|---|---|
| API framework | **FastAPI** | Async, automatic OpenAPI docs, modern type-hint-first design |
| ORM | **SQLAlchemy 2.0** | Modern `Mapped[]` syntax, plays well with FastAPI |
| Database | **PostgreSQL 16** + **pgvector** | Vector similarity search in the database, no separate vector store needed |
| Migrations | **Alembic** | Versioned, auto-generated schema changes |
| PDF parsing | **PyMuPDF (fitz)** | Fast, reliable PDF text extraction |
| Embeddings | **OpenAI `text-embedding-3-small`** | 1536-dim, cheap (~$0.02 / 1M tokens) |
| LLM | **OpenAI `gpt-5-mini`** | Cost-effective for short Q&A use cases |
| Containerization | **Docker Compose** | One command runs the whole stack |

---

## Running locally

### Prerequisites

- Docker + Docker Compose
- An OpenAI API key

### Setup

```bash
# 1. Clone
git clone <this-repo-url>
cd file-scan

# 2. Configure environment
cp .env.example .env
# Edit .env and set OPENAI_API_KEY + JWT_SECRET
# Generate a JWT secret: python -c "import secrets; print(secrets.token_urlsafe(32))"

# 3. Start the stack
docker compose up --build -d

# 4. Run the migrations (first time only)
docker exec -it filescan_app alembic upgrade head
```

The API is now running at `http://localhost:8000`. Register a user at `/register`, log in at `/login`, then upload PDFs and ask questions.

---

## API reference

All `/upload` and `/ask` requests require a JWT in the `Authorization: Bearer <token>` header. Obtain one via `/login`.

### `POST /register`

Create a new user. Passwords are hashed with bcrypt before storage.

```bash
curl -X POST http://localhost:8000/register \
  -F "username=alice" \
  -F "password=hunter2pls"
```

Response:
```json
{ "id": 2, "username": "alice" }
```

### `POST /login`

Verify credentials and receive a JWT (valid 24h).

```bash
curl -X POST http://localhost:8000/login \
  -F "username=alice" \
  -F "password=hunter2pls"
```

Response:
```json
{ "access_token": "eyJhbGciOi...", "token_type": "bearer" }
```

### `POST /upload`

Upload a PDF and have it chunked, embedded, and stored. The document is owned by the authenticated user.

```bash
curl -X POST http://localhost:8000/upload \
  -H "Authorization: Bearer <token>" \
  -F "pdf=@/path/to/your.pdf"
```

Response:
```json
{ "document_id": 1 }
```

### `POST /ask`

Ask a question about one of your uploaded documents. Returns 404 if the document doesn't belong to you (no existence leak).

```bash
curl -X POST http://localhost:8000/ask \
  -H "Authorization: Bearer <token>" \
  -F "document_id=1" \
  -F "question=What is this document about?"
```

Response:
```json
{ "answer": "This document discusses ..." }
```

### `GET /db-check`

Health check — confirms the database is reachable. No auth required.

---

## Project structure

```
file-scan/
├── app/
│   ├── main.py              # FastAPI app, router registration
│   ├── config.py            # Loads env vars
│   ├── db.py                # Engine, SessionLocal, Base
│   ├── models/              # SQLAlchemy ORM models (User, Document, Chunk)
│   ├── routes/              # HTTP layer (thin)
│   │   ├── upload.py        # POST /upload — ingest pipeline
│   │   ├── ask.py           # POST /ask — retrieval + LLM
│   │   ├── home.py          # GET /
│   │   └── health.py        # GET /db-check
│   └── services/            # Business logic + DB operations
│       ├── pdf.py           # PyMuPDF text extraction
│       ├── chunker.py       # Splits text into ~500-char chunks
│       ├── embeddings.py    # OpenAI embeddings wrapper
│       ├── storage.py       # save_document + get_top_chunks
│       └── llm.py           # OpenAI chat completion wrapper
├── alembic/                 # DB migrations
├── templates/, static/      # Server-rendered UI (minimal)
├── Dockerfile               # App image
├── docker-compose.yml       # App + Postgres
└── requirements.txt
```

---

## Why I built this

I wanted a portfolio project that goes beyond CRUD apps — something that shows I understand modern AI-adjacent backend patterns. RAG was a great choice because it forced me to learn: vector embeddings, similarity search at the database level, Alembic migrations with custom Postgres extensions, and a clean layered architecture (models / services / routes).

I deliberately kept the LLM logic dumb and the data layer interesting — the hard parts of RAG aren't talking to OpenAI, they're chunking, retrieval quality, and how you store/query vectors.

---

## What's next

- **Per-user document list UI** — currently the home page only uploads-and-asks in one shot; a "your documents" view + dashboard is the next iteration
- **Logout + `/me` endpoint** — small additions to round out the auth surface
- **Smarter chunking** — sentence-aware splitting instead of fixed character windows
- **Logging** — replace remaining `print` statements with the `logging` module
- **More test coverage** — currently covers chunker + auth (hash/verify/JWT); route-level integration tests are next

---

## Notes for reviewers

- All migrations live in `alembic/versions/` and are auto-applied by the setup steps above.
- The `vector` Postgres extension is enabled inside the first migration (`CREATE EXTENSION IF NOT EXISTS vector`).
- pgvector cosine distance is used for retrieval: `.order_by(Chunk.embedding.cosine_distance(question_vector)).limit(5)`.
