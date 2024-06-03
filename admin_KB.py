from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def admin_panel() -> ReplyKeyboardMarkup:


    kb = [[KeyboardButton(text="👑админ панель 👑")], [KeyboardButton(text="Услуги")], [KeyboardButton(text="Контакты")],
         [KeyboardButton(text="Расположение")], [KeyboardButton(text="Кредитные карты")], [KeyboardButton(text="Новости")],
         [KeyboardButton(text="Оформление кредита")], [KeyboardButton(text="Тарифы и комиссии")],[KeyboardButton(text="Актуальный курс валют")],
         [KeyboardButton(text="Интернет-банкинг")] ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard
async def button_panel():
    kb = [
        [KeyboardButton(text="Рассылка ✉️")],
        [KeyboardButton(text="Назад ⬅️⬅️")]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Админка"
    )
    return keyboard


async def button_back() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Назад ⬅️")]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )

    return keyboard
