from time import sleep
import requests, re
from requests import ConnectionError
from fake_useragent import UserAgent
from lxml import html
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
import pymorphy2
import wordcloud

morph = pymorphy2.MorphAnalyzer(lang='ru')



rus_stopwords = stopwords.words('russian')


urls = {
    'https://www.interfax.ru/news/' : '<a href=\"/\w+/\d{6,}\"><h3>\D+</h3>',
    'https://ria.ru/': '<span class=\"cell-list__item-title\">\D+/span>',
    'https://news.mail.ru/politics/': '<span class=\"newsitem__title-inner\">\D+</span>',
    'https://www.rbc.ru/politics/?utm_source=topline':'<span class=\"item__title rm-cm-item-text\"\D+</span>',
    'https://rg.ru/news.html' : '<span class=\"b-link__inner-text\">\D+</span>',
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
        try:
            r = requests.get(url[0], headers=headers)
        except ConnectionError:
            print('Ошибка соединеня')
            continue
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
            for data in match[0]:
                tree = html.fromstring(data)
                text = tree.cssselect('div:first_child') # костыль для получения текста из под тега html
                fild_data.append(text[0].text_content().strip())
    return fild_data


def add_data_to_file():
    with open('data_news.txt', 'w', encoding='utf-8') as f:
        for text in get_data():
            f.write(text)
            f.write('\n')


def get_data_from_file(filename='data_news.txt'):
    f = open(filename, encoding='utf-8')
    need_data = [i.strip() for i in f.readlines()]
    f.close()
    return need_data


def clear_data(): #оптимизировать эту залупу нужно
    res = ''
    sent = ''
    for text in get_data_from_file():
        sent = ''
        for j in text.lower().split():
                if j not in rus_stopwords:
                    j = j.replace(',','').replace('"', '')
                    tag_j = morph.parse(j)[0].tag
                    norm_j = morph.normal_forms(j)[0]
                    if 'NOUN' in tag_j:
                        sent += norm_j + ' '
        res += sent
    return res



def get_wordcloud(text_raw=clear_data()):
    wordcloud = WordCloud().generate(text_raw)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

get_wordcloud()

# f = open('data_news.txt', "r", encoding='utf-8')
# text=f.read()
# text = text.lower()
# spec_chars = string.punctuation + '\n'
# text = " ".join(ch for ch in text.split() if ch not in rus_stopwords)
# print(text)
