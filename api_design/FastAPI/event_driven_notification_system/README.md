# Event Driven Notification System with Webhooks

A FastAPI-based webhook dispatcher with worker support. Here we are designing a complete system for learning purpose.

<p align="center">
  🚧 <br />
  <b>Under Construction</b>
</p>

# Overview

We have seen apps that notify us the moment something important happens: *a payment succeeds, a task completes or a new comment lands on our social-media post*. This kind of responses are based on event-driven notification systems which integrate deeply with APIs and external services using **webhooks**.

In machine-learning, this can be useful feature to have:
- When building a real-time analytics dashboard, updates are pushed to the dashboard without having to **polling** the backend APIs.
- When building a ML-training platform, onces the tasks are finished and results are pushed to the platform's dashboard for allowing to be used by subsequent tasks:
    - Training a ML model -> Metric Calculation -> Dev Tests -> Analysis

In this case, we're designing an API that triggers outbound HTTP events whenever specific actions occur in the the app. In this way, we can decouple notification logic from the core business flow, while keeping things fast, clean, and scalable.

Example for this API:

- A seller gets notified when a buyer places an order.

# Tech Stack

- **FastAPI**: for building the main API layer
- **httpx**: Async HTTP Clients
- **RQ queues**: for background task queueing
- **RQ workers**: for background task workers
- **Uvicorn**: ASGI server to support async operations
- **Webhooks**: for now `https://webhook.site`


# System Design

## Modular Architecture Diagram

Here is the overview system design.

![system design](/api_design/FastAPI/event_driven_notification_system/assets/Event-driven_notification_system_modular_architecture_diagram.png)

## Sequence Diagram

Here is the sequence diagram for this use-case.

![system design](/api_design/FastAPI/event_driven_notification_system/assets/Event-driven_notification_system_sequence_diagram.png)


# Project Structure:

Here is the project structure:

```markdown
event_driven_notification_system/
├─ docker-compose.yml
├─ Dockerfile
├─ .env.example
├─ requirements.txt
├─ README.md
├─ app/
│ ├─ __init__.py
│ ├─ main.py
│ ├─ core/
│ │ └─ config.py
│ ├─ schemas.py
│ ├─ db.py
│ ├─ webhooks/
│ │ ├─ dispatcher.py
│ │ └─ utils.py
│ └─ worker.py
```


# How this works:

1. FastAPI app (/order endpoint)
    - Receives an order.
    - Publishes an event (order) into the queue (Redis/RabbitMQ or simple Python queue in the minimal example).

2. Worker process
    - Consumes the event.
    - Calls fire_webhook(...) to deliver the webhook.

That function uses httpx synchronously (or with retry logic).


# How to run (Locally):

1. Create `.env` file

    ```bash
    cp .env.sample .env
    ```

2. Build the docker images

    ```bash
    cd /event_driven_notification_system
    docker compose up --build
    ```

3. Create a sample webhook by visiting `https://webhook.site` and set the token of `WEBHOOK_TARGET_URL` in `.env`.

4. Submit a job: *POST an order*

    ```bash
    curl -X POST "http://localhost:8000/order" -H "Content-Type: application/json" -d '{"order_id": 123, "user_id": 7, "amount": 49.9}'
    ```

5. Watch the worker container logs to see delivery attempts: placement of the order is notified to the seller

    - If you used webhook.site or a local receiver, you will see incoming requests.
    - Visit the `https://webhook.site/<token_id>` to see the results.


# Improvments to be done:

1. **Add persistent DB models for subscribers, delivery attempts and dead-letter queue:**

    - What: Store data about subscribers (who registered for notifications), delivery attempts (every try with status, timestamp, error), and a dead-letter queue (DLQ) (failed events after all retries).
    - Why:
        - Subscribers → persistently know who gets which event.
        - Delivery attempts → debugging, auditing, and metrics.
        - DLQ → so you don’t lose events permanently. Ops team can reprocess them later.
    - How: Use PostgreSQL/MySQL with ORM models (SQLAlchemy, Django ORM).

2. **Add rate-limiting per webhook consumer**

    - What: Ensure no single consumer gets overwhelmed (e.g., max 10 requests/second per subscriber).
    - Why: Protects downstream services from being DOS’ed.
    - How: Use Redis or token-bucket algorithm.

3. **Use structured logging (JSON) and monitoring (Prometheus, Grafana)**

    - What: Instead of free-form text logs, use structured logs (JSON). Example:

        ```bash
        { "event": "order.created", "status": "success", "delivery_time_ms": 120 }
        ```


    - Why:
        - Easier to parse with log aggregators (ELK, Loki).
        - Useful for dashboards.

    - Monitoring: Expose metrics in Prometheus format → Grafana dashboards for:
        - Delivery latency
        - Success vs. failure rates
        - Retry counts

4. **Use exponential backoff with Jitter and Circuit Breaker**

    - Exponential backoff: Wait progressively longer before retrying (e.g., 1s → 2s → 4s → 8s).

    - Jitter: Add randomness so not all workers retry at the same time (avoids “retry storm”).

    - Circuit breaker: If a consumer endpoint keeps failing, pause sending temporarily and mark it as unhealthy.

    - Why: Improves reliability and avoids hammering flaky endpoints.

5. **Use a dedicated process supervisor (systemd / k8s) and multiple worker replicas**

    - What: Use a supervisor like systemd (bare metal/VMs) or Kubernetes (cloud-native) to manage worker processes. Run multiple worker replicas.

    - Why:
        - Auto-restart on crash.
        - Scale horizontally for high throughput.
        - Zero-downtime rolling upgrades.

6. **Webhook delivery audit & re-delivery UI**
    - What: Admin dashboard/UI where you can:
        - See delivery history (per subscriber).
        - Inspect payloads & headers.
        - Retry failed deliveries (manual or automated).

    - Why: Transparency for developers integrating your webhooks.
    - Example: Stripe and GitHub both provide webhook dashboards with replay features.