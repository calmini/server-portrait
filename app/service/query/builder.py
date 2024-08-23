from app.service.models.hbase import HbaseTemplate, EndpointCounterModel

class HbaseQueryRequestBuilder:

    _template: HbaseTemplate

    def __init__(self, ):
        self.reset()

    def reset(self):
        self._template = HbaseTemplate()
    
    def add_counter(self, endpoint: str, counter: str):
        if self._template.endpoint_counters is None:
            self._template.endpoint_counters = list()
        
        self._template.endpoint_counters.append(
            EndpointCounterModel(endpoint=endpoint, counter=counter)
        )
    
    @property
    def start(self):
        return self._template.start
    
    @start.setter
    def start(self, start):
        if self.end > 0:
            assert start < self.end, "查询起始时间请小于终止时间"
        
        self._template.start = start
    
    @property
    def end(self):
        return self._template.end
    
    @end.setter
    def end(self, end):
        if self.start > 0:
            assert end > self.start, "查询终止时间请大于起始时间"
        
        self._template.end = end

    def build(self) -> HbaseTemplate:
        template = self._template
        self.reset()
        return template