
from app.service.query.base import QueryInterface
from app.service.models.hbase import HbaseTemplate
from app.utils.wrapper import Wrapper
from app.service.container import TrendContainer
from app.config.load_config import globalAppConfigure
from app.utils.context import traceId
from typing import List
from asyncio import Semaphore
from typing import Optional

import asyncio

class HbaseQueryImpl(QueryInterface):

    def __init__(self, 
                 semphore: Optional[Semaphore]=None,
                 timeout: Optional[int] = None):
        super().__init__(semphore)
        self.timeout = timeout
        

    async def query_one(self, reqTemplate: HbaseTemplate):
        # 如果超出控制的并发量, 会阻塞在这里, 从而降低对服务端的影响
        async with self._semphore:
            session = await self._executor.get_session()
            with session.post(globalAppConfigure.baseHbaseURL, json = reqTemplate.model_dump()) as job:
                reqJson = await job.json()
                return reqJson

    # 重写抽象方法
    async def query(self, reqCollections: List[HbaseTemplate]) -> List:
        if self.timeout is not None:
            wrapped_tasks = [
                Wrapper.timeoutWrapper(self.query_one(req), timeout=self.timeout) for req in reqCollections
            ]
        else:
            wrapped_tasks = [
                Wrapper.asyncWrapper(self.query_one(req)) for req in reqCollections
            ]
        
        numPendingTasks = len(wrapped_tasks)
        trends: List[TrendContainer] = list()
        # 执行异步请求, 使用as_completed的缺点在于不知道哪些任务超时了, 更合理的方式是使用wait或者gather
        # 然而使用wait/gather的不足的地方在于必须等待所有io都执行完毕后才能执行后续逻辑
        for task in asyncio.as_completed(wrapped_tasks):
            try:
                retJson = await task
                # 数据解析可以放在这里
                if len(retJson):
                    trends.extend(
                        [TrendContainer.from_dict(ret) for ret in retJson]
                    )
                numPendingTasks -= 1
            except asyncio.exceptions.TimeoutError as err:
                # 执行超时操作
                self.on_timeout()
            except Exception as err:
                # 执行失败操作
                self.on_fail()
            
        
        # 检查是否存在任务超时或者被取消了
        if numPendingTasks > 0:
            print(f"trace: {traceId.value} 存在 {numPendingTasks} 个任务执行超时或失败")
            
        return list(filter(lambda x: not x.empty, trends))

    
