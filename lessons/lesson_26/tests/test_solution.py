import asyncio

from solution import a, b


class TestSolution:
    def test_sync(self):
        a()

    def test_async(self):
        asyncio.run(b())
