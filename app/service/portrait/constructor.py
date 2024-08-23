"""
主要用于构建请求的对象和组装返回的对象

从redis中存储的数据结构主要是
{
    "field": "memory",
    "detail": [
        {
            "property": "quantitate",
            "metric": "mem.memfree",
            "cap_metric": "mem.memtotal",
            "scale": 1.0
        },
        {
            "property": "forecast",
            "metric": "usedmemory",
            "stack": "true",
            "cap_metric": "mem.memtotal",
            "scale": 1.0
        }
    ]
}
"""
from typing import List, Dict
from abc import abstractmethod
from aioredis.client import Redis
from pydantic import ValidationError

from app.service.models.configure import MetricType
from app.service.query.executor import RemoteIOExecutor, ioexecutor
from app.service.models.hbase import HbaseTemplate
from app.service.models.portrait import PortraitModel, Quantitative, CapacityForecast
from app.service.query.builder import HbaseQueryRequestBuilder
from app.service.models.configure import ServerConfigure
from app.service.container import TrendContainer
from app.config.load_config import globalAppConfigure

class ConstructorInterface:

    _remote_configure_retriever: RemoteIOExecutor = ioexecutor

    # 实现从远程拉取数据配置
    async def retrieve_configure(self, rkey: str) -> List[ServerConfigure]:
        rClient: Redis = await self._remote_configure_retriever.get_redis()
        exist = await rClient.exists(rkey)
        if not exist:
            return list()
        
        fields: Dict = await rClient.hgetall(await rClient.get(rkey))
        remote_configures: List[ServerConfigure] = list()
        if len(fields):
            for field, conf in fields.items():
                try:
                    conf_model = ServerConfigure.model_validate_json(conf)
                    remote_configures.append(conf_model)
                except ValidationError as err:
                    print(f"配置读取失败, 确认是否合理 -> {conf}")
                    continue
                
        return remote_configures
        
    async def retrieve_request_content(self, endpoint: str, group: str, starttime: int) -> List[HbaseTemplate]:
        configures: List[ServerConfigure] = await self.retrieve_configure(rkey=endpoint + ":" + group)
        return self.post_construct(endpoint, starttime, configures)
    
    @abstractmethod
    def post_construct(self,
                       endpoint: str,
                       starttime: int, 
                       configure: ServerConfigure) -> List[HbaseTemplate]:
        """ 定义对于数据请求对象的构建
        """
        raise NotImplementedError()

    @abstractmethod
    def concat_construct(self, trends: List[TrendContainer]) -> PortraitModel: # 定义返回结果
        """ 定义对于响应数据组装的构建
        """
        raise NotImplementedError()


class ServerPortraitConstructorImpl(ConstructorInterface):

    def post_construct(self, 
                       endpoint: str,
                       starttime: int, 
                       configure: List[ServerConfigure]) -> List[HbaseTemplate]:
        """ 为服务端画像构造查询请求
        """
        request_bodys: List[HbaseTemplate] = list()
        builder: HbaseQueryRequestBuilder = HbaseQueryRequestBuilder() # 共用同一个即可
        
        for serverConfig in configure:
            # 遍历不同域的指标
            field = serverConfig.field # 这个不确定是否需要
            for detail in serverConfig.detail:
                builder.add_counter(
                    endpoint = endpoint, counter = detail.counter
                )

                if detail.property == MetricType.FORECAST:
                    builder.start = starttime
                    builder.end = starttime + globalAppConfigure.futureQueryPeriod
                else:
                    builder.start = starttime - globalAppConfigure.lastQueryPeriod
                    builder.end = starttime

                request_bodys.append(builder.build())

        return request_bodys
    
    def concat_construct(self, trends: List[TrendContainer]) -> PortraitModel:
        """ 组装返回的数据结果
        """
        quantTrends: List[Quantitative] = list()
        forecastTrends: List[CapacityForecast] = list()
        
        for trend in trends:
            if trend.forecast:
                forecastTrends.append(
                    CapacityForecast.from_trend_component(trend)
                )
            else:
                quantTrends.append(
                    Quantitative.from_trend_component(trend)
                )

        return PortraitModel(
            field="total",
            quantitative=quantTrends,
            capacityForecast=forecastTrends
        )
    

class InstancePortraitConstructorImpl(ConstructorInterface):

    def post_construct(self, 
                       endpoint: str,
                       starttime: int,
                       configure: List[ServerConfigure]) -> List[HbaseTemplate]:
        return 
    
    def concat_construct(self, trends: List[TrendContainer]) -> PortraitModel:
        return 
