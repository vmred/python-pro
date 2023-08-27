import asyncio
import time
from functools import wraps


def measure_exec_time(func):
    @wraps(func)
    def wrapper_sync(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds")
        return result

    @wraps(func)
    async def wrapper_async(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds")
        return result

    if asyncio.iscoroutinefunction(func):
        return wrapper_async

    return wrapper_sync


@measure_exec_time
def a():
    print('function a called')


@measure_exec_time
async def b():
    await asyncio.sleep(1)
    print('function b called')


if __name__ == '__main__':
    a()
    asyncio.run(b())
