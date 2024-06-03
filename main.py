import asyncio
import logging
import xml.etree.ElementTree as ET

import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from admin_KB import *
from config import *
from db import *
from user_KB import *

logging.basicConfig(level=logging.INFO)
bot=Bot(token=API_TOKEN_CFG)
dp=Dispatcher()


class OrderFood(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()
    choosing_food_fize = State()
    first_start_vibor_group = State()
    glav_menu = State()
    choose_group = State()
    input_teacher = State()
    input_my_teacher_group = State()
    choosing_food_fize1 = State()


class admin(StatesGroup):
    send_all = State()


@dp.message(Command("start"))
async def start(message: types.Message):
    user1=message.from_user.id
    user1_name=message.from_user.last_name
    if await check_user(user1):
        if message.from_user.id in ADMIN_ID:
            mar = await admin_panel()
            photo_path = 'img/image.jpg'
            photo = FSInputFile(photo_path)
            await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=start_text)
            await bot.send_message(message.from_user.id, "Админка", reply_markup=mar)
        else:
            keyboard = await first_start_kb()
            photo_path = 'img/image.jpg'
            photo = FSInputFile(photo_path)
            await bot.send_photo(chat_id=message.chat.id, photo=photo)
            await message.answer(start_text, reply_markup=keyboard)
    else:
        await add_user(user1, user1_name)
        if message.from_user.id in ADMIN_ID:
            mar = await admin_panel()
            photo_path = 'img/image.jpg'
            photo = FSInputFile(photo_path)
            await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=start_text)
            await bot.send_message(message.from_user.id, "Админка", reply_markup=mar)
        else:
            keyboard = await first_start_kb()
            photo_path = 'img/image.jpg'
            photo = FSInputFile(photo_path)
            await bot.send_photo(chat_id=message.chat.id, photo=photo)
            await message.answer(start_text, reply_markup=keyboard)


@dp.message(Command("help"))
async def any_message(message: types.Message, state: FSMContext):
    keyboard=await button_help()
    mar=keyboard
    await bot.send_message(message.from_user.id, f"{help_text}", reply_markup=mar)




@dp.message(F.text == "Как открыть счет в вашем банке?", )
async def uslug_commands1(message: types.Message):
    await message.reply(f"{help1}")

@dp.message(F.text == "Какие документы необходимы для открытия счета?", )
async def uslug_commands2(message: types.Message):
    await message.reply(f"{help2}")

@dp.message(F.text == "Как узнать баланс по карте?", )
async def uslug_commands3(message: types.Message):
    await message.reply(f"{help3}")

@dp.message(F.text == "Как оформить кредит?", )
async def uslug_commands4(message: types.Message):
    await message.reply(f"{help4}")

@dp.message(F.text == "Как изменить лимит по карте?", )
async def uslug_commands5(message: types.Message):
    await message.reply(f"{help5}")

@dp.message(F.text == "Как рассчитать кредит?", )
async def uslug_commands6(message: types.Message):
    await message.reply(f"{help6}")

@dp.message(F.text == "Как рассчитать ипотеку?", )
async def uslug_commands7(message: types.Message):
    await message.reply(f"{help7}")

@dp.message(F.text == "Как узнать актуальный курс валют?", )
async def uslug_commands8(message: types.Message):
    await message.reply(f"{help8}")

@dp.message(F.text == 'Задать вопрос оператору')
async def support(message: types.Message, state: FSMContext):
    await state.set_state(OrderFood.choosing_food_name)
    await message.answer("Напишите ваш вопрос:")

@dp.message(OrderFood.choosing_food_name)
async def process_question(message: types.Message, state: FSMContext):
    user_id=(message.from_user.id)
    question=message.text
    await add_question(user_id, question)
    builder=InlineKeyboardBuilder()
    builder.button(text="Ответить", callback_data="answer")
    builder.button(text="Отклонить", callback_data="decline")

    for ADMIN_ID1 in ADMIN_ID:
     await bot.send_message(ADMIN_ID1, f"Новый вопрос от пользователя {user_id}:\n\n{question}",
                           reply_markup=builder.as_markup())
    await state.clear()
    await message.answer("Ваш вопрос отправлен в оператору. Ожидайте ответа.")


