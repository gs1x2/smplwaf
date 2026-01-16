import asyncio
import aiohttp
import os
import sys
import json

sys.path.append(os.getcwd())
from config import config

async def test_api_details():
    url = f"http://localhost:{config.WEB_PORT}/api/sessions"
    auth = aiohttp.BasicAuth(config.ADMIN_USERNAME, config.ADMIN_PASSWORD)

    print(f"Fetching {url}...")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, auth=auth) as resp:
            print(f"Status: {resp.status}")
            assert resp.status == 200

            data = await resp.json()
            print(f"Sessions: {len(data)}")

            # Find a session with messages
            found_msg = False
            for s in data:
                if 'streams' in s:
                    for st in s['streams']:
                        if 'messages' in st:
                            for m in st['messages']:
                                print(f"Checking Message ID {m['id']}...")
                                if 'timestamp' in m:
                                    print(f"PASS: Timestamp present: {m['timestamp']}")
                                    assert m['timestamp'] is not None
                                    found_msg = True
                                else:
                                    print("FAIL: Timestamp missing!")
                                    assert False
                                break
                        if found_msg: break
                if found_msg: break

            if not found_msg:
                print("WARNING: No messages found in DB to verify structure. Run traffic generator first.")

if __name__ == "__main__":
    asyncio.run(test_api_details())
