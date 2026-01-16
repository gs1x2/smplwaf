from typing import Optional, Dict, List, Union
from dataclasses import dataclass, field
from enum import Enum
import httptools

class ParserMode(Enum):
    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"

@dataclass
class HttpRequest:
    method: str = ""
    path: str = ""
    version: str = ""
    headers: Dict[str, str] = field(default_factory=dict)
    raw_headers: str = ""
    body: bytes = b""
    client_ip: str = "" 
    destination_port: int = 0 

    @property
    def data(self) -> str:
        return self.body.decode('utf-8', errors='ignore')

    def __repr__(self):
        return f"<HttpRequest {self.method} {self.path}>"

@dataclass
class HttpResponse:
    status_code: int = 0
    version: str = ""
    headers: Dict[str, str] = field(default_factory=dict)
    raw_headers: str = ""
    body: bytes = b""

    def __repr__(self):
        return f"<HttpResponse {self.status_code}>"

class HttpStreamParser:
    def __init__(self, mode: ParserMode = ParserMode.REQUEST):
        self.mode = mode
        self.completed_messages: List[Union[HttpRequest, HttpResponse]] = []


        self._current_headers = {}
        self._current_raw_headers = []
        self._current_body = b""
        self._current_url = b"" 
        self._current_status_code = 0 

        if mode == ParserMode.REQUEST:
            self._parser = httptools.HttpRequestParser(self)
        else:
            self._parser = httptools.HttpResponseParser(self)

    def feed(self, data: bytes) -> List[Union[HttpRequest, HttpResponse]]:
        try:
            self._parser.feed_data(data)
        except httptools.HttpParserError:
            raise

        results = self.completed_messages
        self.completed_messages = []
        return results


    def on_message_begin(self):
        self._current_headers = {}
        self._current_raw_headers = []
        self._current_url = b""
        self._current_body = b""
        self._current_status_code = 0

    def on_url(self, url: bytes):
        self._current_url += url

    def on_status(self, status: bytes):
    #в httptools так не работает
        pass

    def on_header(self, name: bytes, value: bytes):
        key = name.decode('utf-8', errors='replace')
        val = value.decode('utf-8', errors='replace')
        self._current_headers[key] = val
        self._current_raw_headers.append(f"{key}: {val}")

    def on_headers_complete(self):
        #!!потом
        pass

    def on_body(self, body: bytes):
        self._current_body += body

    def on_message_complete(self):
        version = self._parser.get_http_version()

        if self.mode == ParserMode.REQUEST:
            msg = HttpRequest(
                method=self._parser.get_method().decode('utf-8', errors='replace'),
                path=self._current_url.decode('utf-8', errors='replace'),
                version=version,
                headers=self._current_headers,
                raw_headers="\r\n".join(self._current_raw_headers),
                body=self._current_body
            )
        else:
            msg = HttpResponse(
                status_code=self._parser.get_status_code(),
                version=version,
                headers=self._current_headers,
                raw_headers="\r\n".join(self._current_raw_headers),
                body=self._current_body
            )

        self.completed_messages.append(msg)
