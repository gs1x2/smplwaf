import asyncio
import aiohttp
import os
import sys

sys.path.append(os.getcwd())
from config import config

async def test_rule_actions():
    base_url = f"http://localhost:{config.WEB_PORT}/api/rules"
    auth = aiohttp.BasicAuth(config.ADMIN_USERNAME, config.ADMIN_PASSWORD)

    rule_path = "dynamic/action_test.rule"
    rule_content = "action.mark('test')"

    async with aiohttp.ClientSession(auth=auth) as session:
        # 1. Create Rule
        print("Creating rule...")
        await session.post(f"{base_url}/file", json={"path": rule_path, "content": rule_content})

        # 2. Toggle Rule (Disable)
        print("Disabling rule...")
        resp = await session.post(f"{base_url}/toggle", json={"path": rule_path})
        assert resp.status == 200

        # Check list (should be disabled)
        resp = await session.get(f"{base_url}/list")
        data = await resp.json()
        found = False
        for r in data:
            if r["path"] == rule_path + ".disabled":
                assert r["enabled"] is False
                found = True
        if not found:
            print("FAIL: Disabled rule not found in list")
            assert False

        # 3. Toggle Rule (Enable)
        print("Enabling rule...")
        resp = await session.post(f"{base_url}/toggle", json={"path": rule_path + ".disabled"})
        assert resp.status == 200

        # 4. Delete Rule
        print("Deleting rule...")
        resp = await session.post(f"{base_url}/delete", json={"path": rule_path})
        assert resp.status == 200

        # Verify deletion
        resp = await session.get(f"{base_url}/list")
        data = await resp.json()
        for r in data:
            if r["path"] == rule_path:
                print("FAIL: Rule still exists")
                assert False

        print("PASS: Rule actions verified")

if __name__ == "__main__":
    asyncio.run(test_rule_actions())
