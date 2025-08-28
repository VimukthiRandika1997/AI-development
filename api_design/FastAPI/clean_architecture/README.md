# Clean Architecture

Introduction to Clean Architecture

## What is Clean Architecture ?

This is a software design principle that helps to build scalable, maintainable and testable applications by organizing code into clear layers with strict dependency rules.

## 🔑 Core Principles

- **Seperation of concerns**: Business logic is isolated from frameworks, UI, DB and external services.
- **Dependency Rule**: Source code dependencies always point inward (from outer layers -> inner layers).
- **Testability**: You can test core logic without worrying about DB, APIs or frameworks.
- **Framework Independent**: You can swap FastAPI for Flask, PostgreSQL for MongoDB, etc., without changing core logic.

## 🏛 Layers in Clean Architecture

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