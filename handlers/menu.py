from aiogram import types, F
from aiogram.filters import Command
from bot import dp
from keyboards import main_kb, ingame_kb
from handlers.game import start_game, user_state

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Выберите следующий шаг", reply_markup=main_kb)

@dp.message(F.text == "🕹 Начать игру")
async def on_start_game(message: types.Message):
    user_state[message.from_user.id] = []
    await message.answer("Игра начинаеться...", reply_markup=ingame_kb)
    await start_game(message)

@dp.message(F.text == "📖 Правила")
async def show_rules(message: types.Message):
    await message.answer("Правила игры следующие: 1. Никому не рассказывайте об этой игре.")

@dp.message(F.text == "⚙ Настройки")
async def show_settings(message: types.Message):
    await message.answer("Настроек пока нет.")

@dp.message(F.text == "🕹 Закончить игру")
async def on_start_game(message: types.Message):
    await message.answer("Игра заканчиваеться..", reply_markup=main_kb)

# @dp.message(F.text == "✍️ Написать свою историю")
# async def ask_user_story(message: types.Message):
#     if message.from_user.id in user_state:
#         await message.answer("Напишите свой фрагмент истории:")
#     else:
#         await message.answer("Сначала начните игру!")

# @dp.message()
# async def handle_user_story(message: types.Message):
#     if (
#         message.reply_to_message
#         and "Напишите свой фрагмент истории" in message.reply_to_message.text
#         and message.from_user.id in user_state
#     ):
#         history = user_state[message.from_user.id]
#         scene, options = continue_story(message.text, history)
#         text = f"{scene}\n" + "\n".join([f"- {opt}" for opt in options])
#         await message.answer(text)
