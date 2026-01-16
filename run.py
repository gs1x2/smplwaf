import asyncio
import logging
import sys
import os
import uvicorn
from fastapi import FastAPI


sys.path.append(os.getcwd())

from config import config
from app.core.proxy import TcpProxy
from app.database.db import db
from app.web.app import app as web_app 


logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.getLogger("aiosqlite").setLevel(logging.WARNING)

logger = logging.getLogger("Main")

async def run_proxy():
    proxy = TcpProxy(
        listen_host=config.PROXY_HOST,
        listen_port=config.PROXY_PORT,
        target_host=config.TARGET_HOST,
        target_port=config.TARGET_PORT
    )


    web_app.state.rule_engine = proxy.rule_engine


    await db.connect()

    try:
        await proxy.start()
    except asyncio.CancelledError:
        pass

async def run_web():
    config_uvicorn = uvicorn.Config(web_app, host="0.0.0.0", port=config.WEB_PORT, log_level="info")
    server = uvicorn.Server(config_uvicorn)
    await server.serve()

async def main():
    print("="*60)
    print(f"Файрволл запущен")
    print(f"Прокси слушает: {config.PROXY_HOST}:{config.PROXY_PORT} -> {config.TARGET_HOST}:{config.TARGET_PORT}")
    print(f"Панель управления: http://localhost:{config.WEB_PORT}")
    print("="*60)


    try:
        await asyncio.gather(
            run_proxy(),
            run_web()
        )
    except KeyboardInterrupt:
        logger.info("Остановка...")
    finally:
        await db.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
