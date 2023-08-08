import asyncio
import random
import sys
import time
import unittest
from pathlib import Path

for parent in Path(__file__).parents:
    sys.path.append(str(parent))
print(sys.path)

from webants.downloader import Downloader
from webants.libs import Request, Response


class TestDownloaderMethods(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.httpbin = "http://127.0.0.1:5000"
        # from httpbin import app
        # app.run(host='127.0.0.1',
        #         port=5000)
        self.max_size = 100
        time.sleep(1)
        q = asyncio.PriorityQueue()
        r_q = asyncio.Queue()
        self.dl = Downloader(
            request_queue=q, response_queue=r_q, log_level=10, concurrency=50, delay=0
        )
        # with open('../data/urls.txt', 'r', encoding='utf-8') as f:
        #     self.urls = f.readlines()

    async def asyncTearDown(self) -> None:
        await self.dl.close()

    def enqueue(self, request_queue):
        index = 0
        while index < self.max_size:
            r = Request(url=f"http://127.0.0.1:5000/get?name={index}")
            r.priority = random.randint(0, self.dl.concurrency)
            request_queue.put_nowait((r.priority, r))
            index += 1
        print(request_queue)

    async def fetch(self, url):
        resp = await self.dl.fetch(Request(url))
        return resp

    async def test_10_downloader_ok(self):
        resp = await self.fetch(f"http://127.0.0.1:5000/get?name=1")
        self.assertTrue(resp.ok)
        self.assertIsInstance(resp, Response)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.text, str)
        self.assertIsInstance(resp.json, dict)

    async def test_20_downloader_html(self):
        resp = await self.fetch("http://127.0.0.1:5000/html")
        self.assertIn("h1", resp.text)
        self.assertEqual(str(resp.url), "http://127.0.0.1:5000/html")

    async def test_30_downloader_xml(self):
        resp = await self.fetch("http://127.0.0.1:5000/xml")
        self.assertIn("item", resp.text)

    async def test_40_downloader_gzip(self):
        resp = await self.fetch("http://127.0.0.1:5000/gzip")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("gzipped", resp.text)

    async def test_50_downloader_deflate(self):
        resp = await self.fetch("http://127.0.0.1:5000/deflate")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("deflated", resp.text)

    async def test_60_downloader_not_ok(self):
        resp = await self.fetch("http://127.0.0.1:5000/status/400")
        self.assertFalse(resp.ok)
        self.assertFalse(resp)
        resp = await self.fetch("http://127.0.0.1:5000/status/500")
        self.assertFalse(resp.ok)
        self.assertFalse(resp)
        resp = await self.fetch("http://127.0.0.1:5000/status/600")
        self.assertFalse(resp.ok)
        self.assertFalse(resp)

    async def test_70_downloader_retry(self):
        await self.fetch("https://www.google.com")
        with self.assertRaises(TimeoutError) as cm:
            raise TimeoutError(cm)
        self.assertEqual(self.dl.request_queue.qsize(), 0)

    async def test_method_start_downloader(self):
        while True:
            try:
                self.dl.response_queue.get_nowait()
            except asyncio.QueueEmpty:
                break
        self.enqueue(self.dl.request_queue)
        tasks = [asyncio.create_task(self.dl.start_downloader())]
        await asyncio.gather(*tasks)
        self.assertEqual(self.dl.response_queue.qsize(), self.max_size)
        self.assertEqual(self.dl.request_queue.qsize(), 0)


if __name__ == "__main__":
    unittest.main(verbosity=3)
