import sys
from typing import Any, Callable
import asyncio

from Executable import Executable
from Errors import WorkflowError

class Workflow(Executable):
    def __init__(self, name: str,timeout: int=None,max_retries: int = 0, retry_delay: int = 1, retry_cleanup: Callable = None, *args: Any, **kwargs: Any):
        super().__init__(name, func=None,timeout=timeout,max_retries= max_retries, retry_delay= retry_delay, retry_cleanup= retry_cleanup, *args, **kwargs)
        self.steps = []
        self.first_step = None
        self.last_step = None
        self.current_step = None
    
    def add(self, step: Executable):
        """
        Adds a step to the workflow.

        Parameters:
            step (Executable): The step to be added.

        Raises:
            TypeError: If `step` is not an instance of `Executable`.

        Returns:
            None
        """
        if not isinstance(step, Executable):
            raise TypeError("step must be an instance of Executable")
        
        if self.first_step is None:
            self.first_step = step
            self.last_step = step
        else:
            step.prev = self.last_step
            self.last_step.next = step
            self.last_step = step
        self.steps.append(step)
    
    async def execute(self, *args: Any, **kwargs: Any):
        """
        Executes the workflow asynchronously.

        Args:
            *args (Any): Variable length argument list.
            **kwargs (Any): Arbitrary keyword arguments.

        Returns:
            Tuple[Any, str]: A tuple containing the updated data and the status of the workflow.
        """
        self.status = "RUNNING"
        retries = 0
        while retries <= self.max_retries:
            try:
                self.current_step = self.first_step
                while self.current_step is not None:
                    if self.current_step.status != "COMPLETED":
                        self.data, _ = await self.current_step.execute(self.data, *self.args, *args, **self.kwargs,**kwargs)
                        
                        if self.current_step.status !="COMPLETED":
                            raise Exception(self.current_step.failure_reason)

                    self.current_step = self.current_step.next
                self.status = "COMPLETED"
                break
            except Exception as e:
                self.status = "FAILED"
                self.failure_reason = WorkflowError(f"Workflow '{self.name}' failed at step: '{self.current_step.name}', reason: {str(e)}")
                # print(f"Workflow '{self.name}' failed at step: '{self.current_step.name}', reason: {str(e)}")
                if retries < self.max_retries:
                    if self.retry_cleanup:
                        await asyncio.wait_for(self.retry_cleanup(), None)
                    await asyncio.sleep(self.retry_delay)
                    retries += 1
                else:
                    raise self.failure_reason
        return self.data, self.status
