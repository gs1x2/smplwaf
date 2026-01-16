from typing import Union
from app.core.parser import HttpRequest, HttpResponse

def format_http_message(msg: Union[HttpRequest, HttpResponse]) -> str:

    lines = []

    if isinstance(msg, HttpRequest):
        title = f"> {msg.method} {msg.path} HTTP/{msg.version}"
        prefix = "> "
    else:
        title = f"< HTTP/{msg.version} {msg.status_code}"
        prefix = "< "

    lines.append(title)


    for key, val in msg.headers.items():
        lines.append(f"{prefix}{key}: {val}")

    lines.append(prefix) 

    if msg.body:
        body_preview = msg.body[:500] 
        try:
            body_str = body_preview.decode('utf-8')
            lines.append(body_str)
        except UnicodeDecodeError:
            lines.append(f"[Binary: {len(msg.body)} bytes]")

        if len(msg.body) > 500:
            lines.append(f"... ({len(msg.body) - 500} more bytes)")

    return "\n".join(lines)
