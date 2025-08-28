# 🏛 Layers in Clean Architecture

```pgsql
+----------------------+
|     Presentation     |  ← FastAPI Routes, Controllers
+----------------------+
|   Application Layer  |  ← Use Cases, Services, Orchestrators
+----------------------+
|    Domain Layer      |  ← Entities, Business Rules, Models
+----------------------+
|  Infrastructure      |  ← DB, External APIs, Repositories
+----------------------+
```

- **Presentation Layer** -> User interaction (FastAPI endpoints)
- **Application Layer** -> Use cases (defines what the system should do)
- **Domain Layer** -> Pure business logic (Entities, Value Objects)
- **Infrastructure Layer** -> Implements interfaces (DB, APIs, etc)


# Clean Architecture with FastAPI

We’ll build a Task Manager API with Clean Architecture.

## 📂 Project Structure

```bash
fastapi_clean_arch/
│── app/
│   ├── main.py
│   ├── api/               # Presentation Layer
│   │   └── v1/
│   │       └── task_routes.py
│   ├── application/       # Application Layer
│   │   └── task_service.py
│   ├── domain/            # Domain Layer
│   │   └── task.py
│   ├── infrastructure/    # Infrastructure Layer
│   │   ├── db.py
│   │   └── task_repository.py
│   └── schemas.py
```

### How to run:

```bash
uvicorn app.main:app --reload
```

Test Endpoints:

- POST /tasks → Create Task
- GET /tasks → List Tasks
- PUT /tasks/{id} → Mark Completed


## 🔥 Why This is Clean?

- Business rules (Task entity) have zero knowledge of FastAPI or DB.
- TaskService (use cases) depends only on abstract repo.
- TaskRepository can be swapped (e.g., SQLite, Postgres) without changing service.
- Routes just orchestrate request/response mapping.