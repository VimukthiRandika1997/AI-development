# Load / Performance Testing

Here we try to test API's performance under heavy load

## Key Metrics to Note:

### p95

- This is 95th percentile latency is a way to measure performance in systems, especially in ML/AI services, APIs and distributed systems

#### What it means:

- Suppose our system handles 100 requests
- We measure how long each request takes (AKA latency)
- Now sort those latencies from fastest -> slowest
- The **95th percentile (p95)** is the latency below which 95% requests fall

- In other words:
    - **p50 (median)** -> half of requests are faster, half are slower
    - **p95** -> 95% of requests are faster than this value, but 5% are slower
    - **p99** -> 99% of requests are faster than this value, but 1% are slower

#### Why it's important for ML/AI systems:

- Average (mean) latency can hide slow cases (outliers)
- Users care about worst-case experience, not just the average
- For example:
    - Average latency: *200 ms*
    - p95 latency: *800 ms* (meaning 5% of users may experience 800 ms delay)
    - This would be a critical if we're building apps, RAG systems, search, or APIs