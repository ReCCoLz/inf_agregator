import pymorphy2
import requests, re
from fake_useragent import UserAgent
from lxml import html

urls = {
    'https://www.interfax.ru/news/' : '<a href=\"/\w+/\d{6,}\"><h3>\D+</h3>',
    'https://ria.ru/': '<span class=\"cell-list__item-title\">\D+/span>',
    'https://news.mail.ru/politics/': '<span class=\"newsitem__title-inner\">\D+</span>',
    'https://www.rbc.ru/politics/?utm_source=topline':'<span class=\"item__title rm-cm-item-text\"\D+</span>',
    'https://rg.ru/news.html' : '<span class=\"b-link__inner-text\">\D+</span>'
}

def get_data():
    ua = UserAgent()

    fild_data = []

    headers = {
        'User-Agent': f'{ua.random}',
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers' }

    for url in urls.items():
        r = requests.get(url[0], headers=headers)
        # print(r.text)
        match = re.findall(url[1], r.text)
        if 'h3' in match[0]:
             for data in match:     
                tree = html.fromstring(data)
                text = tree.cssselect('h3:first_child') # костыль для получения текста из под тега html
                fild_data.append(text[0].text_content().strip())
        if 'span' in match[0]:
             for data in match:
                tree = html.fromstring(data)
                text = tree.cssselect('span:first_child') # костыль для получения текста из под тега html
                fild_data.append(text[0].text_content().replace('\xa0', ' ').replace('\u200b', '').strip())
        if 'div' in match[0]:
                tree = html.fromstring(data)
                text = tree.cssselect('div:first_child') # костыль для получения текста из под тега html
                fild_data.append(text[0].text_content().strip())
    return fild_data

print(len(get_data()))
print(get_data())
