from datetime import datetime
import logging
from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram import Dispatcher, Bot, executor

import DCode

logging.basicConfig(level=logging.INFO)

bot = Bot('5342747269:AAHkiT2x4afIzykaHA8DRId9lFdGf9NqxyE')
dp = Dispatcher(bot)

button_hi = KeyboardButton('/get') #тут текст кнопки пишешь 
greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_hi)
greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_hi)

@dp.message_handler(commands=['start', 'привет', 'Привет'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Здравствуй. Теперь ты будешь чувствовать сябя более информированным, чем был раньше.', reply_markup=greet_kb1) # сюад передаёшь


@dp.message_handler(commands=['help', 'помощь', 'команды', 'comands'])
async def help(message: types.Message):
    await bot.send_message(message.from_user.id, f'Все, что тебе нужно нажимать, дружок, это /get.')

@dp.message_handler(commands=['new_get'])
async def new_get(message: types.Message):
    await bot.send_message(message.from_user.id, get_new())

@dp.message_handler(commands=['get'])
async def get(message: types.Message):
    print(message.from_user)
    await bot.send_message(message.from_user.id, get_new())

def get_new() -> str:
    with open('message.txt', encoding='utf8') as f:
        last_time = int(f.readline())
        dif = int(datetime.now().timestamp())-last_time
        if dif < 10*60:
            return f.read()
    return DCode.main()

if __name__ == '__main__':
    executor.start_polling(dp)
