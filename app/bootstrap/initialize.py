from fastapi import FastAPI
from app.controller import RegisterRouterList
from app import middleware

def Init(server: FastAPI):
    """ 初始化项目"""
    # 挂载静态资源目录
    # server.mount("/static", StaticFiles(directory="static"), name="static")

    # 注册自定义错误处理器 TODO
    #errors.registerCustomErrorHandle(server)
    # 注册中间件
    middleware.registerMiddlewareHandle(server)
    # 加载路由
    #for item in RegisterRouterList:
    #    server.include_router(item.router)
    for item in RegisterRouterList:
        server.include_router(item.router)