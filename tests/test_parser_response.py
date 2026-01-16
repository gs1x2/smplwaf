import unittest
from app.core.parser import HttpStreamParser, ParserMode, HttpResponse

class TestResponseParser(unittest.TestCase):
    def test_simple_response(self):
        parser = HttpStreamParser(mode=ParserMode.RESPONSE)
        raw_res = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nhello"

        msgs = parser.feed(raw_res)
        self.assertEqual(len(msgs), 1)
        res = msgs[0]
        self.assertIsInstance(res, HttpResponse)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'text/plain')
        self.assertEqual(res.body, b'hello')

    def test_chunked_response(self):
        # httptools handles chunked decoding automatically? Let's verify.
        # Actually httptools just passes the body chunks. It decodes the chunk headers.
        parser = HttpStreamParser(mode=ParserMode.RESPONSE)
        raw_res = b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n5\r\nhello\r\n0\r\n\r\n"

        msgs = parser.feed(raw_res)
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0].body, b'hello')

if __name__ == "__main__":
    unittest.main()
