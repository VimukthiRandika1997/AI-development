# TL;DR

- ThreadPoolExecutor is the recommended modern API for threading in Python.

- It simplifies thread management, improves readability, and reduces bugs compared to threading.Thread directly.


## 🚀 Why ThreadPoolExecutor?

- Instead of manually:
    - creating each `threading.Thread`
    - starting them
    - tracking them
    - calling `.join()`

- The `ThreadPoolExecutor` manages a pool of worker threads for us:
    - we must submit tasks (functions) to the pool
    - It handles scheduling, running, and collecting results


## 🔑 Key Features

1. Thread Pool
    - A fixed (or dynamic) number of worker threads are created once and reused.

2. submit() vs map()

    - `submit(fn, *args)`: Schedules a function to run in a thread, returns a `Future`.
    - `map(fn, iterable)`: Like the built-in `map()`, but runs each item in a separate thread.

3. Future Object

    - Represents a pending result.
    - Methods: `future.result()`, `future.done()`, `future.exception()`.

4. Automatic Cleanup
    - Using a `with` block shuts down the pool automatically.


## Examples


### Example 1: Basic Implementation

```python
from concurrent.futures import ThreadPoolExecutor
import time

def task(name):
    print(f"{name} starting")
    time.sleep(2)
    return f"{name} done"

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(task, f"Thread-{i}") for i in range(5)]

    for future in futures:
        print(future.result()) # wait for each thread's result
```

- What happens:
    - `max_workers=3` -> only 3 threads run at once, event though 5 tasks were submitted
    - The executor reuses threads as soon as thread finishes


### Example 2: Using `map()`

- A shortcut if all tasks use the same function:

```python
from concurrent.futures import ThreadPoolExecutor
import time

def square(n):
    time.sleep(1)
    return n * n

nums = [1, 2, 3, 4, 5]

with ThreadPoolExecutor() as executor:
    results = executor.map(square, nums)  # returns an iterator
    print(list(results))
```

- What happens:
    - Runs all `square()` calls in parallel (default `max_workers` is usually CPU count * 5 for I/O tasks)

### Example 3: Web scraping

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests, time

urls = [
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/2",
]

def fetch(url):
    r = requests.get(url)
    return url, r.status_code

start = time.time()
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(fetch, url) for url in urls]

    for future in as_completed(futures):
        url, status = future.result()
        print(f"{url} -> {status}")

print("Total time:", time.time() - start)
```

- Instead of creating a thread per URL manually, you just submit tasks.
- `as_completed()` yields futures as soon as they finish

## 💡 Tips & Best Practices

1. Pick the Right max_workers

    - For **I/O-bound tasks** (network calls, file I/O), use a larger number (e.g., 20–50).

    - For **CPU-bound tasks**, threads don’t help—use ProcessPoolExecutor instead.

2. Always Use `with` Context

    - Ensures clean shutdown (calls `executor.shutdown(wait=True)` automatically).

3. Use `as_completed` for Streaming Results

    - Don’t wait for all tasks; process each result as it finishes.

4. Handle Exceptions in **Futures**

    ```python
    try:
        result = future.result()
    except Exception as e:
        print("Task failed:", e)
    ```

5. Avoid Global State

    - Threads share memory, hence this prefers returning results instead of modifying global variables

## 🏁 When to Use ThreadPoolExecutor

✅ Great For:

- Web scraping / API calls
- Reading/writing many files
- Database queries

❌ Not Great For:

- Heavy computations (matrix multiplications, deep learning). Use multiprocessing instead.