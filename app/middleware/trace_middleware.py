from datetime import datetime
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.utils.context import traceId
from app.utils.utils import StringUtil

class TraceIdMiddleware(BaseHTTPMiddleware):
    """ 
    参考: https://blog.csdn.net/qq_36815042/article/details/129308934
    参考: https://zhuanlan.zhihu.com/p/432010113
    """

    def __init__(self, app):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next) -> Response:
        # 添加traceid
        currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request_id = StringUtil.GenerateMd5(currentTime)
        reqJson = await request.json()
        # print(f"调用-TraceId生成-TraceLogMiddleware--before-{reqJson} - {request_id}")
        traceId.set(request_id)
        result = await call_next(request)
        # print(f"调用-TraceId生成-TraceLogMiddleware--after-{reqJson} - {request_id}")
        traceId.set("-")
        return result
