from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import pathlib
import asyncio
import config
import main
import uselessdb    
import logging

 
logging.basicConfig(level=logging.INFO)
token = config.token 
loop = asyncio.get_event_loop()



bot = Bot(token)
dp = Dispatcher(bot)


async def update_wordcloud(time=600):
    while True:
        main.add_data_to_file()
        main.get_wordcloud()
        await asyncio.sleep(time)

        

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if str(message.from_user.id) not in uselessdb.get_user_id():
        uselessdb.add_user_to_db(message.from_user.id)
    await bot.send_message(message.from_user.id, f'{config.hello_mes}')
    

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await bot.send_message(message.from_user.id, f'{config.help_mes}')


@dp.message_handler(commands=['get'])
async def send_pic(message = types.Message):
    path_to_photo = pathlib.Path('wordcloud.png')
    photo = types.InputFile(path_to_photo)
    await bot.send_photo(message.from_user.id, photo)


loop.create_task(update_wordcloud())

if __name__ == '__main__':
    executor.start_polling(dp, loop=loop)
