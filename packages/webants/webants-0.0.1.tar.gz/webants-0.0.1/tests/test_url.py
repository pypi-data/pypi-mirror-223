import unittest

from webants.utils.url import *


class TestSchedulerMethods(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.url1 = (
            "http://feng@baidu.com:123@108.170.5.99:80/forum.php?mod=forumdisplay&fid=30&filter=author"
            "&orderby=dateline"
        )
        self.url2 = "https://feng:123@108.170.5.99:443/forum.php"
        self.url3 = "http://feng:123@108.170.5.99:8080/forum.php"
        self.url4 = "https://docs.python.org/zh-cn/3.10/library/abc.html#module-abc"
        self.img_url = "http://bi-si888.xyz/data/attachment/forum/202011/12/160030e9l3s5w5n5x5lnln.jpg"

    def test_lenient_host(self):
        self.assertEqual("baiducom", lenient_host("www.baidu.com"))
        self.assertEqual("108.170.5.99", lenient_host("108.170.5.99"))

    def test_normalize_url(self):
        self.assertEqual(
            normalize_url(self.url1),
            "http://108.170.5.99/forum.php?fid=30&filter=author&mod=forumdisplay&orderby=dateline",
        )
        self.assertEqual(
            normalize_url(self.url2, keep_auth=True),
            "https://feng:123@108.170.5.99/forum.php",
        )
        self.assertNotEqual(
            normalize_url(self.url1, keep_default_port=True),
            "http://108.170.5.99/forum.php?fid=30&filter=author&mod=forumdisplay&orderby=dateline",
        )

        self.assertEqual(normalize_url(self.url3, keep_auth=True), self.url3)

        self.assertNotEqual(normalize_url(self.url4), self.url4)
        self.assertEqual(normalize_url(self.url4, keep_fragments=True), self.url4)
        self.assertEqual(
            normalize_url(
                self.url1,
                keep_auth=True,
                keep_default_port=True,
                keep_blank_values=True,
                keep_fragments=True,
                sort_query=False,
            ),
            self.url1,
        )

    def test_url_fingerprint(self):
        self.assertEqual(
            url_fingerprint(self.img_url), "a5e702c710e410ff30cf1c4b797d5d0d8820da07"
        )
        self.assertEqual(
            url_fingerprint(self.img_url, new_host="108.170.5.99"),
            url_fingerprint(url_with_host(self.img_url, "108.170.5.99")),
        )

    def test_url_fp_to_filename(self):
        self.assertEqual(
            url_fp_to_filename(self.img_url, algorithm_name="md5", suffix="jpeg"),
            "3bc991a749301f4868b51617a20ccda1.jpeg",
        )

    def test_url_to_path(self):
        self.assertEqual(
            url_to_path("file:///E:/Code/Python/WebCrawler/hkpic/html"),
            "E:/Code/Python/WebCrawler/hkpic/html",
        )
        self.assertEqual(
            url_to_path("https://docs.python.org/zh-cn/3.11/library/pathlib.html"),
            "zh-cn/3.11/library/pathlib.html",
        )

    def test_url_with_host(self):
        self.assertEqual(
            url_with_host(
                self.url1,
                "bscdn.xyz",
                key=[
                    "hk-bici.com",
                    "bi-si888.xyz",
                ],
            ),
            self.url1,
        )

        self.assertEqual(url_with_host(self.url1, new_host=None), self.url1)


if __name__ == "__main__":
    unittest.main()
