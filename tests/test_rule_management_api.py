import asyncio
import aiohttp
import os
import sys
import shutil

sys.path.append(os.getcwd())
from config import config

async def test_rule_api():
    base_url = f"http://localhost:{config.WEB_PORT}/api/rules"
    auth = aiohttp.BasicAuth(config.ADMIN_USERNAME, config.ADMIN_PASSWORD)

    test_rule_path = "dynamic/api_test.rule"
    test_rule_content = "if 'api_test' in request.path: action.drop()"

    async with aiohttp.ClientSession(auth=auth) as session:
        # 1. Create/Update Rule
        print(f"Creating rule at {test_rule_path}...")
        async with session.post(f"{base_url}/file", json={"path": test_rule_path, "content": test_rule_content}) as resp:
            print(f"Save Status: {resp.status}")
            assert resp.status == 200

        # 2. List Rules
        print("Listing rules...")
        async with session.get(f"{base_url}/list") as resp:
            data = await resp.json()
            print(f"Rules: {data}")
            assert test_rule_path in data

        # 3. Read Rule
        print("Reading rule...")
        async with session.get(f"{base_url}/file", params={"path": test_rule_path}) as resp:
            data = await resp.json()
            assert data["content"] == test_rule_content

        # 4. Reload Rules
        print("Reloading engine...")
        async with session.post(f"{base_url}/reload") as resp:
            print(f"Reload Status: {resp.status}")
            assert resp.status == 200

if __name__ == "__main__":
    asyncio.run(test_rule_api())
