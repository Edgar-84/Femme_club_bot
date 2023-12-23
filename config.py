import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Settings:
    TOKEN_API: str
    ADMIN_ID: str
    MASTER_ID: str
    start_message: str
    private_instagram_group: str
    WEBHOOK_HOST: str
    WEBHOOK_PATH: str
    WEBHOOK_URL: str
    WEBAPP_HOST: str
    WEBAPP_PORT: int


load_dotenv()

TOKEN_API = os.getenv('TOKEN_API')
ADMIN_ID = os.getenv('ADMIN_ID')
MASTER_ID = os.getenv('MASTER_ID')

start_message = os.getenv('start_message')
private_instagram_group = os.getenv('private_instagram_group')

# webhook settings
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = os.getenv('WEBAPP_HOST')
WEBAPP_PORT = os.getenv('WEBAPP_PORT')

data = Settings(TOKEN_API, ADMIN_ID, MASTER_ID, start_message, private_instagram_group, WEBHOOK_HOST, WEBHOOK_PATH,
                WEBHOOK_URL, WEBAPP_HOST, WEBAPP_PORT)
