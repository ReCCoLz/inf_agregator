    # Словарь "ссылка":"регулярное выражение"
urlist = {'https://news.yandex.ru/':'data-counter=".*">(.*?)</a></h2>',
'https://news.mail.ru/?from=menu':'photo__title photo__title_new photo__title_new_hidden.*?">(.*?)</span>',
'https://ria.ru/':'<meta itemprop="name" content="(.*?)"><span',
'https://www.rbc.ru/':'<span class="news-feed__item__title">\n\ *(.*?)\n',
    # 'http://www.vesti.ru/':'<h3 class="b-item__title"><a href=".*?">(.*?)</a> </h3>',
'https://news.rambler.ru/?utm_source=head&utm_campaign=self_promo&utm_medium=nav&utm_content=main':'data-blocks="teaser::[0987654321]+::content">\n([^><"/]*?)\n',
'https://rg.ru/':'<span class="b-link__inner-text">(.*?)</span>',
'http://www.interfax.ru':'<a href=".*?" data-vr-headline>(.*?)</a></H3></div>'}

token = '5197195042:AAEKvG9uJ1NQi150GTnTNRpSiIt_3TP7aao'

owner_id = 1740400965


hello_mes = """Здравствуй, Я - Агрегатор Новостей
Чтобы получить мой список команд - напиши /help"""

help_mes = """
Вот мой список команд: 
    /help - список команд бота
    /start - стартовое сообщение 
    /get - получить текущее "облако слов"
    /rate - рейтинг слов текущих новостей

Если вы напишите любое слово, то получите список новостей, в которых упоминается данное слово.\n
По умолчанию выводится 5 новостей, но это число можно изменить, добавив после интересующего вас слова
любое в диапозоне от 1 до 20. 

Например:
    Россия 3
    Ес 5
    Сша 9
    Море 20
"""