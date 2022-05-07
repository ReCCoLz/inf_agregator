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
    try:
        while True:
            main.add_data_to_file()
            main.get_wordcloud()
            await asyncio.sleep(time)
    except:
        bot.send_message(config.owner_id, 'Произошла ошибка на сервере')

        

@dp.message_handler(commands=['start', 'привет', 'Привет'])
async def start(message: types.Message):
    if str(message.from_user.id) not in uselessdb.get_user_id():
        uselessdb.add_user_to_db(message.from_user.id)
    await bot.send_message(message.from_user.id, f'{config.hello_mes}')
    

@dp.message_handler(commands=['help', 'помощь', 'команды', 'comands'])
async def help(message: types.Message):
    await bot.send_message(message.from_user.id, f'{config.help_mes}')


@dp.message_handler(commands=['get', 'получить', 'облако', 'облако слов'])
async def send_pic(message = types.Message):
    path_to_photo = pathlib.Path('wordcloud.png')
    photo = types.InputFile(path_to_photo)
    await bot.send_photo(message.from_user.id, photo)


@dp.message_handler(commands=['rate'])
async def send_rate_words(message = types.Message):
    sens = ''
    k = 0
    flatten = [str(item) for sub in main.get_rate_words() for item in sub]
    for word in flatten:
        sens += word + ' '
        k += 1
        if k == 2:
            sens += '\n'
            k = 0
    await bot.send_message(message.from_user.id, f'{sens}')


@dp.message_handler(content_types=[types.ContentType.ANY])
async def send_news(message = types.Message):
    if len(message.text.split()) >= 2:
        word = message.text.split()[0]
        num = int(message.text.split()[1])
    else:
        word = message.text.split()[0]
        num = 5
    if word.isdigit():
        await bot.send_message(message.from_user.id, 'Число не является словом.')
    else:
        if message.text[0] == '/':
            await bot.send_message(message.from_user.id, 'Такой команды не существует.\nСписок доступных команд - /help')
        else:
            if 1 <= num <= 20:
                for sens in main.get_news_of_word(word, num):
                    await asyncio.sleep(0.5)
                    await bot.send_message(message.from_user.id, f'{sens}')
            else:
                await bot.send_message(message.from_user.id, 'Вы ввели число вне диапозона\n Диапозон от 1 до 20')

# loop.create_task(update_wordcloud())

if __name__ == '__main__':
    executor.start_polling(dp, loop=loop)
