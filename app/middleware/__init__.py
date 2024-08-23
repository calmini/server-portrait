from fastapi import FastAPI

from .token_middleware import TokenMiddleware
from .usetime_middleware import UseTimeMiddleware
from .trace_middleware import TraceIdMiddleware

# 定义注册顺序
middlewareList = [
    UseTimeMiddleware,  # 添加耗时请求中间件
    TraceIdMiddleware,  # 添加链路id中间件
    TokenMiddleware,  # 添加token验证中间件
]


def registerMiddlewareHandle(server: FastAPI):
    """ 注册中间件 """

    # 倒序中间件
    middlewareList.reverse()
    # 遍历注册
    for _middleware in middlewareList:
        server.add_middleware(_middleware)
