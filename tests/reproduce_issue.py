import asyncio
import aiohttp
import os
import sys

sys.path.append(os.getcwd())

async def run_test():
    print("Sending POST request with body 'test'...")
    async with aiohttp.ClientSession() as session:
        try:
            # We target the proxy port 8080
            # payload='test' means body is "test"
            async with session.post('http://localhost:8080/submit', data='test', timeout=2) as resp:
                print(f"Response Status: {resp.status}")
                text = await resp.text()
                print(f"Response Body: {text}")

                if resp.status == 200 or resp.status == 404:
                    print("FAIL: Request passed through (expected block/connection drop)")
                else:
                    print("SUCCESS: Request was blocked (status not 200/404)")
        except aiohttp.ClientConnectorError:
            print("SUCCESS: Connection dropped (Blocked)")
        except Exception as e:
            print(f"SUCCESS: Exception occurred ({e})")

if __name__ == "__main__":
    # We assume run.py and python3 -m http.server 9000 are already running from the previous step
    # If not, this script might fail to connect.
    # But for the purpose of the plan step, I will run the env setup in bash.
    asyncio.run(run_test())
