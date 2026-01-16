import asyncio
import os
import sys

sys.path.append(os.getcwd())

from app.core.session import SessionManager
from app.database.db import db

async def test_session_aggregation():
    # Setup
    await db.connect()

    # 1. First connection
    print("Starting Stream 1...")
    sid1 = await SessionManager.start_stream("10.0.0.1", 1001, "8.8.8.8", 80)
    assert sid1 > 0

    # Check parent user session
    rows = await db.fetch_all("SELECT user_session_id FROM tcp_streams WHERE id = ?", (sid1,))
    uid1 = rows[0]['user_session_id']
    print(f"Stream 1 -> User Session {uid1}")

    # 2. Second connection immediately (should share user session)
    print("Starting Stream 2 (same IP)...")
    sid2 = await SessionManager.start_stream("10.0.0.1", 1002, "8.8.8.8", 80)

    rows = await db.fetch_all("SELECT user_session_id FROM tcp_streams WHERE id = ?", (sid2,))
    uid2 = rows[0]['user_session_id']
    print(f"Stream 2 -> User Session {uid2}")

    assert uid1 == uid2, "User Session ID should match for rapid connections"

    # 3. Third connection from different IP (should be new session)
    print("Starting Stream 3 (diff IP)...")
    sid3 = await SessionManager.start_stream("192.168.1.1", 5000, "8.8.8.8", 80)
    rows = await db.fetch_all("SELECT user_session_id FROM tcp_streams WHERE id = ?", (sid3,))
    uid3 = rows[0]['user_session_id']
    print(f"Stream 3 -> User Session {uid3}")

    assert uid3 != uid1

    await db.close()
    print("TEST PASSED")

if __name__ == "__main__":
    asyncio.run(test_session_aggregation())
