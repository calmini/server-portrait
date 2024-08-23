import asyncio

class Wrapper:

    @staticmethod
    def timeoutWrapper(coro, timeout):
        # 超时的协程会自动取消
        return asyncio.wait_for(coro, timeout=timeout)
    
    @staticmethod
    def asyncWrapper(coro) -> asyncio.Task:
        return asyncio.create_task(coro)