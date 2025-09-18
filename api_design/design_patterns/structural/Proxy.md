# Proxy Pattern



This pattern adds functionality or logic (logging, caching, authorization) to a resource without changing its interface.

- The main class is called `Real Subject`
- The client should use the **proxy** or the real subject without any code change, hence both must have the same interface
- Logging and controlling access to the real-subject are some of the proxy pattern usages.

```python
from typing import Union

# Interface
class Subject:
    """
    The interface for both RealSubject and Proxy should be same.
    So the client can use RealSubject or Proxy with no code change. 
    """

    def do_the_job(self, user: str) -> None:
        raise NotImplementedError()


# Real Subject
class RealSubject(Subject):
    """
    This is the main job doer. 
    This can be external services like payment gateways, etc
    """

    def do_the_job(self, user: str) -> None:
        print(f"I am doing the job for {user}")


# Proxy
class Proxy(Subject):
    def __init__(self) -> None:
        self._real_subject = RealSubject()

    def do_the_job(self, user: str) -> None:
        """
        Logging and controlling access are some examples of proxy usage. 
        """

        print(f"f[log] Doing the job for {user} is requested")

        if user == "admin":
            self._real_subject.do_the_job(user)
        else:
            print("[log] I can do the job just for `admin`")


# Client
def client(job_doer: Union[RealSubject, Proxy], user: str) -> None:
    job_doer.do_the_job(user)


# Running
proxy = Proxy()
real_subject = RealSubject()

client(job_doer=proxy, user="admin")
# [log] Doing the job for admin is requested.
# I am doing the job for admin

client(proxy, 'anonymous')
# [log] Doing the job for anonymous is requested.
# [log] I can do the job just for `admins`.

client(real_subject, 'anonymous')
# I am doing the job for anonymous
```