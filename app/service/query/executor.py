
"""
在一个应用程序中最好使用唯一的ClientSession保证不会频繁创建连接池, 可以创建一个单例模式，这个真得是单例，因为session得在异步中实现
由于模块化本身就是单例模式, 因此可以在项目任何地方引入这个对象来实现aiohttp客户端的使用
参考: https://blog.ibeats.top/issues/python-asyncio-run
参考: https://blog.csdn.net/lymmurrain/article/details/109037460
"""
import aiohttp
from aioredis.client import Redis
from aiohttp.connector import TCPConnector
import aiohttp.connector
from app.config.load_config import globalAppConfigure

class RemoteIOExecutor:

    _session: aiohttp.ClientSession = None
    _redisClient: Redis = None

    def __init__(self) -> None:
        pass

    async def init_http(self):
        # 如果需要多个不同的session共享同一个连接池，需要在参数中定义connector_owner=False, 这样在关闭session的时候不会把connector也一起关了(默认是会一起关闭)
        # session内部包含了连接池，建议对于同一个域名共用同一个session, 当涉及到多个请求域名的情况下可以指定多个session, 多个session也可以共享同一个连接池
        self._session = aiohttp.ClientSession(connector=TCPConnector(limit=globalAppConfigure.connector_limit))

    async def init_redis(self):
        url = f"redis://{globalAppConfigure.baseRedisNAME}:{globalAppConfigure.baseRedisPWD}@{globalAppConfigure.baseRedisURL}:{globalAppConfigure.baseRedisPORT}"
        self._redisClient = Redis.from_url(url)

    async def get_session(self):
        # 单线程模型不需要加锁
        if self._session is None:
            # 初始化session的过程必须在事件循环中
            await self.init_http()

        return self._session

    async def get_redis(self):
        if self._redisClient is None:
            await self.init_redis()
        return self._redisClient

    async def close(self):
        if self._session is not None:
            await self._session.close()

        if self._redisClient is not None:
            await self._redisClient.close()

# 单例模式
ioexecutor = RemoteIOExecutor()
