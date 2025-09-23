# Multi-processing

## 🚀 TL;DR

- **multiprocessing** lets you truly run code in parallel across CPU cores
- Key tools: `Process`, `Pool`, `Queue`, `Manager`, and synchronization primitives
- Always wrap your code in `if __name__ == "__main__":` when starting processes

## 1️⃣ What is multiprocessing

- Python’s **Global Interpreter Lock (GIL)** limits true parallelism for CPU-bound tasks in threads
    - **CPU-bound tasks**: Heavy computations (e.g., image processing, numerical simulations).

    - **I/O-bound tasks**: Waiting on disk, network, or database.

- Threads are fine for **I/O bound** tasks, but for **CPU-bound** work, we need to use **processes**

- **multiprocessing** avoids the GIL by spawning separate OS processes, each with its own Python interpreter and memory space


## 2️⃣ Core Concepts

### ✅ Process

- A Process is an independent Python interpreter
- Each process:
    - Has its own memory space
    - Runs concurrently on different CPU cores

### ✅ Communication

- Since processes do not share memory, you need:
    - Queues / Pipes: For passing messages or data
    - Managers: For sharing Python objects (lists, dicts, etc.)

### ✅ Synchronization

- To avoid race conditions when sharing resources:
    - Lock: Only one process can access a section of code at a time.
    - Event/Semaphore/Condition: Advanced coordination primitives


### ✅ Pools

`multiprocessing.Pool` manages a pool of worker processes, making it easy to parallelize a function across many inputs

## 3️⃣ Minimal Example

### Example 1

```python
from multiprocessing import Process
import os, time

def worker(name):
    print(f"Worker {name} (PID: {os.getpid()}) started")
    time.sleep(2)
    print(f"Worker {name} finished")

if __name__ == "__main__":
    p1 = Process(target=worker, args=("A",))
    p2 = Process(target=worker, args=("B",))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Main process done")


# What happens:

# - p1 and p2 run in parallel.
# - start() launches each process.
# - join() waits for them to finish.
```

### Example 2: Using a Queue for Communication

```python
from multiprocessing import Process, Queue

def square(numbers, queue):
    for n in numbers:
        queue.put(n * n)

if __name__ == "__main__":
    nums = [1, 2, 3, 4]
    q = Queue()

    p = Process(target=square, args=(nums, q))
    p.start()
    p.join()

    results = []
    while not q.empty():
        results.append(q.get())

    print("Squares:", results)
```

### Example 3: Pool – Simple Parallel Map

```python
from multiprocessing import Pool
import time

def cube(x):
    time.sleep(1)
    return x ** 3

if __name__ == "__main__":
    nums = [1, 2, 3, 4, 5]

    # Create a pool of workers
    with Pool(processes=3) as pool:  # 3 workers
        results = pool.map(cube, nums)
    print(results)

# What happens:
# `pool.map` automatically splits the list across workers
# The total runtime is about `len(nums) / processes` seconds, not the full 5 seconds
```

### Example 4: Sharing State with Manager


```python
from multiprocessing import Process, Manager

def add_numbers(shared_list):
    for i in range(5):
        shared_list.append(i)

if __name__ == "__main__":
    with Manager() as manager:
        shared_list = manager.list()  # shared, process-safe
        p1 = Process(target=add_numbers, args=(shared_list,))
        p2 = Process(target=add_numbers, args=(shared_list,))
        p1.start(); p2.start()
        p1.join(); p2.join()
        print("Shared List:", list(shared_list))
```


## 4️⃣ Best Practices

1. Guard your code with `if __name__ == "__main__":` to avoid infinite process spawning
2. Use `pool` for simple parallel mapping, `Process` for custom control
3. Avoid sharing mutable objects directly:
    - Use `Queue` or `Manager` instead
4. Balance CPU cores:
    - Don't spawn more heavy processes than cores: use `os.cpu_count()`
5. Graceful shutdown:
    - Use `terminate()` or `join()` carefully to release resources


## 5️⃣ When to Use vs. Alternatives

| Technique           | Best for                       | Avoid when                              |
| ------------------- | ------------------------------ | --------------------------------------- |
| **multiprocessing** | CPU-bound tasks                | When you need large shared state        |
| **threading**       | I/O-bound tasks                | Heavy CPU work (due to GIL)             |
| **asyncio**         | Concurrent I/O (single-thread) | Heavy CPU work                          |
| **joblib / dask**   | High-level parallelism         | When you need low-level process control |
