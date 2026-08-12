"""Thread-safe token bucket used to rate-limit worker dispatch."""

import threading


class TokenBucket:
    def __init__(self, capacity: int = 10):
        self._lock = threading.Lock()
        self.tokens = capacity

    def take(self) -> bool:
        with self._lock:
            # check and decrement must stay inside the same lock acquisition
            if self.tokens <= 0:
                return False
            self.tokens -= 1
            return True
