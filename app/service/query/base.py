
from app.service.query.executor import RemoteIOExecutor, ioexecutor
from app.utils.context import traceId
from abc import abstractmethod
from typing import Optional
from asyncio import Semaphore
from app.config.load_config import globalAppConfigure

class QueryInterface:

    _executor: RemoteIOExecutor = ioexecutor
    _semphore: Semaphore = None

    def __init__(self,
                 semphore: Optional[Semaphore]=None):
        # 信号量, 用来控制单线程并发量
        semphore_limit = globalAppConfigure.max_asyncio_req_limit
        if semphore_limit > 0 and semphore is None:
            self._semphore = Semaphore(semphore_limit)

    @abstractmethod
    async def query(self):
        raise NotImplementedError()
        
    # 执行一些超时的记录
    def on_timeout(self):
        print(f"trace: {traceId.value} 存在任务执行超时")

    def on_fail(self):
        print(f"trace: {traceId.value} 存在任务执行失败")