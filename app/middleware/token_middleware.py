from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.utils.context import traceId
from app.utils.http_response import ResponseFail


class TokenMiddleware(BaseHTTPMiddleware):
    """ token验证中间件 """

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        # print("调用-token验证中间件-TokenMiddleware---before")
        token = request.headers.get("X-Token", "")
        if not len(token):
            return ResponseFail(msg="缺失Token信息", code=-1, trace_id=traceId.value)
        
        result = await call_next(request)
        # print("调用-token验证中间件-TokenMiddleware---after", token)
        return result
