
from contextvars import ContextVar

# https://github.com/fastapi/fastapi/discussions/8628
class ContextVarWrapper:

    def __init__(self, context: ContextVar) -> None:
        self._context = context

    def set(self, value):
        self._context.set(value)

    def reset(self, value):
        self._context.reset(value)
    
    @property
    def value(self):
        return self._context.get()
    

# 全局变量
traceId = ContextVarWrapper(ContextVar("request-trace-id", default=""))