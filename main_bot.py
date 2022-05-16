import logging
from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram import Dispatcher, Bot, executor

from DCode import main

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

# @dp.message_handler(commands=['get'])
# async def get(message: types.Message):
#     print(message.from_user)
#     await bot.send_message(message.from_user.id, f'иди в жопу, ты мне мешаешь, я сейчас общаюсь не с тобой. как меня допилят, тебе сообщат')

@dp.message_handler(commands=['get'])
async def get(message: types.Message):
    print(message.from_user, '!!!!!NEW!!!!!')
    m = '''№ [перемещение] слово
 1| [___0] РОССИЯ   
 2| [__+1] ПУТИН     
 3| [__+2] УКРАИНА     
 4| [__+3] ЧЕЛОВЕК    
 5| [__+4] САНКЦИЯ      
 6| [NEW] МИШУСТИН  
 7| [NEW] ТУМИНАСА     
 8| [NEW] ПРЕМИЯ     
 9| [__+5] СТОЛКНОВЕНИЕ     
10|[__+6] ПОЕЗД    

Рост NEW показало слово "мишустин"

"Мишустин лишил режиссера Туминаса правительственной премии"

"Мишустин исключил Римаса Туминаса из лауреатов премии в области культуры"'''
    await bot.send_message(message.from_user.id, m)
    await bot.send_message(message.from_user.id, main())

if __name__ == '__main__':
    executor.start_polling(dp)

# № [перемещение] слово1 [0] РОССИЯ
# 2 [__+2] УКРАИНА
# 3 [__+1] ПУТИН
# 4 [_+11] ФИНЛЯНДИЯ
# 5 [NEW] МИШУСТИН
# 6 [NEW] ТУМИНАСА
# 7 [NEW] ПРЕМИЯ
# 8 [NEW] БОРРЕЛЬ
# 9 [NEW] ЗЕРНО
# 10 [NEW] ХРАНИЛИЩЕ

# Рост NEW показало слово "мишустин"
# Мишустин лишил режиссера Туминаса правительственной премии
# Мишустин исключил Римаса Туминаса из лауреатов премии в области культуры