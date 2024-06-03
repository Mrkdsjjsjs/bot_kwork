from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder






async def first_start_kb() -> ReplyKeyboardMarkup:


    kb = [[KeyboardButton(text="Услуги")], [KeyboardButton(text="Контакты")],
         [KeyboardButton(text="Расположение")], [KeyboardButton(text="Кредитные карты")],
         [KeyboardButton(text="Новости")],
         [KeyboardButton(text="Оформление кредита")], [KeyboardButton(text="Тарифы и комиссии")],
          [KeyboardButton(text="Актуальный курс валют")],
         [KeyboardButton(text="Интернет-банкинг")]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard

async def button_help() -> ReplyKeyboardMarkup:
    kb = [
    [KeyboardButton(text="Как открыть счет в вашем банке?")],
    [KeyboardButton(text="Какие документы необходимы для открытия счета?")],
    [KeyboardButton(text="Как узнать баланс по карте?")],
    [KeyboardButton(text="Как оформить кредит?")],
        [KeyboardButton(text="Как изменить лимит по карте?")],
        [KeyboardButton(text="Как рассчитать кредит?")],
        [KeyboardButton(text="Как рассчитать ипотеку?")],
        [KeyboardButton(text="Как узнать актуальный курс валют?")],
        [KeyboardButton(text="Задать вопрос оператору")],
        [KeyboardButton(text="Назад ⬅️⬅️")]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )

    return keyboard

async def button_back() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Назад ⬅️")]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    return keyboard



async def uslug1() -> ReplyKeyboardMarkup:


    kb = [[KeyboardButton(text="Кредитование")], [KeyboardButton(text="Депозиты")],
         [KeyboardButton(text="Консультации")], [KeyboardButton(text="Назад ⬅️⬅️")]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard


async def kurs() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Обновить")],
        [KeyboardButton(text="Назад ⬅️⬅️")]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    return keyboard

async def rasporaz_kb() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="На метро")],
        [KeyboardButton(text="На автобусе")],
        [KeyboardButton(text="На автомобиле")],
        [KeyboardButton(text="Назад ⬅️⬅️")]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    return keyboard

async def kurs1() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="USD")],
        [KeyboardButton(text="EUR")],
        [KeyboardButton(text="GBP")],
        [KeyboardButton(text="JPY")],
        [KeyboardButton(text="AUD")],
        [KeyboardButton(text="CZK")],
        [KeyboardButton(text="Назад ⬅️⬅️")]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    return keyboard


async def kurs_USD() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Обновить USD")],
        [KeyboardButton(text="Назад ⬅️⬅️.")]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    return keyboard

async def kurs_EUR() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Обновить EUR")],
        [KeyboardButton(text="Назад ⬅️⬅️.")]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    return keyboard

async def kurs_GBP() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Обновить GBP")],
        [KeyboardButton(text="Назад ⬅️⬅️.")]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    return keyboard

async def kurs_JPY() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Обновить JPY")],
        [KeyboardButton(text="Назад ⬅️⬅️.")]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    return keyboard

async def kurs_AUD() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Обновить AUD")],
        [KeyboardButton(text="Назад ⬅️⬅️.")]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    return keyboard

async def kurs_CZK() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Обновить CZK")],
        [KeyboardButton(text="Назад ⬅️⬅️.")]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    return keyboard
