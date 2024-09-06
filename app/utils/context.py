
from contextvars import ContextVar, Token
# https://github.com/fastapi/fastapi/discussions/8628
# 参考contextvars向下兼容的版本来理解Token的含义
# https://github.com/MagicStack/contextvars/blob/master/contextvars/__init__.py
class ContextVarWrapper:

    def __init__(self, context: ContextVar) -> None:
        self._context = context

    def set(self, value) -> Token:
        # 会返回一个Token对象, Token(ctx, var, old_value)
        return self._context.set(value)

    def reset(self, token: Token):
        # 所谓reset的含义就是还原contextvar的前一个值
        self._context.reset(token)
    
    @property
    def value(self):
        return self._context.get()
    

# 全局变量
traceId = ContextVarWrapper(ContextVar("request-trace-id", default=""))