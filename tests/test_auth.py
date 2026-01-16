import asyncio
import aiohttp
import os
import sys
import base64

sys.path.append(os.getcwd())
from config import config

async def test_auth():
    url = f"http://localhost:{config.WEB_PORT}/api/sessions"

    # 1. No Auth
    print("Testing No Auth...")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(f"Status: {resp.status}")
            assert resp.status == 401
            print("PASS: 401 Unauthorized received")

    # 2. Correct Auth
    print("Testing Correct Auth...")
    auth = aiohttp.BasicAuth(config.ADMIN_USERNAME, config.ADMIN_PASSWORD)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, auth=auth) as resp:
            print(f"Status: {resp.status}")
            assert resp.status == 200
            print("PASS: 200 OK received")

if __name__ == "__main__":
    asyncio.run(test_auth())
