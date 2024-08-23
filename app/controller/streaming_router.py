import json
import time
from typing import List
from fastapi import APIRouter
from fastapi.responses import Response
from fastapi.requests import Request
from app.utils.context import traceId
from app.service.portrait.constructor import ServerPortraitConstructorImpl
from app.service.container import TrendContainer
from app.service.models.hbase import HbaseTemplate
from app.service.models.portrait import PortraitModel
from app.service.query.hbase import HbaseQueryImpl
from app.utils.http_response import ResponseFail, ResponseSuccess


router = APIRouter(prefix="/v1/portrait/query",tags=["实时数据获取"])

@router.post("/server")
async def query_server(request: Request):
    inputBody = await request.json()
    serverConstructor = ServerPortraitConstructorImpl()
    # 构建查询对象
    hbaseRequestContents: List[HbaseTemplate] = await serverConstructor.retrieve_request_content(
        endpoint = inputBody["endpoint"],  group=inputBody["group"], starttime=int(time.time())
    )
    if not len(hbaseRequestContents):
        return ResponseFail(
            msg = "没有取到已注册的配置信息",
            code = -1,
            trace_id = traceId.value
        )
    
    # 执行查询请求
    hbaseQueryImpl: HbaseQueryImpl = HbaseQueryImpl()
    trends: List[TrendContainer] = await hbaseQueryImpl.query(hbaseRequestContents) # 异步查询
    if not len(trends):
        return ResponseFail(
            msg = "没有取到数据, 服务端可能存在一些问题",
            code = -1,
            trace_id=traceId.value
        )

    # 组装查询结果
    portrait: PortraitModel = serverConstructor.concat_construct(trends)
    return ResponseSuccess(
        resp = portrait.model_dump(),
        trace_id=traceId.value
    )

@router.post("/instance")
async def query_instance(request: Request):
    print(f"当前的request-id是{traceId.value}")
    # content = await qexecutor.query_baidu()
    reqJson = await request.json()
    return Response(content=json.dumps({
         "content": reqJson,
         "trace-id": traceId.value
     }))
    pass