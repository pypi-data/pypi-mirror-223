import asyncio

from webants.libs import Response, LinkItem, TextItem, LinkItemDescriptor
from webants.parser import Parser


class HKPicParser(Parser):
    url = LinkItemDescriptor(attr="href", selector="a[href]")
    image = LinkItem(
        attr="file",
        selector="td.plc img[file]",
        base_url="http://108.170.5.99",
        hosts_allow=["108.170.5.99"],
        link_process_func=lambda link: link.remove_suffix(".thumb.jpg"),
    )
    title = TextItem(selector="title")
    forum = LinkItem(attr="href", selector="a[href]")


async def main():
    raw_req_queue = asyncio.Queue()
    resp_queue = asyncio.Queue()

    with open(
        r"E:\Code\Python\WebCrawler\pygather\data\html\thread.htm", "r", encoding="utf8"
    ) as fp:
        html = fp.read()
    resp_queue.put_nowait(
        Response(
            method="GET",
            url="http://108.170.5.99/thread-8127933-1-1.html",
            status_code=200,
            reason="",
            request=None,
            body=html.encode(encoding="utf8"),
        )
    )
    with open(
        r"E:\Code\Python\WebCrawler\pygather\data\html\forum.htm", "r", encoding="utf8"
    ) as fp:
        html = fp.read()
    resp_queue.put_nowait(
        Response(
            method="GET",
            url="http://108.170.5.99/forum.php",
            status_code=200,
            reason="",
            request=None,
            body=html.encode(encoding="utf8"),
        )
    )
    parser = HKPicParser(
        response_queue=resp_queue, raw_request_queue=raw_req_queue, log_level=10
    )

    await parser.start_parser()
    await parser.close()


if __name__ == "__main__":
    asyncio.run(main(), debug=True)
