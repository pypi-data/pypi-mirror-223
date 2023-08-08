import unittest

from webants.libs import Request
from webants.utils import url_fingerprint


class TestRequestModule(unittest.TestCase):
    def setUp(self) -> None:
        self.req1 = Request(
            "http://user:pass@example.com:8042/over/there?arg2=b&arg1=a2&arg1=a1#nose"
        )
        self.req2 = Request(
            "http://user:pass@example.com:8042/over/there?arg1=a2&arg1=a1&arg2=b#nose1"
        )

    def test_fingerprint(self):
        self.assertEqual(self.req1.fingerprint(), self.req2.fingerprint())

        self.assertNotEqual(
            self.req1.fingerprint(keep_auth=True), self.req2.fingerprint()
        )
        self.assertNotEqual(
            self.req1.fingerprint(sort_query=False), self.req2.fingerprint()
        )

        self.assertNotEqual(
            self.req1.fingerprint(sort_query=False),
            self.req2.fingerprint(sort_query=False),
        )

        self.assertNotEqual(
            self.req1.fingerprint(keep_fragments=True),
            self.req2.fingerprint(keep_fragments=True),
        )
        self.assertNotEqual(
            self.req1.fingerprint(), url_fingerprint(self.req1.url, self.req1.method)
        )

    def test_request_comparison(self):
        self.assertFalse(self.req1 < self.req2)
        self.assertTrue(self.req1 > self.req2)

        self.assertFalse(self.req1 == self.req2)


if __name__ == "__main__":
    unittest.main()
