from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class MetricType(str, Enum):
    QUANTITATE = "quantitate"
    FORECAST = "forecast"

class MetricDetail(BaseModel):
    property: MetricType
    metric: str = Field(default="")
    cap_metric: str = Field(default="")
    scale: float = Field(default=1.0)
    stack: bool = Field(default=True)
    tags: str = Field(default="")

    @property
    def counter(self):
        counter: str = self.metric
        if len(self.tags) and self.property == MetricType.FORECAST:
            counter = counter + "/" + self.tags + ",group=Instance_capacity_pred_scp"
        
        elif len(self.tags):
            counter = counter + "/" + self.tags
        
        else:
            pass

        return counter

class ServerConfigure(BaseModel):
    field: str = Field(default="")
    detail: List[MetricDetail] = Field(default=list())