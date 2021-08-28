from typing import TypeVar, Generic, Callable, Optional
from time import time

T = TypeVar('T')

class Cached(Generic[T]):
    action: Callable[[], T]
    lifetime: float
    timestamp: Optional[float] = None
    value: Optional[T] = None
    locked = False

    def __init__(self, action: Callable[[], T], lifetime = 1):
        self.action = action
        self.lifetime = lifetime

    def get(self) -> T:
        if self.locked: return self.value
        if not self.timestamp or time() - self.timestamp > self.lifetime:
            self.locked = True
            self.value = self.action()
            self.timestamp = time()
            self.locked = False
        return self.value
