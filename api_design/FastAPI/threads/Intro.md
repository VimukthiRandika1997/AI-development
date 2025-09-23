# Threads 

## 🚀 TL;DR

- Threads let us run multiple tasks at the same time within a single process.
- These are suitable for **I/O bound tasks** where that spends a lot of time waiting: network requests, file I/O or database queries
- Avoid threads for CPU-heavy work: use `multiprocessing` instead
- Protect shared resources with **locks** or use thread-safe structures like `queue.Queue`


## 1️⃣ Core Concepts

### 1. Thread vs Process

| Feature           | Thread                           | Process                             |
| ----------------- | -------------------------------- | ----------------------------------- |
| Memory            | Shares memory with main program  | Has its own memory space            |
| Creation overhead | Light                            | Heavier                             |
| Best for          | I/O-bound tasks (waiting on I/O) | CPU-bound tasks (heavy computation) |

- Threads share the **same memory space**, which makes the communcation easy but requires careful handling to avoid race conditions.


### 2. The Global Interpreter Lock (GIL)

- Python's GIL allows **only one thread** to execute Python bytecode at a time
- This means **threads won't spead up CPU-heavy tasks**: image-processing, math calculations

- But threads are great for **I/O heavy tasks**: network requests, file reads/writes


### 3. Thread Safety & Synchornization

Because threads share memory, we must prevent conflicts:

- **Lock / RLock**: ensures only one thread can access a shared resources at a time
- **Semaphore**: limits access to a resource by a fixed number of threads
- **Event**: lets threads wait for a signal
- **Queue**: threads-safe way to share data between threads

## 2️⃣ Minimal Examples

### Example 1: Creating threads

```python
import threading
import time

def worker(name):
    print(f"{name} starting")
    time.sleep(2)
    print(f"{name} done")


# Create threads
t1 = threading.Thread(target=worker, args=("Thread-1"))
t2 = threading.Thread(target=worker, args=("Thread-2"))

# Start threads
t1.start()
t2.start()

# Wait for threads to finish
t1.join()
t2.join()

print("All threads finished")


# Output:

# Thread-1 starting
# Thread-2 starting
# Thread-1 done
# Thread-2 done
# All threads finished.

```

- In here, all threads run concurrently: while one is sleeping, the other can work


### Example 2:  Thread with Locks (Avoiding Race Condition)

- Suppose two threads update the same global variable

```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        with lock:          # Ensures only one thread changes counter at a time
            counter += 1


t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)

t1.start()
t2.start()
t1.join()
t2.join()

print("Counter:", counter)   # Expected output: 200000
```

- Without the lock, the result might be less than 200000 because of race conditions

### Example 3: I/O bound Task (Web Request)

```python
import threading
import requests
import time

urls = [
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/2",
]

def fetch(url):
    r = requests.get(url)
    print(f"{url} -> {r.status_code}")

start = time.time()

threads = []
for url in urls:
    # Creating threads
    t = threading.Thread(target=fetch, args=(url,))
    # Starting threads
    t.start()
    threads.append(t)

# Wait for threads to finish
for t in threads:
    t.join()

print("Total time:", time.time() - start)
```

- Each request sleeps 2 seconds on the server side
- Without threads, total time ~6 seconds
- With threads, totatl time ~2 seconds due to concurrent downloads