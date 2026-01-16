import asyncio
import os
import sys

sys.path.append(os.getcwd())

from app.database.db import db
from config import config

async def test_db():
    # Ensure clean start
    if os.path.exists(config.DB_PATH):
        os.remove(config.DB_PATH)

    print("Initializing DB...")
    await db.connect()

    print("Checking tables...")
    async with db._connection.execute("SELECT name FROM sqlite_master WHERE type='table';") as cursor:
        tables = await cursor.fetchall()
        table_names = [row['name'] for row in tables]
        print(f"Tables found: {table_names}")

        assert 'user_sessions' in table_names
        assert 'tcp_streams' in table_names
        assert 'messages' in table_names

    print("Inserting user session...")
    uid = await db.execute(
        "INSERT INTO user_sessions (client_ip, start_time, last_activity_time) VALUES (?, ?, ?)",
        ('127.0.0.1', 1000.0, 1000.0)
    )
    print(f"User Session ID: {uid}")

    print("Inserting TCP Stream...")
    tid = await db.execute(
        "INSERT INTO tcp_streams (user_session_id, client_ip, client_port, start_time) VALUES (?, ?, ?, ?)",
        (uid, '127.0.0.1', 12345, 1000.0)
    )
    print(f"TCP Stream ID: {tid}")

    assert uid > 0
    assert tid > 0

    await db.close()
    print("TEST PASSED")

if __name__ == "__main__":
    asyncio.run(test_db())
