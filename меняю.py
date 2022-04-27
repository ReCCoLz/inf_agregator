#!/usr/bin/env python3
#coding:utf8

import requests, re
import os, time
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

KVO = 10 # Количество отслеживаемых слов
MINLEN = 5 # Минимальная длинка слов
LOOKAT = 50 # Количество слов, учитываемых в статистике
URLIST = {'https://news.yandex.ru/':'data-counter=".*">(.*?)</a></h2>',
    'https://news.mail.ru/?from=menu':'photo__title photo__title_new photo__title_new_hidden.*?">(.*?)</span>',
    # 'https://ria.ru/':'<meta itemprop="name" content="(.*?)"><span',
    'https://www.rbc.ru/':'<span class="news-feed__item__title">\n\ *(.*?)\n',
    # 'http://www.vesti.ru/':'<h3 class="b-item__title"><a href=".*?">(.*?)</a> </h3>',
    'https://news.rambler.ru/?utm_source=head&utm_campaign=self_promo&utm_medium=nav&utm_content=main':'data-blocks="teaser::[0987654321]+::content">\n([^><"/]*?)\n',
    'https://rg.ru/':'<span class="b-link__inner-text">(.*?)</span>',
    'http://www.interfax.ru':'<a href=".*?" data-vr-headline>(.*?)</a></H3></div>'}

CLEAR_LIST = ['.',',',':','»','«', '"']

CLEAR_COMMAND: str = {
    'nt': 'cls',
    'posix': 'clear'
}.get(os.name, lambda x: None)

def clear_str(s1, li):
        s2 = s1
        for iii in li:
            s2 = s2.replace(iii,'')
        return s2.lower()


class News:
    def __init__(self) -> None:
        self.rawtitles = []
        self.all = self.get_al()
    
    def get_al(self):  # долгая функция
        al = ''
        for i in URLIST.keys():
            s = self.parce(i,URLIST[i])
            if s == 'FIASCO':
                s = self.parce(i,URLIST[i])
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

    def find_news_by_word(self, word, limit = 6):
        cococo = 0
        for i in self.rawtitles:
            ii = []
            for j in clear_str(i, CLEAR_LIST).split():
                ii.append(morph.parse(j)[0].normal_form)
            if word in ii:
                yield i
                cococo +=1
            if cococo >= limit:
                break

class Data:
    def __init__(self, news: News) -> None:
        self.words_dict: dict = self.transform_news_to_dict(news)

    def transform_news_to_dict(self, news: News):
        di = {}
        for ii in news.all.split():
            p = morph.parse(ii)[0]
            # смотрим только существительные
            if p.tag.POS in ['NOUN']: # ,'VERB','INFN']:
                i = p.normal_form
                if len(i)>=MINLEN:
                    if di.get(i, -1)<0:
                        di[i] = 1
                    else:
                        di[i] = di[i] + 1
        return di
    
    def get_ans(self):
        self.words_dict['0'] = 0
        ans = ['0']*(LOOKAT +1)
        for i in self.words_dict.keys():
            for j in range(LOOKAT):
                ind = LOOKAT-j-1
                if self.words_dict[i] >= self.words_dict[ans[ind]]:
                    ans[ind+1] = ans[ind]
                    ans[ind] = i
        return ans

class A:
    def __init__(self, ans) -> None:
        self.read_last()
        self.ans = ans
        self.status = self.get_status()
        
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
            swr += f"'{self.ans[i]}':{str(i)},"
        swr = swr[:-1]+'}'

        with open('last.txt','w', encoding='utf-8') as f:
            f.write(swr)
    
    def get_status(self) -> dict:
        status = {}
        for i in range(KVO):
            ch = self.lastd.get(self.ans[i], -1337) - i
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
            print(t+('{0:2d}|{1:13}|{2:^13}'.format(i+1, self.ans[i].upper(), self.status[i]))+'\033[0m')



while True:
    news = News()
    data = Data(news)
    ans = data.get_ans()
    
    a = A(ans)
    status = a.get_status()
    os.system(CLEAR_COMMAND)
    a.draw()
    a.write()
    
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
    print(f'Рост {status[ind]} показало слово "{ans[ind]}"')

    # печатаем новости со словом, показавшим рост
    for new in news.find_news_by_word(ans[ind], 6): print(new)
        
    time.sleep(30)
    
