from webants.libs.exceptions import InvalidExtractor
from webants.libs.extractor import *

# ElementExtractor = Extractor.create_extractor('ElementExtractor')
# AttribExtractor = Extractor.create_extractor('AttribExtractor')
# LinkExtractor = Extractor.create_extractor('LinkExtractor')
# TextExtractor = Extractor.create_extractor('TextExtractor')
#
# FilteringLinkExtractor = Extractor.create_extractor('filtering')

try:
    AttrExtractor = ExtractorFactory.create_extractor("AttrExtractor")
except InvalidExtractor as exception:
    assert isinstance(exception, InvalidExtractor)


def test_extract_method():
    url = "http://108.170.5.99/forum.php"
    file_path = r"E:\Code\Python\WebCrawler\pygather\data\html\forum.htm"
    with open(file_path, "r", encoding="utf8") as fp:
        html = fp.read()
    # resp.encoding = 'gb2312'
    print(f"--------ElementExtractor---------")
    e = ElementExtractor(selector="a.xst")
    els = e.extract(html)
    print(els)
    e = ElementExtractor()
    print(e.extract(html))
    print(f"\n--------LinkExtractor---------")
    e = LinkExtractor(selector="a.xst", attr="href", base_url=url)
    print("LinkExtractor", e.extract(html))

    print(f"\n--------AttribExtractor---------")
    e = AttribExtractor(tags="a", attr="href")
    print("AttribExtractor", links1 := e.extract(html))

    e = AttribExtractor(attr="href", selector="a[href]")
    print("AttribExtractor", links2 := e.extract(html))

    e = AttribExtractor(
        tags=None,
        attr="href",
        xpath="//a[@href]",
    )
    print("AttribExtractor", links3 := e.extract(html))

    e = AttribExtractor(attr="href", selector="a.xst")
    print("AttribExtractor", links4 := e.extract(html))

    assert links1 == links2 == links3 != links4

    print(f"\n--------TextExtractor---------")
    e = TextExtractor(selector="a")
    texts = e.extract(
        html,
    )
    print(texts)

    e = TextExtractor(xpath="//div")
    texts1 = e.extract(html)
    print(texts1)
    e = TextExtractor(xpath="//div//text()")
    texts2 = e.extract(html)
    print(texts2)
    assert texts != texts1 != texts2

    e = TextExtractor(tags="title")
    print(
        "title: ",
        "".join(
            e.extract(
                html,
            )
        ),
    )

    print(f"\n--------LinkExtractor---------")
    with open(
        r"E:\Code\Python\WebCrawler\pygather\data\html\thread.htm", "r", encoding="utf8"
    ) as fp:
        html = fp.read()
    e = LinkExtractor(tags=("img",), attr="file", base_url=url)
    print("LinkExtractor", links1 := e.extract(html))
    e = LinkExtractor(selector="img[file]", attr="file", base_url=url)
    print("LinkExtractor", links2 := e.extract(html))
    e = LinkExtractor(xpath="//img[@file]", attr="file", base_url=url)
    print("LinkExtractor", links3 := e.extract(html))
    assert len(links1) == len(links2) == len(links3)


def test_filtering_extractor():
    print(f"\n--------FilteringLinkExtractor---------")
    url = "http://108.170.5.99/forum.php"
    file_path = r"E:\Code\Python\WebCrawler\pygather\data\html\forum.htm"
    with open(file_path, "r", encoding="utf8") as fp:
        html = fp.read()

    fle = FilteringLinkExtractor(
        hosts_allow=[
            "108.170.5.99",
        ],
        selector="a.xst",
        # tags=['a'],
        attr="href",
        base_url=url,
        many=True,
    )
    print("FilteringLinkExtractor", results := fle.extract(html))
    if results:
        assert any(["108.170.5.99" in link.url for link in results])

    with open(
        r"E:\Code\Python\WebCrawler\pygather\data\html\thread.htm", "r", encoding="utf8"
    ) as fp:
        html = fp.read()

    def foo(link: Link):
        return link.remove_suffix(".thumb.jpg")

    fle = FilteringLinkExtractor(
        hosts_allow=[
            "108.170.5.99",
        ],
        extensions_allow=["Jpg", "jpeg", "png", "GIF"],
        selector="img[file]",
        attr="file",
        link_process_func=foo,
        base_url=url,
    )
    print("FilteringLinkExtractor", results := fle.extract(html))
    if results:
        assert any(["108.170.5.99" in link.url for link in results])


def test_functions():
    with open(
        r"E:\Code\Python\WebCrawler\pygather\data\html\thread.htm", "r", encoding="utf8"
    ) as fp:
        html = fp.read()
    print(extract_links(html, selector="a[href]"))
    print(extract_links(html, xpath="//a[@href]"))
    print(extract_links(html, tags="a", attr="href"))
    print(extract_and_filter_links(html, hosts_allow=["108.170.5.99"]))

    print(extract_links(html, selector="base")[0])
    print(get_base_url(html))

    print(extract_attrib(html, tags="a", attr="href"))
    print(extract_text(html, selector="div a"))

    print(extract_text(html, tags="title")[0])
    print(get_html_title(html))


if __name__ == "__main__":
    test_extract_method()
    test_filtering_extractor()
    print(f"\n--------Extractor---------")
    print(ExtractorFactory.extractors.keys())
    # test_functions()
