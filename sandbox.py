import pymorphy2

morph = pymorphy2.MorphAnalyzer(lang='ru')

word = 'людей'
print(word.tag)

print(morph.parse(word)[0].tag)