@dp.callback_query(F.data == 'answer')
async def handle_admin_commands(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.message.chat.id, f"Напишите ответ ")
    await state.set_state(OrderFood.choosing_food_fize)


@dp.message(OrderFood.choosing_food_fize)
async def process_question(message: types.Message,state: FSMContext
                           ):
    questions=await get_pending_questions()
    question=message.text
    if questions:
        for q in questions:
            await update_question_status(q[1], 'answered')
            await bot.send_message(q[1], f"Ответ от оператора:\n{question}")
            await message.answer(f"Ответ отправлен пользователю {q[1]}.")
            await state.clear()
            await start(message)
            break


@dp.callback_query(F.data == 'decline')
async def handle_admin_commands1(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.message.chat.id, f"Напишите ответ ")
    await state.set_state(OrderFood.choosing_food_fize1)


@dp.message(OrderFood.choosing_food_fize1)
async def process_question1(message: types.Message):
    questions=await get_pending_questions()
    question=message.text
    if questions:
        for q in questions:
            await update_question_status(q[1], 'declined')
            await bot.send_message(q[1], f"Ваш вопрос #{q[1]} был отклонен. Причина: {question}")
            await message.answer(f"Вопрос #{q[1]} отклонен.")
            await start(message)
            break


@dp.message(F.text == "Услуги")
async def uslug(message: types.Message):
    builder=InlineKeyboardBuilder()
    builder.button(text="Подробнее об услугах", callback_data="uslugi")
    await message.reply(f"{uslug_text}", reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'uslugi')
async def uslug_commands(callback: types.CallbackQuery, state: FSMContext):
    mar = await uslug1()
    await bot.send_message(callback.message.chat.id, f"{full_uslug_text}",reply_markup=mar)

@dp.message(F.text == "Кредитование", )
async def uslug_commands(message: types.Message):
    await message.reply(f"{kreditovanie}")

@dp.message(F.text == "Депозиты", )
async def uslug_commands(message: types.Message):
    await message.reply(f"{depozip}")

@dp.message(F.text == "Консультации", )
async def uslug_commands(message: types.Message):
    await message.reply(f"{kosult}")


@dp.message(F.text == "Контакты")
async def kontact(message: types.Message):
    builder=InlineKeyboardBuilder()
    builder.button(text="Подробнее об услугах", callback_data="full_kontact")
    await message.reply(f"{kontact_text}", reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'full_kontact')
async def kontact_commands(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.message.chat.id, f"{full_kontact_text}")


@dp.message(F.text == "Расположение")
async def kontact(message: types.Message):
    builder=InlineKeyboardBuilder()
    builder.button(text="Полный адрес и карта", callback_data="full_rasporaz")
    await message.reply(f"{rasporaz_text}", reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'full_rasporaz')
async def handle_admin_commands(callback: types.CallbackQuery, state: FSMContext):
    mar = await rasporaz_kb()
    await bot.send_message(callback.message.chat.id, f"{full_rasporaz_text}", reply_markup=mar)

@dp.message(F.text == "На метро")
async def kontact(message: types.Message):
    await bot.send_message(message.from_user.id, f"{raspoloz1}")

@dp.message(F.text == "На автобусе")
async def kontact(message: types.Message):
    await bot.send_message(message.from_user.id, f"{raspoloz2}")

@dp.message(F.text == "На автомобиле")
async def kontact(message: types.Message):
    await bot.send_message(message.from_user.id, f"{raspoloz3}")


@dp.message(F.text == "Кредитные карты")
async def kontact(message: types.Message):
    builder=InlineKeyboardBuilder()
    builder.button(text="Подробнее о картах", callback_data="full_kart")
    await message.reply(f"{kart_text}", reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'full_kart')
