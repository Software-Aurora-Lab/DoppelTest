from concurrent.futures import thread
import threading


class ThreadSafeVariable:

    def __init__(self, value) -> None:
        self.value = value
        self.lock = threading.Lock()

    def set(self, new_value):
        self.lock.acquire()
        self.value = new_value
        self.lock.release()

    def get(self):
        self.lock.acquire()
        result = self.value
        self.lock.release()
        return result
