from aiogram import types, Router, F
import llm
from keyboards import generate_inline_keyboard
from bot import dp
from user_data import user_state

router = Router()
dp.include_router(router)

async def start_game(message: types.Message):
    user_state[message.from_user.id] = []
    await send_scene(message)

async def send_scene(message: types.Message, user_id=None):
    uid = user_id or message.from_user.id
    history = user_state[uid]
    text, options = await llm.generate_scene(history)

    user_state[uid].append(text + "\n")

    keyboard = generate_inline_keyboard(options)

    await message.answer(text, reply_markup=keyboard)

@router.callback_query(F.data.startswith("opt_"))
async def handle_choice(callback: types.CallbackQuery):
    uid = callback.from_user.id
    data = callback.data
    
    buttons = callback.message.reply_markup.inline_keyboard
    button_text = None
    for row in buttons:
        for button in row:
            if button.callback_data == data:
                button_text = button.text
                break
        if button_text:
            break
    if button_text is None:
        button_text = data

    user_state[uid].append(button_text + "\n")

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(button_text)
    await callback.answer()
    await send_scene(callback.message, user_id=uid)
