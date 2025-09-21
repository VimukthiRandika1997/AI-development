# Handling Memory Leaks

<p align="center">
  🚧 <br />
  <b>Under Construction</b>
</p>

## 💡 The Issue

Python sometimes doesn't free up memory

- When we run a python program that uses a lot of RAM, small bits of memory can stay **stuck** even after the work is done
- If we keep running the same code again and again, those stuck bits adds up
- In AI systems, often time big files like PDFs or images are handled.
- This it eats lots of memory and if that memory isn't released, we get an **Out Of Memory (OOM)** error.

Example:

- We have a FastAPI server that reads PDFs for an AI pipeline
- Each time a PDF is uploaded, memory usage creeps a bit higher
- After many uploads, the server runs out of RAM and dies

## 🧠 The Goal

We want to ingest PDFs for an AI system without leaking memory

- Instead of letting the FastAPI web-server handle heavy PDF processing, we hand the heavy work to **short-lived worker process**
- Each worker finishes its job and exits, so the operating system frees all the memory automatically

| Component                       | Role                                                                                   |
| ------------------------------- | -------------------------------------------------------------------------------------- |
| **FastAPI app (`main.py`)**     | Receives the uploaded PDF and pushes a “to-do” job into a queue.                       |
| **Redis**                       | Acts as the “queue” (message broker) so FastAPI and the worker can talk.               |
| **Celery worker (`worker.py`)** | A separate process that takes a job from the queue, processes the PDF, and then exits. |
| **Docker / Docker Compose**     | Runs everything in isolated containers so it’s easy to start, stop, and scale.         |


## ✅ Implementation

Instead of letting your main app process every PDF directly:

1. Main server takes the request only.
2. It accepts the PDF and puts a message in a “to-do” list (a queue).
3. A worker process wakes up.
4. This worker is a separate program whose only job is to handle one PDF.
5. Worker finishes and quits.
6. When it quits, the operating system automatically frees all the memory it used—no leaks stay behind.
7. Repeat for the next file.

Each new PDF spins up a fresh worker. No build-up of hidden memory.

## Concrete Example

### Project Structure

```markdown
pdf_ingestion_service/
├─ app/
│  ├─ main.py
│  ├─ worker.py
│  └─ ingest.py
├─ requirements.txt
├─ Dockerfile
└─ docker-compose.yml
```

# Workflow

1. User uploads a PDF

    - A client sends a POST request to http://localhost:8000/ingest with a file
    - FastAPI saves the file temporarily on disk

2. FastAPI queues the job


### How to Run locally

1. Build the docker images

    ```bash
    docker-compose up --build
    ```

2. Upload a PDF file to the server

    ```bash
    curl -F "file=@example.pdf" http://localhost:8000/ingest
    ```
3. If we need more throughput, then we can run more workers:

    ```bash
    docker compose up --scale worker=5
    ```

    - Now 5 workers can process 5 PDFs at the same time
    - Each of them is still short-lived and memory safe

### How to deploy to GCP Cloud Run
