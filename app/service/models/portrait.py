from pydantic import BaseModel
from app.service.models.hbase import Timepoint
from app.service.container import TrendContainer
from typing import List

class CapacityReference(BaseModel):
    maxCapacityRef: float
    minCapacityRef: float

class Quantitative(BaseModel):
    metric: str
    capacityReference: CapacityReference
    last: List[Timepoint]

    @classmethod
    def from_trend_component(cls, trend: TrendContainer):
        return cls(
            metric = trend.counter,
            capacityReference = CapacityReference(
                maxCapacityRef=trend.maxCapacity,
                minCapacityRef=trend.minCapacity
            ),
            last = trend.trend[-1:]
        )


class CapacityForecast(BaseModel):
    metric: str
    values: List[Timepoint]

    @classmethod
    def from_trend_component(cls, trend: TrendContainer):
        return cls(
            metric = trend.counter,
            values = trend.trend
        )

class PortraitModel(BaseModel):
    field: str
    quantitative: List[Quantitative]
    capacityForecast: List[CapacityForecast]


    