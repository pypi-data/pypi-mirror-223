from typing import Any, Callable
import uuid
import asyncio

class Executable:
    def __init__(self, name: str, func: Callable =None, timeout: int = None, max_retries: int = 0, retry_delay: int = 1, retry_cleanup: Callable = None, *args: Any, **kwargs: Any):
        self.id = uuid.uuid4()
        self.name = name
        self.func = func
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.retry_cleanup = retry_cleanup
        self.args = args
        self.kwargs = kwargs
        self.status = "NOT STARTED"
        self.failure_reason = None
        self.data = None
        self.prev = None
        self.next = None
    
    async def execute(self, *args: Any, **kwargs: Any):
        """
        Execute the function asynchronously.

        Args:
            *args (Any): Positional arguments to be passed to the function.
            **kwargs (Any): Keyword arguments to be passed to the function.

        Returns:
            Tuple[Any, str]: A tuple containing the data returned by the function and the status of the execution.

        Raises:
            Exception: If the execution fails after the maximum number of retries.
            Exception: If the execution is cancelled.
            Exception: If an error occurs during the execution.
        """
        self.status = "RUNNING"
        retries = 0
        while retries <= self.max_retries:
            try:
                if self.func:
                    if self.timeout is not None:
                        self.data = await asyncio.wait_for(self.func(*self.args, *args, **self.kwargs,**kwargs), self.timeout)
                    else:
                        self.data = await self.func(*self.args, *args, **self.kwargs,**kwargs)
                self.status = "COMPLETED"
                break
            except asyncio.TimeoutError as e:
                self.status = "FAILED"
                self.failure_reason = Exception(f"Execution of '{self.name}' exceeded timeout.")
                # print(f"Execution of '{self.name}' exceeded timeout.")
                if retries < self.max_retries:
                    if self.retry_cleanup:
                        await asyncio.wait_for(self.retry_cleanup(), None)
                    await asyncio.sleep(self.retry_delay)
                    retries += 1
                else:
                    raise self.failure_reason
            except asyncio.CancelledError as e:
                self.status = "CANCELLED"
                self.failure_reason = Exception(f"Execution of '{self.name}' cancelled.")
                raise self.failure_reason
            except Exception as e:
                self.status = "FAILED"
                self.failure_reason = e
                if retries < self.max_retries:
                    if self.retry_cleanup:
                        await asyncio.wait_for(self.retry_cleanup(), None)
                    await asyncio.sleep(self.retry_delay)
                    retries += 1
                else:
                    raise self.failure_reason
        return self.data, self.status