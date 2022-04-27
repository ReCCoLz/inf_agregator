#!/usr/bin/env python3
# coding:utf8

import requests
import re
import os
import time
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

KVO = 10  # Количество отслеживаемых слов
MINLEN = 5  # Минимальная длинка слов
LOOKAT = 50  # Количество слов, учитываемых в статистике
URLIST = {'https://news.yandex.ru/': 'data-counter=".*">(.*?)</a></h2>',
          'https://news.mail.ru/?from=menu': 'photo__title photo__title_new photo__title_new_hidden.*?">(.*?)</span>',
          # 'https://ria.ru/':'<meta itemprop="name" content="(.*?)"><span',
          'https://www.rbc.ru/': '<span class="news-feed__item__title">\n\ *(.*?)\n',
          # 'http://www.vesti.ru/':'<h3 class="b-item__title"><a href=".*?">(.*?)</a> </h3>',
          'https://news.rambler.ru/?utm_source=head&utm_campaign=self_promo&utm_medium=nav&utm_content=main': 'data-blocks="teaser::[0987654321]+::content">\n([^><"/]*?)\n',
          'https://rg.ru/': '<span class="b-link__inner-text">(.*?)</span>',
          'http://www.interfax.ru': '<a href=".*?" data-vr-headline>(.*?)</a></H3></div>'}

CLEAR_LIST = ['.', ',', ':', '»', '«', '"']
TEST = True

CLEAR_COMMAND: str = {
    'nt': 'cls',
    'posix': 'clear'
}.get(os.name)


def clear_str(s1, li):
    s2 = s1
    for iii in li:
        s2 = s2.replace(iii, '')
    return s2.lower()


class Word:
    def __init__(self, name, status) -> None:
        self.name = name
        self.status = status


class Words:
    def __init__(self, **words) -> None:
        self.all = sorted(
            [Word(name, status) for name, status in words.items()],
            key=lambda word: word.status,
            reverse=True
        )[:LOOKAT]

    def get_names(self) -> list:
        return [word.name for word in self.all]


class News:
    def __init__(self) -> None:
        self.rawtitles = []
        self.all = self.get_al()

    def get_al(self):  # долгая функция
        if TEST:
            with open('News.get_al.output.txt') as f:
                return f.read()
        al = ''
        for i in URLIST.keys():
            s = self.parce(i, URLIST[i])
            if s == 'FIASCO':
                s = self.parce(i, URLIST[i])
            if s != 'FIASCO':
                al += s + ' '
        # with open('News.get_al.output.txt', 'w') as f:
        #     f.write(clear_str(al, CLEAR_LIST))
        return clear_str(al, CLEAR_LIST)

    def parce(self, url, regexp):
        s = 'FIASCO'
        try:
            r = requests.get(url)
            if r.status_code == 200:
                a = (re.findall(regexp, r.text))
                self.rawtitles += a
                s = ' '.join(a)
        except:
            pass
        return s

    def find_news_by_word(self, word, limit=6):
        cococo = 0
        for i in self.rawtitles:
            ii = []
            for j in clear_str(i, CLEAR_LIST).split():
                ii.append(morph.parse(j)[0].normal_form)
            if word in ii:
                yield i
                cococo += 1
            if cococo >= limit:
                break

    def get_all_words(self) -> Words:
        di = {}  # word: mentionability
        for ii in self.all.split():
            p = morph.parse(ii)[0]
            # смотрим только существительные
            if p.tag.POS in ['NOUN']:  # ,'VERB','INFN']:
                i = p.normal_form
                if len(i) >= MINLEN:
                    if di.get(i, -1) < 0:
                        di[i] = 1
                    else:
                        di[i] = di[i] + 1
        return Words(**di)


class Data:
    def __init__(self, words) -> None:
        self.read_last()
        self.words = words
        self.status = self.get_status()
        # print(self.words, self.status)

    def read_last(self) -> dict:
        try:
            with open('last.txt', 'r') as f:
                swr = f.read()
            self.lastd = eval(swr)
        except:
            self.lastd = {}

    def write(self) -> None:
        swr = "{"
        for i in range(LOOKAT):
            swr += f"'{self.words[i]}':{str(i)},"
        swr = swr[:-1]+'}'

        with open('last.txt', 'w', encoding='utf-8') as f:
            f.write(swr)

    def get_status(self) -> dict:
        status = {}
        for i in range(KVO):
            ch = self.lastd.get(self.words[i], -1337) - i
            if ch < -1000:
                status[i] = 'NEW'
            else:
                if ch > 0:
                    status[i] = '+'+str(ch)
                else:
                    status[i] = str(ch)
        return status

    def draw(self) -> None:
        print('{0:_>2}|{1:_^13}|{2:_^13}'.format(" №", "слово", "перемещение"))

        for i in range(KVO):
            t = ''
            if self.status[i][0] == '+':
                t = '\033[0;42m'
            elif self.status[i][0] == '-':
                t = '\033[0;41m'
            else:
                t = '\033[0m'
            print(t+('{0:2d}|{1:13}|{2:^13}'.format(i+1,
                  self.words[i].upper(), self.status[i]))+'\033[0m')


while True:
    news = News()

    words: Words = news.get_all_words()
    w_names = words.get_names()
    data = Data(
        w_names
    )
    words = data.words
    status = data.status
    # os.system(CLEAR_COMMAND)
    data.draw()
    data.write()

    time.sleep(77)

    # Определяем самое поднявшееся слово
    uppp = -1
    ind = -1

    for i in range(KVO):
        if status[i] == 'NEW':
            ind = i
            break
        else:
            tem = int(status[i])
            if tem > uppp:
                uppp = tem
                ind = i
    print(f'Рост {status[ind]} показало слово "{w_names[ind]}"')

    # печатаем новости со словом, показавшим рост
    for new in news.find_news_by_word(w_names[ind], 6):
        print(new)

    time.sleep(30)
