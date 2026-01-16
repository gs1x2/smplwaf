import aiosqlite
import logging
import os
import asyncio
from config import config

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.db_path = config.DB_PATH
        self._connection = None

    async def connect(self):
        if not self._connection:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self._connection = await aiosqlite.connect(self.db_path)
            self._connection.row_factory = aiosqlite.Row
            await self.init_db()

    async def close(self):
        if self._connection:
            await self._connection.close()
            self._connection = None

    async def init_db(self):
        if not self._connection:
            return


        await self._connection.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_ip TEXT,
                start_time REAL,
                last_activity_time REAL,
                alert_level INTEGER DEFAULT 0 -- 0=None, 1=Mark, 2=Block
            )
        """)

        await self._connection.execute("""
            CREATE TABLE IF NOT EXISTS tcp_streams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_session_id INTEGER,
                client_ip TEXT,
                client_port INTEGER,
                target_ip TEXT,
                target_port INTEGER,
                start_time REAL,
                end_time REAL,
                is_closed INTEGER DEFAULT 0,
                FOREIGN KEY(user_session_id) REFERENCES user_sessions(id)
            )
        """)

        await self._connection.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tcp_stream_id INTEGER,
                type TEXT,  -- 'REQUEST' or 'RESPONSE'
                method TEXT,
                url TEXT,
                status_code INTEGER,
                headers TEXT, -- JSON string
                body BLOB,
                tags TEXT, -- JSON list of tags
                timestamp REAL,
                FOREIGN KEY(tcp_stream_id) REFERENCES tcp_streams(id)
            )
        """)


        try:
            await self._connection.execute("ALTER TABLE messages ADD COLUMN tags TEXT")
        except:
            pass


        try:
            await self._connection.execute("ALTER TABLE user_sessions ADD COLUMN alert_level INTEGER DEFAULT 0")
        except:
            pass

        await self._connection.commit()

    async def execute(self, query: str, parameters: tuple = ()):
        if not self._connection:
            await self.connect()
        async with self._connection.execute(query, parameters) as cursor:
            await self._connection.commit()
            return cursor.lastrowid

    async def fetch_all(self, query: str, parameters: tuple = ()):
        if not self._connection:
            await self.connect()
        async with self._connection.execute(query, parameters) as cursor:
            return await cursor.fetchall()

db = Database()
