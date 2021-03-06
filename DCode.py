#!/usr/bin/env python3
# coding:utf8

from tkinter.tix import Tree
import requests
import re
import os
from datetime import datetime
import pymorphy2
import json

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
TEST = False
CLEAR_COMMAND: str = {
    'nt': 'cls',
    'posix': 'clear'
}.get(os.name)

def substidution(func):
    file_name = func.__name__+'.txt'
    def f(*args, **kwargs):
        if not TEST:
            return func(*args, **kwargs)
        if not os.path.exists(file_name):
            output = func(*args, **kwargs)
            with open(file_name, 'w', encoding='utf8') as file:
                file.write(json.dumps(output))
            return output
        with open(file_name, encoding='utf8') as f:
            return json.loads(f.read())
    return f


def clear_str(s1:str, li:list) -> str:
    s2 = s1
    for iii in li:
        s2 = s2.replace(iii, '')
    return s2.lower()


class Word:
    def __init__(self, name) -> None:
        self.name = name

    def define_status(self, lastd: dict) -> str:
        if self.name not in lastd:
            self.status = 'NEW'
        else:
            ch = lastd.get(self.name)
            if ch > 0:
                self.status = '+'+str(ch)
            else:
                self.status = str(ch)


class Words:
    def __init__(self, words: dict) -> None:
        words = sorted(words.items(), key=lambda x: x[1], reverse=True)[
            :LOOKAT]
        self.all = [Word(word[0]) for word in words]

    def define_words_status(self, lastd: dict) -> None:
        for word in self.all:
            word.define_status(lastd)

    def __getitem__(self, key: int):
        return self.all[key]


class News:
    def __init__(self) -> None:
        self.rawtitles = []
        self.all = self.get_al()

    @substidution
    def get_al(self) -> str:
        al = ''
        for i in URLIST.keys():
            s = self.parce(i, URLIST[i])
            if s == 'FIASCO':
                s = self.parce(i, URLIST[i])
            if s != 'FIASCO':
                al += s + ' '
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
        return Words(di)


class Data:
    def __init__(self, words: Words) -> None:
        self.read_last()
        self.words = words
        self.words.define_words_status(self.lastd)

    def read_last(self) -> dict:
        try:
            with open('last.txt', 'r', encoding='utf8') as f:
                swr = f.read()
            self.lastd = eval(swr)
        except:
            self.lastd = {}

    def write_to_file(self) -> None:
        swr = "{"
        for i in range(LOOKAT):
            swr += f"'{self.words[i].name}':{str(i)},"
        swr = swr[:-1]+'}'

        with open('last.txt', 'w', encoding='utf8') as f:
            f.write(swr)

    def __str__(self) -> str:
        result = '№ [перемещение] слово\n'

        for i in range(KVO):
            result += f'{i+1} [{self.words[i].status}] {self.words[i].name.upper()}\n'

        return result

    def get_grouwth_word(self) -> Word:
        uppp = -1

        for word in self.words[:KVO]:
            if word.status == 'NEW':
                return word
            tem = int(word.status)
            if tem > uppp:
                uppp = tem
                res = word
        return res

def main():
    result = ''

    news = News()

    words: Words = news.get_all_words()
    data = Data(words)
    result = str(data) + '\n'

    data.write_to_file()
    grouwth_word = data.get_grouwth_word()
    result += f'Рост {grouwth_word.status} показало слово "{grouwth_word.name}"\n\n'
    for new in news.find_news_by_word(grouwth_word.name, 6):
        result += f'"{new}"\n\n'

    with open('message.txt', 'w', encoding='utf8') as f:
        f.write(
            f'{int(datetime.now().timestamp())}\n{result}'
        )
    return result
    # time.sleep(30)
