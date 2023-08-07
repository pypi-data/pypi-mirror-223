from typing import Callable
from Executable import Executable

class Step(Executable):
    def __init__(self, name: str, func: Callable, timeout:int=None,max_retries: int = 0, retry_delay: int = 1, retry_cleanup: Callable = None, *args, **kwargs):
        super().__init__(name=name, func=func, timeout=timeout,max_retries= max_retries, retry_delay= retry_delay, retry_cleanup= retry_cleanup, *args, **kwargs)
