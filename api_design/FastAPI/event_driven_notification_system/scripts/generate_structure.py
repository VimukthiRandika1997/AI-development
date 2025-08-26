import os

# Define the folder and file structure
structure = {
    "fastapi-webhooks": {
        "docker-compose.yml": "",
        "Dockerfile": "",
        ".env.example": "",
        "requirements.txt": "",
        "README.md": "# fastapi-webhooks\n\nA FastAPI-based webhook dispatcher with worker support.\n",
        "app": {
            "__init__.py": "",
            "main.py": "# FastAPI entrypoint\n",
            "core": {
                "config.py": "# Settings via environment variables\n"
            },
            "schemas.py": "# Pydantic schemas\n",
            "db.py": "# Database connection and models\n",
            "webhooks": {
                "dispatcher.py": "# Webhook dispatch logic\n",
                "utils.py": "# Webhook utility functions\n"
            },
            "worker.py": "# Background worker (Celery/RQ/etc.)\n"
        }
    }
}


def create_structure(base_path, struct):
    for name, content in struct.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            os.makedirs(base_path, exist_ok=True)
            with open(path, "w") as f:
                f.write(content)


if __name__ == "__main__":
    create_structure(".", structure)
    print("✅ fastapi-webhooks project structure created successfully!")
