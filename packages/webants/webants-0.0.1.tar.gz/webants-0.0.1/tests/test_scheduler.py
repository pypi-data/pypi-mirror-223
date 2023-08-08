import asyncio

import unittest

try:
    import sys

    sys.path.append(r"/")
except ImportError:
    import sys

from webants.scheduler import Scheduler
from webants.libs import Request


class TestSchedulerMethods(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.s = Scheduler(
            raw_request_queue=asyncio.Queue(),
            request_queue=asyncio.PriorityQueue(),
            log_level=10,
        )

    async def asyncTearDown(self) -> None:
        await self.s.close()

    def test_enqueue_request(self):
        urls = [
            "http://127.0.0.1:5000/get?name=1",
            "http://127.0.0.1:5000/get?name=2",
            "http://127.0.0.1:5000/get?name=3",
            "http://127.0.0.1:5000/get?name=1",
        ]
        requests = [Request(url) for url in urls]
        for r in requests:
            self.s.enqueue_request(r)
        self.assertEqual(self.s.request_queue.qsize(), 3)

    async def test_start_schedule(self):
        urls = [
            "http://127.0.0.1:5000/get?name=1",
            "http://127.0.0.1:5000/get?name=2",
            "http://127.0.0.1:5000/get?name=3",
            "http://127.0.0.1:5000/get?name=1",
        ]
        requests = [Request(url) for url in urls]
        for r in requests:
            self.s.raw_request_queue.put_nowait(r)
        self.assertEqual(self.s.raw_request_queue.qsize(), 4)

        await self.s.start_scheduler()
        self.assertEqual(self.s.raw_request_queue.qsize(), 0)
        self.assertEqual(self.s.request_queue.qsize(), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
