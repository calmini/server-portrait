# 数据容器
from typing import List, Dict, Callable
import numpy as np

class CapacityMixin:

    _maxCap: float = None
    _minCap: float = None

    def _extract(self, extract_func: Callable):
        raw = [x["value"] for x in self.trend]
        return extract_func(raw)

    @property
    def maxCapacity(self):
        if self._maxCap is None:
            # 设置
            self._maxCap = float(self._extract(np.max))

        return self._maxCap 
    
    @maxCapacity.setter
    def maxCapacity(self, value):
        raise ValueError("不能设置最大值")

    @property
    def minCapacity(self):
        if self._minCap is None:
            # 设置
            self._minCap = float(self._extract(np.min))

        return self._minCap

    @minCapacity.setter
    def minCapacity(self, value):
        raise ValueError("不能设置最小值")


class TrendContainer(CapacityMixin):

    def __init__(self, 
                 trend: List[Dict[str, float]],
                 is_forecast: bool,
                 meta: Dict[str, str]):
        # 不对外暴露属性, 通过给定的api访问具体的数据
        self.trend = trend
        self._is_forecast = is_forecast
        self._meta = meta

    @property
    def endpoint(self):
        return self._meta.get("endpoint", "")

    @property
    def counter(self):
        return self._meta.get("counter", "")
    
    @property
    def ip(self):
        return self._meta.get("ip", "")
    
    @property
    def forecast(self):
        return self._is_forecast
    
    @property
    def empty(self):
        return len(self.trend) == 0

    @classmethod
    def from_dict(cls, data: Dict) -> "TrendContainer":
        forecast = "hubble-cp" in data["endpoint"]
        trend = data.pop("Values")
        return cls(
            trend = trend,
            is_forecast = forecast,
            meta = data
        )
