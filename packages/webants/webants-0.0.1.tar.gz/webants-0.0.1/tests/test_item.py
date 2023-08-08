from webants.libs.item import *


def test_link_item():
    url = "http://108.170.5.99/forum.php"
    file_path = r"E:\Code\Python\WebCrawler\pygather\data\html\forum.htm"
    with open(file_path, "r", encoding="utf8") as fp:
        html = fp.read()

    class TestMeta(type):
        def __new__(mcs, name: str, bases: tuple, attrs: dict):
            __items__ = {}
            for attr, attr_value in attrs.items():
                # 将自定义的Item类存储到类属性中
                if isinstance(attr_value, ItemDescriptor):
                    __items__[attr] = attr_value
            attrs["__items__"] = __items__
            return type.__new__(mcs, name, bases, attrs)

    class Test(metaclass=TestMeta):
        link = LinkItemDescriptor(attr="href", selector="a.xst", base_url=url)
        attr = AttrItemDescriptor(
            attr="href",
            selector="a.xst",
        )
        element = ElementItemDescriptor(
            attr="href",
            selector="a.xst",
        )
        text = TextItemDescriptor(attr="href", selector="a.xst")
        a = 2

    t = Test()
    print(t.__items__)

    for item_name, item_descriptor in t.__items__.items():
        if isinstance(item_descriptor, ItemDescriptor):
            setattr(t, item_name, html)
            print(f"[{item_name}]\n", getattr(t, item_name), "\n", sep="")


if __name__ == "__main__":
    test_link_item()
