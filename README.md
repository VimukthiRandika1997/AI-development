# Building and Experimenting Production Grade AI Applications

## API Design For AI-Background Generation

A production grade FastAPI service for AI Background Generation using fine-tuned diffusion models:

- [api-design](/ai-background-generation/README.md)
- [product-development](https://github.com/VimukthiRandika1997/AI-background-generation)

- ![Sample generated product-shots](/ai-background-generation/assets/sample_image.png)

## RAGs

Production grade RAG for business-usecases: [check-this](/ai_workflows/Document_analysis_RAG/README.md)


## FastAPI Design

Architecting the FastAPI for different use-cases. 

- ## Handling Long Running Jobs with FastAPI

- A non-blocking, async-safe job-system to handle long-running background tasks: [more details](/api_design/FastAPI/long_running_jobs_with_fastapi/README.md)

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