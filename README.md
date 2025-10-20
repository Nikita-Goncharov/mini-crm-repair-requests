# Mini CRM — Repair Requests Backend

A lightweight CRM system for managing repair requests, with role-based access for **Admins** and **Workers**.  
Built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **Alembic**.

---

## 🚀 Local Run (Docker Compose)

### 1. Clone the repository
```bash
git clone https://github.com/Nikita-Goncharov/mini-crm-repair-requests.git
cd mini-crm-repair-requests
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=database

TEST_ADMIN_LOGIN=admin
TEST_ADMIN_PASSWORD=pass

TEST_WORKER_LOGIN=worker
TEST_WORKER_PASSWORD=pass

DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/database
DATABASE_URL_SYNC=postgresql://postgres:postgres@localhost:5432/database

SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 3. Run with Docker Compose

```bash
docker compose up --build
```

The backend will be available at:

```
http://localhost:8000
```

Swagger docs:

```
http://localhost:8000/docs
```

---

## 🧩 Database & Migrations

If you’re running locally (not in Docker) or want to apply migrations manually:

### Create migration:

```bash
alembic revision --autogenerate -m "message"
```

### Apply migration:

```bash
alembic upgrade head
```

When using Docker, migrations are automatically applied on container startup.

---

## 🔑 Environment Variables

| Variable                      | Description                                |
| ----------------------------- | ------------------------------------------ |
| `POSTGRES_USER`               | PostgreSQL username                        |
| `POSTGRES_PASSWORD`           | PostgreSQL password                        |
| `TEST_ADMIN_LOGIN`            | Login for test admin record                |
| `TEST_ADMIN_PASSWORD`         | Password for test admin record             |
| `TEST_WORKER_LOGIN`           | Login for test worker record               |
| `TEST_WORKER_PASSWORD`        | Password for test worker record            |
| `POSTGRES_DB`                 | Database name                              |
| `DATABASE_URL`                | Async DB connection string                 |
| `DATABASE_URL_SYNC`           | Sync DB connection (for local tools/tests) |
| `SECRET_KEY`                  | Secret key for JWT tokens                  |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time (in minutes)         |

---

## 📡 API Endpoints

### 🔐 Auth

| Method | Endpoint          | Description                       |
| ------ | ----------------- | --------------------------------- |
| `POST` | `/api/auth/token` | Obtain JWT token for admin/worker |

### 🧑‍💼 Admin

| Method   | Endpoint                                | Description             |
| -------- | --------------------------------------- | ----------------------- |
| `POST`   | `/api/admin/workers`                    | Create worker account   |
| `GET`    | `/api/admin/workers`                    | Get all workers         |
| `DELETE` | `/api/admin/workers/{id}`               | Delete worker           |
| `GET`    | `/api/admin/tickets`                    | Get all tickets         |
| `POST`   | `/api/admin/tickets/{ticket_id}/assign` | Assign ticket to worker |

### 🔧 Worker

| Method | Endpoint                                 | Description                                       |
| ------ | ---------------------------------------- | ------------------------------------------------- |
| `GET`  | `/api/worker/tickets`                    | Get assigned tickets                              |
| `PUT`  | `/api/worker/tickets/{ticket_id}/status` | Update ticket status (e.g. `in_progress`, `done`) |

### 📞 Public

| Method | Endpoint              | Description                        |
| ------ | --------------------- | ---------------------------------- |
| `POST` | `/api/public/tickets` | Create new repair request (ticket) |

---

## 🧰 Example Tokens

You can test endpoints using **Postman**.
Sample Authorization header:

```
Authorization: Bearer <your_access_token>
```

---

## 🧱 Tech Stack

* **FastAPI** — web framework
* **SQLAlchemy 2.0** — ORM
* **PostgreSQL** — database
* **Alembic** — migrations
* **Docker Compose** — container orchestration
* **JWT Auth** — authentication system
