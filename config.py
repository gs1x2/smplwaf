import os

class Config:
    # Учётные данные администратора
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

    # Порт панели управления
    WEB_PORT = int(os.getenv("WEB_PORT", "57230"))

    # Конфиг прокси (Хост не трогать)
    PROXY_HOST = os.getenv("PROXY_HOST", "0.0.0.0")
    PROXY_PORT = int(os.getenv("PROXY_PORT", "8080"))

    # Айпи и порт защищаемого сервиса
    # Например ваш сервис запущен локально на порту 5000:
    TARGET_HOST = os.getenv("TARGET_HOST", "127.0.0.1")
    TARGET_PORT = int(os.getenv("TARGET_PORT", "5000"))

    # Путь к БД
    DB_PATH = "data/db.sqlite"

    # Уровень логирования
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

config = Config()
