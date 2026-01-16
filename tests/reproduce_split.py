import asyncio
import os
import sys

async def run_test():
    host = '127.0.0.1'
    port = 8080

    print(f"Connecting to {host}:{port}...")
    reader, writer = await asyncio.open_connection(host, port)

    # 1. Send Headers (Chunk 1)
    headers = (
        "POST /split_test HTTP/1.1\r\n"
        "Host: localhost:8080\r\n"
        "Content-Length: 4\r\n"
        "Content-Type: text/plain\r\n"
        "\r\n"
    )
    print("Sending Headers...")
    writer.write(headers.encode())
    await writer.drain()

    await asyncio.sleep(0.5) # Ensure flush

    # 2. Send Body (Chunk 2)
    print("Sending Body ('test')...")
    writer.write(b"test")
    await writer.drain()

    # Read response
    try:
        data = await reader.read(1024)
        print(f"Received: {data}")
        if b"200 OK" in data or b"404 Not Found" in data:
            # If we get a valid HTTP response, it means the server processed it.
            # Even if 404, it means the server got the request.
            # If blocked, we expect connection close or no response.
            print("RESULT: Server responded (Passed/Leaked)")
        else:
            print("RESULT: Connection closed/No valid response (Blocked)")
    except Exception as e:
        print(f"RESULT: Error {e}")

    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(run_test())
