import os

# Define the folder and file structure
structure = {
    "app": {
        "__init__.py": "",
        "main.py": "# FastAPI entrypoint\n",
        "core": {
            "config.py": "# Settings\n",
            "celery_app.py": "# Celery initialization\n"
        },
        "db": {
            "__init__.py": "",
            "models.py": "# SQLAlchemy Job model\n"
        },
        "api": {
            "v1": {
                "__init__.py": "",
                "router.py": "# API endpoints\n"
            }
        },
        "modules": {
            "jobs": {
                "__init__.py": "",
                "tasks.py": "# Celery tasks\n",
                "service.py": "# Job service logic\n"
            }
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
    create_structure("..", structure)
    print("✅ Project structure created successfully!")
