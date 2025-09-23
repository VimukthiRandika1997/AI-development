# Asynchronous Programming

This is the Non-blocking approach to run processes

## 1️⃣ Why asyncio?

- Normally, Python code runs synchronously (each line waits until the previous one finishes)
- For tasks like:

    - **I/O-bound operations** (network requests, database queries, file reads/writes)
    - **High-concurrency servers** (web APIs, chat servers)

- It would be wasteful to block the CPU while waiting for these external tasks to be finished
- The Python `asyncio` lets us do other work while waiting


## 2️⃣ Core Concepts


| Concept        | What it is                                                                                           | Example                               |
| -------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------- |
| **Event Loop** | The "orchestra conductor" that schedules and runs asynchronous tasks.                                | `asyncio.run(main())` starts it.      |
| **Coroutine**  | A special function declared with `async def`. It can `await` other coroutines.                       | `async def fetch(): ...`              |
| **Task**       | A coroutine wrapped to run concurrently.                                                             | `task = asyncio.create_task(fetch())` |
| **await**      | Keyword to pause until another coroutine finishes, without blocking the loop.                        | `data = await fetch()`                |
| **Future**     | Low-level object representing a result that will be set later. Usually handled for you by `asyncio`. |                                       |


## 3️⃣ Minimal Example

```python
import asyncio

async def say_hello():
    await asyncio.sleep(1)          # Non-blocking sleep
    print("Hello")

async def say_world():
    await asyncio.sleep(2)
    print("World")

async def main():
    # Run both coroutines concurrently
    task1 = asyncio.create_task(say_hello())
    task2 = asyncio.create_task(say_world())

    await task1
    await task2

asyncio.run(main())

# Output:
#   - Hello
#   - World

# `Hello` prints first because its sleep is shorter
```


## 4️⃣ Common Patterns

### Run many tasks

```python
results = await asyncio.gather(coro1(), coro2(), coro3())
```

### Timeouts

```python
try:
    await asyncio.wait_for(fetch_data(), timeout=5)
except asyncio.TimeoutError:
    print("Took too long!")
```

### Queues (Producer–Consumer)

```python
queue = asyncio.Queue()
await queue.put(item)
item = await queue.get()
```

## 5️⃣ When to Use asyncio

✅ Best for I/O-bound tasks:

- Web servers (FastAPI, aiohttp)
- Bots, crawlers, microservices
- Handling thousands of sockets

❌ Not ideal for CPU-bound tasks:

- Heavy computation (use multiprocessing or threads instead)


## 🚀 FastAPI Example

```python
# main.py
from fastapi import FastAPI
import asyncio
from datetime import datetime

app = FastAPI()


async def slow_task(name: str, delay: int) -> str:
    """
    Simulate a slow I/O operation.
    """
    await asyncio.sleep(delay)  # non-blocking sleep
    return f"{datetime.now().isoformat()} → Task {name} finished after {delay}s"


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI with asyncio!"}


@app.get("/concurrent")
async def run_concurrent():
    """
    Run multiple async tasks at the same time and gather results.
    """
    task1 = asyncio.create_task(slow_task("A", 2))
    task2 = asyncio.create_task(slow_task("B", 3))
    task3 = asyncio.create_task(slow_task("C", 1))

    # Gather waits for all tasks concurrently
    results = await asyncio.gather(task1, task2, task3)
    return {"results": results}

```

```bash
## How to run
# 1. Install dependencies
pip3 install fastapi uvicorn
# 2. Start the server
uvicorn main.app --reload
# 3. Visit in browser or curl
http://127.0.0.1:8000/ -> basic hello
http://127.0.0.1:8000/concurrent -> runs 3 tasks at the same time
```

### 💡 What’s Happening

- `slow_task` is an **async coroutine** that simulates I/O with await `asyncio.sleep`.
- `/concurrent` endpoint creates three tasks with different delays and `awaits` them concurrently.
- Total response time ≈ **max(delay)** (about 3 s) rather than sum (2 + 3 + 1 = 6 s).