from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
