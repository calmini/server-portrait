import asyncio
import aiohttp
import time
from aiohttp import ClientSession

url = "http://localhost:8888"
data = {
    "endpoint": "xxx",
    "group": "mysql"
}

async def watcher():
    while True:
        await asyncio.sleep(1)


async def fetch_status(session: ClientSession, value, route: str):
    async with session.post(route, json={"value": value}) as response:
        content = await response.json()
        return content

async def run_client():
    watch_task = asyncio.create_task(watcher())
    start = time.perf_counter()
    async with aiohttp.ClientSession(url, headers={"X-Token": "token"}) as session:
        tasks = list()
        for i in range(10):
            tasks.append(asyncio.create_task(fetch_status(session, i, "/v1/portrait/query/server")))
        
        results = await asyncio.gather(*tasks)
        print(results)

    end = time.perf_counter()
    
    try:
        watch_task.cancel()
        print("监察任务已取消")
    except asyncio.CancelledError:
        print("监察任务取消失败")
        
    print(f"10个请求耗时 {end-start} s")


if __name__ == "__main__":
    asyncio.run(run_client())