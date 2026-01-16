import asyncio
import logging
from typing import Optional
from app.core.parser import HttpStreamParser, ParserMode, HttpRequest, HttpResponse
from app.core.logger import format_http_message
from app.core.session import SessionManager
from app.core.engine import RuleEngine, ActionType

logger = logging.getLogger(__name__)

class TcpProxy:
    def __init__(self, listen_host: str, listen_port: int, target_host: str, target_port: int):
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.target_host = target_host
        self.target_port = target_port
        self.server = None
        self.rule_engine = RuleEngine() 

    async def start(self):
        self.server = await asyncio.start_server(
            self.handle_client, self.listen_host, self.listen_port
        )
        logger.info(f"Proxy listening on {self.listen_host}:{self.listen_port} -> {self.target_host}:{self.target_port}")
        async with self.server:
            await self.server.serve_forever()

    async def handle_client(self, client_reader: asyncio.StreamReader, client_writer: asyncio.StreamWriter):
        peer_name = client_writer.get_extra_info('peername')
        logger.info(f"New connection from {peer_name}")

        client_ip, client_port = peer_name[0], peer_name[1]

        target_reader, target_writer = await self.connect_to_target()
        if not target_reader or not target_writer:
            client_writer.close()
            return


        stream_id = await SessionManager.start_stream(
            client_ip, client_port, self.target_host, self.target_port
        )

        #парсеры
        req_parser = HttpStreamParser(mode=ParserMode.REQUEST)
        res_parser = HttpStreamParser(mode=ParserMode.RESPONSE)


        client_to_target = asyncio.create_task(
            self.pipe(client_reader, target_writer, "Client->Target", req_parser, stream_id, client_ip)
        )
        target_to_client = asyncio.create_task(
            self.pipe(target_reader, client_writer, "Target->Client", res_parser, stream_id)
        )

        done, pending = await asyncio.wait(
            [client_to_target, target_to_client],
            return_when=asyncio.FIRST_COMPLETED
        )

        for task in pending:
            task.cancel()

        await SessionManager.close_stream(stream_id)

        logger.info(f"Connection closed for {peer_name}")
        client_writer.close()
        target_writer.close()

    async def connect_to_target(self) -> tuple[Optional[asyncio.StreamReader], Optional[asyncio.StreamWriter]]:
        try:
            reader, writer = await asyncio.open_connection(self.target_host, self.target_port)
            return reader, writer
        except Exception as e:
            logger.error(f"Failed to connect to target {self.target_host}:{self.target_port}: {e}")
            return None, None

    async def pipe(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, direction: str, parser: Optional[HttpStreamParser] = None, stream_id: int = -1, client_ip: str = ""):
        try:
            buffer = b""
            MAX_BUFFER = 10 * 1024 * 1024 # 10 мб на буфер для защиты от переполнения
            parser_failed = False

            while True:
                data = await reader.read(4096)
                if not data:
                    break

                if parser and not parser_failed:

                    # 1. в буфер всё
                    buffer += data

                    # 2. парсинг
                    try:
                        messages = parser.feed(data)
                    except Exception:
                        # возможно не хттп, не парсится
                        parser_failed = True
                        writer.write(buffer)
                        await writer.drain()
                        buffer = b""
                        continue

                    # 3. проверяем паршенные сообщения
                    if messages:
                        for msg in messages:
                            # примененеи правил
                            verdict_tags = []
                            blocked = False

                            if isinstance(msg, HttpRequest):
                                msg.client_ip = client_ip
                                msg.destination_port = self.target_port
                                action = self.rule_engine.evaluate(msg)
                                verdict_tags = action.tags

                                if action.type == ActionType.DROP:
                                    logger.warning(f"[{direction}] BLOCKED by Rule. Tags: {verdict_tags}")
                                    await SessionManager.log_request(stream_id, msg, verdict_tags)
                                    await SessionManager.update_session_alert(stream_id, 2) #ставим отметку что блок
                                    return 

                                blocked = False 

                            
                            formatted_log = format_http_message(msg)
                            logger.info(f"\n{'-'*40}\nHTTP CAPTURE [{direction}]:\n{formatted_log}\n{'-'*40}")

                            if isinstance(msg, HttpRequest):
                                await SessionManager.log_request(stream_id, msg, verdict_tags)
                            elif isinstance(msg, HttpResponse):
                                await SessionManager.log_response(stream_id, msg, verdict_tags)



                        #в идеале пропускать только распаршенное, но потом, пока весь буфер шлём



                        writer.write(buffer)
                        await writer.drain()
                        buffer = b""
                    else:

                        if len(buffer) > MAX_BUFFER:
                            logger.warning(f"[{direction}] !!Buf overflow ({len(buffer)} bytes). ") #переполнение
                            writer.write(buffer)
                            await writer.drain()
                            buffer = b""

                        if len(buffer) > 4096:
                             logger.warning(f"[{direction}] Parsing timeout (buff > 4KB without headers).") 
                             parser_failed = True
                             writer.write(buffer)
                             await writer.drain()
                             buffer = b""
                else:
                    #пропуск, если лег парсер
                    writer.write(data)
                    await writer.drain()

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error in pipe {direction}: {e}")
        finally:
             try:
                 writer.close()
             except:
                 pass
