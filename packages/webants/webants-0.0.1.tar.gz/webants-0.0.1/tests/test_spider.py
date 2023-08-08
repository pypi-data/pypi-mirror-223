import json
import re
import tracemalloc
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from webants.libs import Result, Response, Link, LinkItem, TextItem, LinkItemDescriptor
from webants.parser import Parser
from webants.spider import Spider
from webants.utils import load_cookies, valid_path

recoder = []


class MyParser(Parser):
    thread = LinkItemDescriptor(
        attr="href",
        selector="td.icn a:not([title^=全局])",  # th a[href$=html] a.xst
        # xpath='//a[@class]',
        base_url="http://108.170.5.99",
        regexps_allow=[r"/thread-\d+?-1-\d+\.h", r"/forum-18-\d+", r"/forum.php\?.+"],
        hosts_allow=[
            "108.170.5.99",
        ],
        log_level=20,
        link_process_func=lambda link: Link(
            url=re.sub(r"/thread-(\d+)-1-\d+", r"/thread-\g<1>-1-1", link.url),
            unique=link.unique,
        ),
    )

    # forum = LinkItem(attr='href',
    #                  selector='div.pg a',  # th a[href$=html],
    #                  # xpath='//a[@class]',
    #                  base_url='http://108.170.5.99',
    #                  regexps_allow=[r'/thread-\d+-1-1\.', r'/forum-18-\d+', r'/forum.php\?.+'],
    #                  hosts_allow=['108.170.5.99', ],
    #                  log_level=20,)

    image = LinkItem(
        hosts_allow=[
            "108.170.5.99",
        ],
        selector="img[file]",
        attr="file",
        base_url="http://108.170.5.99",
        regexps_deny=["/static/image/.+$"],
        link_process_func=lambda link: link.remove_suffix(".thumb.jpg"),
    )

    title = TextItem(selector="title", many=False)

    # text = TextItem(selector='td.t_f')

    def process_response(self, response: Response) -> Response:
        print("\n[Response]")
        if "thread" in response.url:
            parts = urlparse(response.url)
            _path = self.work_dir / Path(parts.netloc) / valid_path(response.title)
            _path.mkdir(parents=True, exist_ok=True)
            if "tid" in parts.query:
                tid = parse_qs(parts.query).get("tid", [])[0]
                filename = f"thread-{tid}-1-1.html"
            else:
                filename = Path(parts.path).name
            _path /= filename
            print(_path)
            _path.write_text(response.text, encoding=response.encoding)

        recoder.append(f"{response} from '{response.request.cb_kwargs.get('title')}'")
        return response


class HKPicSpider(Spider):
    # 处理动态页面时，即http://108.170.5.99/forum.php?mod=forumdisplay&fid=18&filter=author&orderby=dateline，
    # 这样的链接时存在问题，后续需要处理
    # "file:///E:/Code/Python/WebCrawler/hkpic/html"
    # 'http://108.170.5.99/forum-18-1.html',
    start_urls = [
        # "file:///E:/Code/Python/WebCrawler/hkpic/html",
        # 'http://108.170.5.99/forum-18-1.html',
        # 'http://108.170.5.99/thread-8133704-1-1.html',
        "http://108.170.5.99/forum.php?mod=forumdisplay&fid=294&filter=author&orderby=dateline"
    ]

    def process_result(self, result: Result) -> Result:
        parts = urlparse(result.url)
        _path = self.work_dir / Path(parts.netloc) / valid_path(result.title)
        _path.mkdir(parents=True, exist_ok=True)

        filename = Path(parts.path).name
        _path /= filename
        print("\n[Result]")
        for attr in result.__slots__:
            attr_value = getattr(result, attr)

            if isinstance(attr_value, dict):
                for k, v in attr_value.items():
                    if k == "image":
                        print(k, _path.absolute())
                        _path.write_bytes(v)

            else:
                print(attr, attr_value)

        return result


if __name__ == "__main__":
    # from pygather.downloader import PlaywrightDownloader
    tracemalloc.start()

    s = HKPicSpider(
        spider_log_level=20,
        downloader_log_level=20,
        scheduler_log_level=20,
        parser_log_level=20,
        concurrency=5,
        # downloader=PlaywrightDownloader,
        cookies=load_cookies(data_path=r"E:\Code\Python\WebCrawler\pygather\data"),
        storage_file=r"E:\Code\Python\WebCrawler\pygather\data\state.json",
        unique=False,
        wait_times=5,
        work_dir=r"E:\Code\Python\WebCrawler\pygather\data",
    )

    p = Path("data/recoder.json")
    print(s.work_dir)
    try:
        # import threading
        # t = threading.Thread(target=s.start, args=())
        # print(threading.main_thread())
        # print(t)
        # t.run()
        # t.start()
        s.start()
    finally:
        with p.open("w", encoding="utf8") as f:
            json.dump(recoder, f, ensure_ascii=False)

        snapshot1 = tracemalloc.take_snapshot()
        top_stats = snapshot1.statistics("lineno")
        print("[ Top 20 ]")
        for stat in top_stats[:20]:
            print(stat)
