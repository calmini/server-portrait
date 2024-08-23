import uvicorn
from fastapi import FastAPI

from app import bootstrap
from app.config.load_config import globalAppConfigure
# 主要的问题在于, 如果一个项目中有两个loop要怎么管理. fastapi内部有他自己的loop, aiohttp也有自己的loop
# 所以要兼顾保证他们共用了同一个loop, 由于aiohttp内部创建clientSession的时候，用的是get_event_loop, 这就是产生问题的地方

# TODO 添加日志
# TODO 添加错误处理
# TODO 添加模型pydantic

if __name__ == "__main__":
    # 实例化
    server = FastAPI()
    # 初始化项目
    bootstrap.Init(server)
    # 使用 python main.py 启动服务
    uvicorn.run(server, host=globalAppConfigure.host, port=globalAppConfigure.port)
