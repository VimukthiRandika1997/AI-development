# Overview

Modern APIs need to trigger long-running jobs ( like data-processing, API calls (external), machine-learning model training ) which exceed typical HTTP timeout windows (30-60 seconds). Traditional synchronous APIs can not handle these types of jobs, hence either timeouts or refreshing the state are required.

## Issues with traditonal synchronous APIs:

- Execution time is longer ( > 60 seconds)
- This interfers the client-UI interactions
- Can not scale with heavy loads


## Solution:

Hence we need a non-blocking, aysnc-safe job system to handle these types of long-running jobs.



### Modular Architecture Diagram

![system-architecture](/api_design/FastAPI/long_running_jobs_with_fastapi/assets/long_running_task_overview.png)

### Workflow

```markdown
+-------------------+
|      Client       |
| (User / API Call) |
+-------------------+
        |
        v   HTTP (POST /start-job, GET /status)
+-------------------+
|     FastAPI App   |  <-- app/main.py
+-------------------+
        |
        v
+-------------------+
|     API Router    |  <-- app/api/v1/router.py
+-------------------+
        |
        v
+-------------------+
|   Job Service     |  <-- app/modules/jobs/service.py
+-------------------+
   |            |
   | Save job   | Submit task
   v            v
+-----------+   +-------------------+
| Database  |   |   Celery Worker   | <-- app/modules/jobs/tasks.py
|  (Jobs)   |   +-------------------+
+-----------+            |
       ^                 v
       |        +-------------------+
       |        |  Redis Broker     |
       |        |  (Message Queue)  |
       |        +-------------------+
       |
       +--- Worker updates status/results
```

Flow Explanation:

1. Client calls FastAPI (/start-job or /status).
2. FastAPI → Router → Job Service: request gets routed to service layer.
3. Job Service:
    1. Saves initial job status in Database with a job_id.
    2. Sends task to Celery Worker via Redis Broker.
4. Celery Worker executes long-running task.
5. Worker updates Database with results.
6. Client can query/poll status/results from FastAPI, which pulls from DB.

<!-- Client can query status/results from FastAPI, which pulls from DB.

1. Client submits a long-running job via POST /start-job/, optionally providing a callback_url.

2. Server enqueues the job (for simplicity, via background task).

3. Server immediately returns a job_id.

4. Client polls GET /status/{job_id} to check progress/completion.

5. Optionally, when the job finishes and the client provided a callback_url, the server sends the result via webhook. -->

## Sequence Diagram

Here the sequence diagram for this whole process:

![api-design](/api_design/FastAPI/long_running_jobs_with_fastapi/assets/fastapi_celery_sequence_diagram.png)

# Tech Stack

- ✅ Celery (task queue) for long-running jobs

- ✅ Redis as broker & result backend

- ✅ Database (SQLite for demo) to persist job metadata

- ✅ FastAPI for submitting jobs and polling jobs + optional webhook callback


# 📂 Project Structure

This is the clean and modular project layout:

```markdown
app/
├── __init__.py
├── main.py
├── core/
│   ├── config.py
│   └── celery_app.py
├── db/
│   ├── __init__.py
│   └── models.py
├── api/
│   └── v1/
│       ├── __init__.py
│       └── router.py
├── modules/
│   └── jobs/
│       ├── __init__.py
│       ├── tasks.py
│       └── service.py
requirements.txt
Dockerfile
docker-compose.yml
```


# How to run

1. ▶️ Build and Run Everything

    ```bash
    docker-compose up --build
    ```

    This will set:

    - FastAPI app → http://localhost:8000
    - Redis broker → redis://redis:6379/0 (inside Docker network)
    - Celery worker automatically connected

2. 📋 Usage

    1. Start a job:

        ```bash
        curl -X POST "http://127.0.0.1:8000/api/v1/start-job/" \
            -H "Content-Type: application/json" \
            -d '{"callback_url": "http://example.com/webhook"}'
        ```

    2. Poll status:

        ```bash
        curl http://127.0.0.1:8000/api/v1/status/<job_id>
        ```

👉 Now you have a self-contained dockerized environment:

- web → FastAPI API
- worker → Celery worker
- redis → Broker

# 🧠 Analysis

- Additionally we can setup a webhook to get the result of a particular task once it is completed:

- Here is the pros and cons of both approaches:

    | Approach | Pros | Cons |
    |-----------------|-----------------|-----------------|
    | Polling  | simple to implement  | heavy load on the server  |
    | Wehhooks  | real-time notification  | endpoints must be exposed  |

# 🛡️ Production Considerations

- Add **authentication** to endpoints and webhooks
- Implement retry-mechanism for failed webhook deliveries
- Add timeouts for stale jobs


# 💭 Final Thoughts

- Using this base layout, now we can build scalable system for serving long-running jobs without blocking our main app thread. 
- Common use-cases could be like:
    - ML inference
    - Report Generation ( like model metric-generation after inference )
    - Video Analysis