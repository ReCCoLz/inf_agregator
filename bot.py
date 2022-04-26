import asyncio
from webbrowser import get
from aiogram import Dispatcher, types, Bot 
from aiogram.utils import executor
import config 
import logging
from test import get_data

logging.basicConfig(level = logging.INFO)

bot = Bot(token=config.token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, 'Привет!')

@dp.message_handler(commands=['data'])
async def send_data(message: types.Message):
    MESS_MAX_LENGTH = 4096 #максимальная длинна сообщения 
    mes = ''
    for sent in get_data():
        mes += sent + '.\n\n' 
    for x in range(0, len(mes), MESS_MAX_LENGTH): #делим сообщения на части
        cut_mess = mes[x: x + MESS_MAX_LENGTH]
        await bot.send_message(message.chat.id, cut_mess)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
