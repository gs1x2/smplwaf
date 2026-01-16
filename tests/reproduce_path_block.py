import asyncio
import aiohttp
import os
import sys

sys.path.append(os.getcwd())

async def run_test():
    print("Testing GET /test (Expect Block)...")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('http://localhost:8080/test', timeout=2) as resp:
                print(f"Response Status: {resp.status}")
                if resp.status == 404:
                    print("FAIL: Request passed through (Server returned 404)")
                else:
                    print(f"Result: {resp.status}")
        except aiohttp.ClientConnectorError:
            print("SUCCESS: Connection dropped (Blocked)")
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(run_test())
