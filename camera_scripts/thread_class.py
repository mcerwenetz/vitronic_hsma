from collections.abc import Callable
from threading import Thread
from typing import Any, Iterable, Mapping

class worker_Thread(Thread):

    def __init__(self,target) -> None:
        Thread.__init__(self,target)
        self.target = target
        self.result = None
    def run(self):
        self.result = self.target()

