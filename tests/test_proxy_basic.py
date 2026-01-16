import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from app.core.proxy import TcpProxy

async def run_dummy_server(port):
    server = await asyncio.start_server(handle_echo, '127.0.0.1', port)
    print(f"Dummy Echo Server serving on {port}")
    async with server:
        await server.serve_forever()

async def handle_echo(reader, writer):
    data = await reader.read(1024)
    message = data.decode()
    print(f"Echo Server Received: {message}")

    # Send valid HTTP response so proxy parser is happy
    response = "HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\nEcho!"
    writer.write(response.encode())
    await writer.drain()
    writer.close()

async def run_test():
    # 1. Start Dummy Server
    server_task = asyncio.create_task(run_dummy_server(9000))
    await asyncio.sleep(1) # Wait for startup

    # 2. Start Proxy
    proxy = TcpProxy('127.0.0.1', 8080, '127.0.0.1', 9000)
    proxy_task = asyncio.create_task(proxy.start())
    await asyncio.sleep(1)

    # 3. Client connects to Proxy
    print("Client connecting to proxy...")
    reader, writer = await asyncio.open_connection('127.0.0.1', 8080)

    # Send valid HTTP request
    message = "GET /echo HTTP/1.1\r\nHost: localhost\r\n\r\n"
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(1024)
    response = data.decode()
    print(f"Client Received: {response}")

    writer.close()
    await writer.wait_closed()

    assert "200 OK" in response
    print("TEST PASSED: Proxy forwarded HTTP correctly.")

    # Cleanup
    server_task.cancel()
    proxy_task.cancel()

if __name__ == "__main__":
    try:
        asyncio.run(run_test())
    except KeyboardInterrupt:
        pass
