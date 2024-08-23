from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from app.utils.utils import StringUtil


class Additional(BaseModel):
    """额外信息"""
    time: str = Field(default="")
    trace_id: str = Field(default="")


class HttpResponse(BaseModel):
    """http统一响应"""
    code: int = Field(default=200)  # 响应码
    msg: str = Field(default="查询成功")  # 响应信息
    data: Any = None  # 具体数据
    additional: Additional = None  # 额外信息


def ResponseSuccess(resp: Any, trace_id: Optional[str] = None) -> HttpResponse:
    """成功响应"""
    currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return HttpResponse(
        data=resp,
        additional=Additional(
            trace_id=trace_id if trace_id is not None else StringUtil.GenerateMd5(currentTime),
        ))


def ResponseFail(msg: str, code: int = -1, trace_id: Optional[str] = None) -> HttpResponse:
    """响应失败"""
    return HttpResponse(
        code=code,
        msg=msg,
        additional=Additional(
            trace_id=trace_id if trace_id is not None else StringUtil.GenerateMd5(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ))
