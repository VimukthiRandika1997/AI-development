import time
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Global HTTPBearer instance
security = HTTPBearer(auto_error=True)  # This sets up HTTP Bearer authentication, raising errors automatically if auth is missing or invalid.

class APIKeyAuth:
    """API key authentication"""

    def __init__(self, api_key):
        self.api_key = api_key  # Save the valid API key on initialization.


    def __call__(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        # This makes the class instance callable, so it can be used as a dependency in FastAPI routes.
        # `credentials` is provided by the HTTPBearer security dependency.
        if not credentials or credentials.credentials != self.api_key:
            # If no credentials were provided or they do not match the stored API key,
            # raise an HTTP 401 Unauthorized exception with a detailed JSON error message.
            raise HTTPException(
                status_code=401,
                detail={
                    "success": False,
                    "error": "Invalid or missing API Key",
                    "error_code": "UNAUTHORIZED"
                }
            )
        return credentials.credentials  # If authentication passes, return the API key string.



class RateLimiter:
    """In-memory rate limiter"""

    def __init__(self, max_requests: int = 50, window_seconds: int = 10):
        self.max_requests = max_requests
        self.window_seconds = window_seconds # defines the time window size in seconds.
        self.requests = {} # stores for each client IP a list of timestamps of their recent requests.


    def is_allowed(self, client_ip: str) -> bool:
        """Check if a client identified by client_ip is allowed to make a new request at the current time."""

        now = time.time()

        # Clean old entries
        cutoff = now - self.window_seconds
        self.requests = {
            ip: timestamps for ip, timestamps in self.requests.items() if any(t > cutoff for t in timestamps)
        }

        # Filter timestamps for the current IP
        if client_ip in self.requests:
            self.requests[client_ip] = [t for t in self.requests[client_ip] if t > cutoff]
        else:
            self.requests[client_ip] = [] # a new client
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.max_requests:
            return False

        # Add current request
        self.requests[client_ip].append(now)

        return True