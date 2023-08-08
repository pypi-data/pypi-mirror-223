import unittest
from pathlib import Path
from urllib.parse import urlparse

import aiohttp
import requests

from webants.libs import Response, Request
from webants.utils.login import sync_login_with_playwright, load_cookies


class TestLoginMethods(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.url = "http://108.170.5.99/thread-8089886-1-1.html"
        # self.url = https://dl.reg.163.com/webzj/v1.0.1/pub/index_dl2_new.html?cd=
        # https://d.163.com&cf=/static/styles/urs.css&MGID=1666435314281.6343&wdaId=&pkid=SuaKwhM&product=cainscorner

    async def test_aiohttp_load_cookies(self):
        async with aiohttp.ClientSession() as session:
            async with session.request(
                "Get", self.url, cookies=load_cookies(data_path="data/108.170.5.99")
            ) as r:
                resp = await Response.build(r, Request(self.url))
                print(resp.text)
                self.assertEqual(resp.status_code, 200)
                self.assertIn("距離下一級還需", resp.text)

    async def test_async_login(self):
        # self.async_headers = await async_login_with_playwright(data_path='data/async')
        cookies = load_cookies(data_path="data/async/")
        self.assertIs(cookies, None)

    def test_login_163(self):
        headers = sync_login_with_playwright(
            login_url="https://d.163.com/",
            login_frame_index=-1,
            css_login_frame="a:has-text('登录')",
            css_username='[placeholder="请输入邮箱地址"]',
            username="wosuifeng@163.com",
            css_password='input[name="password"]',
            password="fengqm@163",
            css_login_check="text=我同意 《凯恩之角用户协议》 和 《凯恩之角隐私政策》 >> input[type='checkbox']",
            css_login_button="text=登 录",
            data_path=r"E:\Code\Python\WebCrawler\pygather\data\sync",
        )

        headers.update({"Accept-Encoding": "gzip, deflate"})
        resp = requests.get("https://d.163.com/", headers=headers)

        self.assertIs(resp.status_code, 200)
        self.assertIn("注销", resp.text)

    def test_requests_load_cookies(self):
        resp = requests.get(self.url, cookies=load_cookies())
        self.assertEqual(resp.status_code, 200)
        self.assertIn("距離下一級還需", resp.text)

    def test_sync_login(self):
        self.sync_headers = sync_login_with_playwright(
            login_url="http://108.170.5.99/forum.php",
            login_frame_index=0,
            css_login_frame="",
            css_username="input[name='username']",
            username="bscode",
            css_password="input[name='password']",
            password="F5KKegPQ%2Bn3xTD",
            css_login_check='input[name="cookietime"]',
            css_login_button='button:has-text("登錄")',
            data_path=Path("../../data"),
        )
        data_path = (
            Path(r"E:\Code\Python\WebCrawler\pygather\data\sync")
            / urlparse(self.url).netloc
        )
        cookies = load_cookies(data_path=data_path)
        self.assertIsInstance(cookies, dict)
        self.assertIn("PHPSESSID", cookies.keys())


if __name__ == "__main__":
    unittest.main()