async def handle_admin_commands(callback: types.CallbackQuery, state: FSMContext):
    builder=InlineKeyboardBuilder()
    builder.button(text="Классическая карта", callback_data="kart1")
    builder.button(text="Золотая карта", callback_data="kart2")
    builder.button(text="Платиновая карта", callback_data="kart3")

    await bot.send_message(callback.message.chat.id, f"{full_kart_text}", reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'kart1')
async def handle_admin_commands(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.message.chat.id, f"{classic_kart}")

@dp.callback_query(F.data == 'kart2')
async def handle_admin_commands(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.message.chat.id, f"{gold_rart}")

@dp.callback_query(F.data == 'kart3')
async def handle_admin_commands(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.message.chat.id, f"{platium_kart}")

@dp.message(F.text == "Новости")
async def kontact(message: types.Message):
    builder=InlineKeyboardBuilder()
    builder.button(text="Читать новости", callback_data="full_novosti")
    await message.reply(f"{novosti_text}", reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'full_novosti')
async def handle_admin_commands(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.message.chat.id, f"{full_novosti_text}")


@dp.message(F.text == "Оформление кредита")
async def kontact(message: types.Message):
    builder=InlineKeyboardBuilder()
    builder.button(text="Подробнее о кредитах", callback_data="full_off_cridit")
    await message.reply(f"{cridit_text}", reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'full_off_cridit')
async def handle_admin_commands(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.message.chat.id, f"{full_cridit_text}")


@dp.message(F.text == "Тарифы и комиссии")
async def kontact(message: types.Message):
    builder=InlineKeyboardBuilder()
    builder.button(text="Подробнее о тарифах", callback_data="full_tariv")
    await message.reply(f"{tariv_text}", reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'full_tariv')
async def handle_admin_commands(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.message.chat.id, f"{full_tariv_text}")


@dp.message(F.text == "Интернет-банкинг")
async def kontact(message: types.Message):
    builder=InlineKeyboardBuilder()
    builder.button(text="Подробнее об интернет-банкинге", callback_data="full_barcing")
    await message.reply(f"{barcing_text}", reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'full_barcing')
async def handle_admin_commands(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.message.chat.id, f"{full_barcing_text}")



@dp.message(F.text == "Назад ⬅️⬅️")
async def backback(message: types.Message, bot: Bot):
    await start(message)

@dp.message(F.text == "Назад ⬅️⬅️.")
async def back(message: types.Message, bot: Bot):
    await keurs_v(message, bot)

@dp.message(F.text == "Назад ⬅️")
async def back(message: types.Message, bot: Bot):
    await sendALL1(message, bot)


@dp.message(F.text == "👑админ панель 👑", )
async def sendALL1(message: types.Message, bot: Bot):
    if message.from_user.id in ADMIN_ID:
        mar = await button_panel()
        await bot.send_message(message.from_user.id,"админ панель", reply_markup=mar)


@dp.message(F.text == "Рассылка ✉️", )  # get raspisanie
async def sendALL(message: types.Message, state, bot: Bot):
    if message.from_user.id in ADMIN_ID:
        mar=await button_back()
        await bot.send_message(message.from_user.id, "Введите сообщение для рассылки ✉️", reply_markup=mar)
        await state.set_state(admin.send_all)


@dp.message(admin.send_all)
async def sendALL(message: types.Message, bot: Bot):
    if message.from_user.id in ADMIN_ID:
        asd=await export_users()
        text=message.text
        mar=await button_back()
        for i in asd:
            try:
                await bot.send_message(i, f"{text}", reply_markup=mar)
                print("ОТправилось")
            except Exception:
                pass


async def main():
    if drop_db_CFG == True:
        await drop_db_USER()
        await drop_db_question()
        await init_db()
        await create_db()
        await dp.start_polling(bot)
    elif drop_db_CFG == False:
        await init_db()
        await create_db()
        await dp.start_polling(bot)

