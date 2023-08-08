import asyncio
import tracemalloc

import aiohttp

from webants.libs import Response, Request


async def main():
    url = (
        "http://108.170.5.99/data/attachment/forum/202011/10/170328re946lx74pp4qz78.jpg"
    )
    # url = 'http://108.170.5.99/thread-8075084-1-1.html'
    async with aiohttp.ClientSession() as session:
        async with session.request("Get", url) as r:
            # resp = Response(r.method, r.real_url,
            #                 http_version=r.version,
            #                 status=r.status,
            #                 reason=r.reason,
            #                 headers=r.headers,
            #                 cookies=r.cookies,
            #                 body=await r.read(),
            #                 encoding=r.get_encoding(),
            #                 history=r.history,
            #                 links=r.links,
            #                 request=Request(url))
            resp = await Response.build(r, request=Request(url))
            print(resp.status_code)
            print(resp.text)
            print(resp.mediatype)
            print(resp.encoding)
            print(resp.headers)
            print(r.cookies)


if __name__ == "__main__":
    tracemalloc.start()

    asyncio.run(main())
    snapshot1 = tracemalloc.take_snapshot()

    asyncio.run(main())
    snapshot2 = tracemalloc.take_snapshot()

    # top_stats = snapshot1.statistics('lineno')
    top_stats = snapshot2.compare_to(snapshot1, "lineno")

    print("[ Top 10 ]")
    for stat in top_stats[:10]:
        print(stat)

    top_stats = snapshot1.statistics("traceback")

    # pick the biggest memory block
    stat = top_stats[0]
    print("\n%s memory blocks: %.1f KiB" % (stat.count, stat.size / 1024))
    for line in stat.traceback.format():
        print(line)
