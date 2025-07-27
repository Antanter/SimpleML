from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🕹 Начать игру")],
        [KeyboardButton(text="📖 Правила"), KeyboardButton(text="⚙ Настройки")]
    ],
    resize_keyboard=True
)

ingame_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📖 Предметы"), KeyboardButton(text="⚙ Настройки")],
        [KeyboardButton(text="🕹 Закончить игру")],
    ],
    resize_keyboard=True
)

def generate_inline_keyboard(options):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=opt, callback_data=f"opt_{i}")]
            for i, opt in enumerate(options)
        ]
    )