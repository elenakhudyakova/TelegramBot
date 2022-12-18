from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import *
from extensions import APIException, Convertor
from config import *
from token2 import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    text = "Привет! Для получения информации о валютах, доступных для конвертации введите команду /values"
    await bot.send_message(message.chat.id, text)


@dp.message_handler(commands=['values'])
async def values(message: types.Message):
    text = 'Доступные валюты перечислены ниже (наименования конвертируемой валюты, валюты, в которую конвертировать и сумма вводятся через пробел):'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    await message.reply(text)


@dp.message_handler(content_types=['text'])
async def converter(message: types.Message):
    try:
        base_key, sym_key, amount = message.text.split()
    except ValueError as e:
        await message.reply('Неверное количество параметров')

    try:
        new_price = Convertor.get_price(base_key, sym_key, amount)
        await message.reply(f"Цена {amount} {base_key} в {sym_key} : {new_price}")
    except APIException as e:
        await message.reply( f"Ошибка в команде:\n{e}" )


if __name__ == '__main__':
    executor.start_polling(dp)