@dp.message(F.text == "Обновить")
async def back(message: types.Message, bot: Bot):
    await exchange_command(message)


@dp.message(F.text == "Актуальный курс валют")
async def keurs_v(message: types.Message, bot: Bot):
    mar = await kurs1()
    await message.answer("тут можно посмоттреть основные курсы",reply_markup=mar)

# ', 'EUR', 'GBP', 'JPY', 'AUD', 'CZK
@dp.message(F.text == "Обновить USD")
async def back1(message: types.Message, bot: Bot):
    await exchange21(message)

@dp.message(F.text == "Обновить EUR")
async def back2(message: types.Message, bot: Bot):
    await exchange22(message)

@dp.message(F.text == "Обновить GBP")
async def back3(message: types.Message, bot: Bot):
    await exchange23(message)

@dp.message(F.text == "Обновить JPY")
async def back4(message: types.Message, bot: Bot):
    await exchange25(message)

@dp.message(F.text == "Обновить AUD")
async def back5(message: types.Message, bot: Bot):
    await exchange24(message)

@dp.message(F.text == "Обновить CZK")
async def back6(message: types.Message, bot: Bot):
    await exchange26(message)

@dp.message(F.text == "USD")
async def exchange21(message: types.Message):
    url="https://www.cbr-xml-daily.ru/daily_utf8.xml"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await message.answer("Ошибка при получении данных.")
                return
            data=await response.text()

    root=ET.fromstring(data)

    # Список валют для отображения
    target_currencies=['USD']

    rates=[]
    for valute in root.findall('Valute'):
        char_code=valute.find('CharCode').text
        if char_code in target_currencies:
            name=valute.find('Name').text
            value=valute.find('Value').text
            rates.append(f"Курс {name} ({char_code}): {value} руб.")
        mar = await kurs_USD()
    await message.answer("\n".join(rates),reply_markup=mar)

@dp.message(F.text == "EUR")
async def exchange22(message: types.Message):
    url="https://www.cbr-xml-daily.ru/daily_utf8.xml"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await message.answer("Ошибка при получении данных.")
                return
            data=await response.text()

    root=ET.fromstring(data)

    # Список валют для отображения
    target_currencies=['EUR']

    rates=[]
    for valute in root.findall('Valute'):
        char_code=valute.find('CharCode').text
        if char_code in target_currencies:
            name=valute.find('Name').text
            value=valute.find('Value').text
            rates.append(f"Курс {name} ({char_code}): {value} руб.")
        mar = await kurs_EUR()
    await message.answer("\n".join(rates),reply_markup=mar)

@dp.message(F.text == "GBP")
async def exchange23(message: types.Message):
    url="https://www.cbr-xml-daily.ru/daily_utf8.xml"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await message.answer("Ошибка при получении данных.")
                return
            data=await response.text()

    root=ET.fromstring(data)

    # Список валют для отображения
    target_currencies=['GBP']

    rates=[]
    for valute in root.findall('Valute'):
        char_code=valute.find('CharCode').text
        if char_code in target_currencies:
            name=valute.find('Name').text
            value=valute.find('Value').text
            rates.append(f"Курс {name} ({char_code}): {value} руб.")
        mar=await kurs_GBP()
    await message.answer("\n".join(rates), reply_markup=mar)

@dp.message(F.text == "AUD")
async def exchange24(message: types.Message):
    url="https://www.cbr-xml-daily.ru/daily_utf8.xml"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await message.answer("Ошибка при получении данных.")
                return
            data=await response.text()

    root=ET.fromstring(data)

    # Список валют для отображения
    target_currencies=['AUD']

    rates=[]
    for valute in root.findall('Valute'):
        char_code=valute.find('CharCode').text
        if char_code in target_currencies:
            name=valute.find('Name').text
            value=valute.find('Value').text
            rates.append(f"Курс {name} ({char_code}): {value} руб.")
        mar=await kurs_AUD()
    await message.answer("\n".join(rates), reply_markup=mar)


