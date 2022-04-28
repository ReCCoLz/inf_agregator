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

class A:
    def __init__(self, name) -> None:
        self.name = name
    
    def get_status(self, lastd: dict) -> str:
        if self.name not in lastd:
            self.status = 'NEW'
        else:
            ch = lastd.get(self.name)
            if ch > 0:
                self.status = '+'+str(ch)
            else:
                self.status = str(ch)

class B:
    def __init__(self, words:Words) -> None:
        self.all = [A(word.name) for word in words.all]

    def get_status(self, lastd: dict) -> None:
        for word in self.all:
            word.get_status(lastd)
    
    def __getitem__(self, key:int):
        return self.all[key]


class News:
    def __init__(self) -> None:
        self.rawtitles = []
        self.all = self.get_al()

    def get_al(self):  # долгая функция
        # не хочу  долго ждать, поэтому подставляю уже когда-то выданные этой функцией данные
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
    def __init__(self, words:B) -> None:
        self.read_last()
        self.words = words
        self.words.get_status(self.lastd)

    def read_last(self) -> dict:
        try:
            with open('last.txt', 'r') as f:
                swr = f.read()
            self.lastd = eval(swr)
        except:
            self.lastd = {}

    def write_to_file(self) -> None:
        swr = "{"
        for i in range(LOOKAT):
            swr += f"'{self.words[i].name}':{str(i)},"
        swr = swr[:-1]+'}'

        with open('last.txt', 'w', encoding='utf-8') as f:
            f.write(swr)

    def print(self) -> None:
        print('{0:_>2}|{1:_^13}|{2:_^13}'.format(" №", "слово", "перемещение"))

        for i in range(KVO):
            t = ''
            if self.words[i].status[0] == '+':
                t = '\033[0;42m'
            elif self.words[i].status[0] == '-':
                t = '\033[0;41m'
            else:
                t = '\033[0m'
            print(t+('{0:2d}|{1:13}|{2:^13}'.format(i+1,
                  self.words[i].name.upper(), self.words[i].status))+'\033[0m')

    def get_grouwth_word(self) -> Word:
        uppp = -1
        ind = -1

        for i in range(KVO):
            if self.words[i].status == 'NEW':
                ind = i
                break
            else:
                tem = int(self.words[i].status)
                if tem > uppp:
                    uppp = tem
                    ind = i
        return Word(self.words[ind].name, self.words[i].status)


while True:
    news = News()

    words: Words = news.get_all_words()
    b = B(words)
    data = Data(b)
    # os.system(CLEAR_COMMAND)
    data.print()
    data.write_to_file()

    # time.sleep(77)

    # Определяем самое поднявшееся слово
    grouwth_word = data.get_grouwth_word()
    # print(f'Рост {grouwth_word.status} показало слово "{grouwth_word.name}"')

    # печатаем новости со словом, показавшим рост
    for new in news.find_news_by_word(grouwth_word.name, 6):
        print(new)

    time.sleep(30)
