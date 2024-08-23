from fastapi import APIRouter
from fastapi.requests import Request
from app.utils.http_response import ResponseSuccess
from app.utils.context import traceId

router = APIRouter(prefix="/v1/portrait", tags=["注册指标路由"])

@router.get("/")
async def hello(request: Request):
    return ResponseSuccess(
        resp = "你好欢迎使用",
        trace_id = traceId.value
    )