@dp.message(F.text == "JPY")
async def exchange25(message: types.Message):
    url="https://www.cbr-xml-daily.ru/daily_utf8.xml"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await message.answer("Ошибка при получении данных.")
                return
            data=await response.text()

    root=ET.fromstring(data)

    # Список валют для отображения
    target_currencies=['JPY']

    rates=[]
    for valute in root.findall('Valute'):
        char_code=valute.find('CharCode').text
        if char_code in target_currencies:
            name=valute.find('Name').text
            value=valute.find('Value').text
            rates.append(f"Курс {name} ({char_code}): {value} руб.")
        mar=await kurs_JPY()
    await message.answer("\n".join(rates), reply_markup=mar)

@dp.message(F.text == "CZK")
async def exchange26(message: types.Message):
    url="https://www.cbr-xml-daily.ru/daily_utf8.xml"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await message.answer("Ошибка при получении данных.")
                return
            data=await response.text()

    root=ET.fromstring(data)

    # Список валют для отображения
    target_currencies=['CZK']

    rates=[]
    for valute in root.findall('Valute'):
        char_code=valute.find('CharCode').text
        if char_code in target_currencies:
            name=valute.find('Name').text
            value=valute.find('Value').text
            rates.append(f"Курс {name} ({char_code}): {value} руб.")
        mar=await kurs_CZK()
    await message.answer("\n".join(rates), reply_markup=mar)


@dp.message(Command("exchange"))
async def exchange_command(message: types.Message):
    url="https://www.cbr-xml-daily.ru/daily_utf8.xml"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await message.answer("Ошибка при получении данных.")
                return
            data=await response.text()

    root=ET.fromstring(data)

    # Список валют для отображения
    target_currencies=['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CZK']

    rates=[]
    for valute in root.findall('Valute'):
        char_code=valute.find('CharCode').text
        if char_code in target_currencies:
            name=valute.find('Name').text
            value=valute.find('Value').text
            rates.append(f"Курс {name} ({char_code}): {value} руб.")
        mar = await kurs()
    await message.answer("\n".join(rates),reply_markup=mar)


@dp.message(Command("credit"))
async def credit_command(message: types.Message):
    try:
        args=message.text.split()[1:]  # Получаем аргументы команды
        if len(args) != 3:
            raise ValueError
        await calculate_credit_or_ipoteka(message, args)
    except (IndexError, ValueError):
        await message.answer(
            "Некорректный формат данных. Пожалуйста, введите сумму, срок (в месяцах) и процентную ставку через пробел после команды.\nНапример: /credit 100000 12 10")


@dp.message(Command("ipoteka"))
async def ipoteka_command(message: types.Message):
    try:
        args=message.text.split()[1:]  # Получаем аргументы команды
        if len(args) != 3:
            raise ValueError
        await calculate_credit_or_ipoteka(message, args)
    except (IndexError, ValueError):
        await message.answer(
            "Некорректный формат данных. Пожалуйста, введите сумму, срок (в месяцах) и процентную ставку через пробел после команды.\nНапример: /ipoteka 3000000 240 7")


async def calculate_credit_or_ipoteka(message: types.Message, args):
    try:
        amount = float(args[0])
        term = int(args[1])
        rate = float(args[2]) / 100 / 12

        monthly_payment = (amount * rate) / (1 - (1 + rate) ** -term)
        total_payment = monthly_payment * term
        total_interest = total_payment - amount

        await message.answer(
            f"Ежемесячный платеж: {monthly_payment:.2f} руб.\nОбщая сумма выплат: {total_payment:.2f} руб.\nНачисленные проценты: {total_interest:.2f} руб.")
    except (IndexError, ValueError):
        await message.answer(
            "Некорректный формат данных. Пожалуйста, введите сумму, срок (в месяцах) и процентную ставку через пробел.")



if __name__ == "__main__":
    asyncio.run(main())
