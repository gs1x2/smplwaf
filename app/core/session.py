import json
import time
import logging
from typing import List
from app.database.db import db
from app.core.parser import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)

class SessionManager:
    SESSION_TIMEOUT = 30.0 #дебаг таймаут для непрерывных запросов. 30 сек раунд

    @staticmethod
    async def start_stream(client_ip: str, client_port: int, target_ip: str, target_port: int) -> int:
        try:
            now = time.time()


            rows = await db.fetch_all(
                """
                SELECT id FROM user_sessions
                WHERE client_ip = ? AND last_activity_time > ?
                ORDER BY last_activity_time DESC LIMIT 1
                """,
                (client_ip, now - SessionManager.SESSION_TIMEOUT)
            )

            if rows:
                user_session_id = rows[0]['id']

                await db.execute(
                    "UPDATE user_sessions SET last_activity_time = ? WHERE id = ?",
                    (now, user_session_id)
                )
            else:

                user_session_id = await db.execute(
                    """
                    INSERT INTO user_sessions (client_ip, start_time, last_activity_time)
                    VALUES (?, ?, ?)
                    """,
                    (client_ip, now, now)
                )


            stream_id = await db.execute(
                """
                INSERT INTO tcp_streams (user_session_id, client_ip, client_port, target_ip, target_port, start_time)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_session_id, client_ip, client_port, target_ip, target_port, now)
            )
            return stream_id
        except Exception as e:
            logger.error(f"Failed to start stream: {e}")
            return -1

    @staticmethod
    async def close_stream(stream_id: int):
        try:
            await db.execute(
                "UPDATE tcp_streams SET is_closed = 1, end_time = ? WHERE id = ?",
                (time.time(), stream_id)
            )
        except Exception as e:
            logger.error(f"Failed to close stream {stream_id}: {e}")

    @staticmethod
    async def _update_alert_level(stream_id: int, tags: List[str]):
        if not tags:
            return

        # любой тег > уровень 1 (маркировка), drop > уровень 2 (блок). tcpproxy решает реальный drop

        pass

    @staticmethod
    async def log_request(stream_id: int, req: HttpRequest, tags: List[str] = None):
        try:
            headers_json = json.dumps(req.headers)
            tags_json = json.dumps(tags or [])
            await db.execute(
                """
                INSERT INTO messages (tcp_stream_id, type, method, url, headers, body, tags, timestamp)
                VALUES (?, 'REQUEST', ?, ?, ?, ?, ?, ?)
                """,
                (stream_id, req.method, req.path, headers_json, req.body, tags_json, time.time())
            )
            if tags:
                await SessionManager.update_session_alert(stream_id, 1)
        except Exception as e:
            logger.error(f"Failed to log request for stream {stream_id}: {e}")

    @staticmethod
    async def log_response(stream_id: int, res: HttpResponse, tags: List[str] = None):
        try:
            headers_json = json.dumps(res.headers)
            tags_json = json.dumps(tags or [])
            await db.execute(
                """
                INSERT INTO messages (tcp_stream_id, type, status_code, headers, body, tags, timestamp)
                VALUES (?, 'RESPONSE', ?, ?, ?, ?, ?)
                """,
                (stream_id, res.status_code, headers_json, res.body, tags_json, time.time())
            )
            if tags:
                await SessionManager.update_session_alert(stream_id, 1)
        except Exception as e:
            logger.error(f"Failed to log response for stream {stream_id}: {e}")

    @staticmethod
    async def update_session_alert(stream_id: int, level: int):
        try:

            rows = await db.fetch_all("SELECT user_session_id FROM tcp_streams WHERE id = ?", (stream_id,))
            if rows:
                user_session_id = rows[0]['user_session_id']

                await db.execute(
                    "UPDATE user_sessions SET alert_level = MAX(alert_level, ?) WHERE id = ?",
                    (level, user_session_id)
                )
        except Exception as e:
            logger.error(f"Failed to update alert level: {e}")
