from pydantic import BaseModel
from typing import List
from pydantic.fields import Field

class EndpointCounterModel(BaseModel):
    endpoint: str = Field(default="")
    counter: str = Field(default="")


class HbaseTemplate(BaseModel):
    endpoint_counters: List[EndpointCounterModel] = Field(default=list())
    start: int = Field(0)
    end: int = Field(0)
    cf: str = 'AVERAGE'
    queryType: str = 'original'

class Timepoint(BaseModel):
    timestamp: int
    value: float

class HbaseResponse(BaseModel):
    ip: str = Field(default="")
    endpoint: str = Field(default="")
    counter: str = Field(default="")
    dstype: str = Field(default="")
    step: int = Field(default="GAUGE")
    Values: List[Timepoint] = Field(default=list())