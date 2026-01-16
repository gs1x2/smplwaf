import unittest
from app.core.parser import HttpStreamParser, ParserMode

class TestHttpParser(unittest.TestCase):
    def test_get_request(self):
        parser = HttpStreamParser(mode=ParserMode.REQUEST)
        raw_req = b"GET /index.html HTTP/1.1\r\nHost: localhost\r\n\r\n"
        reqs = parser.feed(raw_req)

        self.assertEqual(len(reqs), 1)
        req = reqs[0]
        self.assertEqual(req.method, "GET")
        self.assertEqual(req.path, "/index.html")
        self.assertEqual(req.headers["Host"], "localhost")
        self.assertEqual(req.body, b"")

    def test_post_request_with_body(self):
        parser = HttpStreamParser(mode=ParserMode.REQUEST)
        body = b"hello=world"
        length = len(body)
        raw_req = f"POST /submit HTTP/1.1\r\nContent-Length: {length}\r\n\r\n".encode() + body

        reqs = parser.feed(raw_req)

        self.assertEqual(len(reqs), 1)
        req = reqs[0]
        self.assertEqual(req.method, "POST")
        self.assertEqual(req.body, body)

    def test_partial_feed(self):
        parser = HttpStreamParser(mode=ParserMode.REQUEST)
        part1 = b"GET /partial "
        part2 = b"HTTP/1.1\r\nHost: "
        part3 = b"localhost\r\n\r\n"

        # Feed partial chunks
        self.assertEqual(parser.feed(part1), [])
        self.assertEqual(parser.feed(part2), [])

        # Complete the request
        reqs = parser.feed(part3)
        self.assertEqual(len(reqs), 1)
        self.assertEqual(reqs[0].method, "GET")
        self.assertEqual(reqs[0].path, "/partial")

    def test_pipelining(self):
        """Test multiple requests in a single chunk"""
        parser = HttpStreamParser(mode=ParserMode.REQUEST)
        req1 = b"GET /first HTTP/1.1\r\nHost: loc\r\n\r\n"
        req2 = b"POST /second HTTP/1.1\r\nContent-Length: 4\r\n\r\ndata"

        reqs = parser.feed(req1 + req2)

        self.assertEqual(len(reqs), 2)
        self.assertEqual(reqs[0].method, "GET")
        self.assertEqual(reqs[0].path, "/first")
        self.assertEqual(reqs[1].method, "POST")
        self.assertEqual(reqs[1].path, "/second")
        self.assertEqual(reqs[1].body, b"data")

    def test_pipelining_split(self):
        """Test multiple requests split across chunks oddly"""
        parser = HttpStreamParser(mode=ParserMode.REQUEST)
        req1 = b"GET /first HTTP/1.1\r\nHost: loc\r\n\r\n"
        req2_part1 = b"POST /sec"
        req2_part2 = b"ond HTTP/1.1\r\nContent-Length: 0\r\n\r\n"

        # Chunk 1: Complete Req 1 and start of Req 2
        reqs1 = parser.feed(req1 + req2_part1)
        self.assertEqual(len(reqs1), 1)
        self.assertEqual(reqs1[0].path, "/first")

        # Chunk 2: Rest of Req 2
        reqs2 = parser.feed(req2_part2)
        self.assertEqual(len(reqs2), 1)
        self.assertEqual(reqs2[0].path, "/second")

if __name__ == "__main__":
    unittest.main()
