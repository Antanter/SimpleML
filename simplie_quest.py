from google import genai
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart

GEMINI_API_KEY = "AIzaSyDDexdfHji_aw8JzB747rdK-m4Ohvc9b50"
TELEGRAM_TOKEN = "8307611638:AAEECNiVEaxK5SmG3p0ZMk6UQ442VHp6hZU"

bot = Bot(token=TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)
dp = Dispatcher()

@dp.message()
async def ask_gemini(message: Message):
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=message.text,
    )

    MAX_LEN = 4096
    text = response.text
    for i in range(0, len(text), MAX_LEN):
        await message.answer(text[i:i + MAX_LEN])

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())