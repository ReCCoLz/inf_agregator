import main
import pymorphy2
from pyparsing import rest_of_line

morph = pymorphy2.MorphAnalyzer(lang='ru')
atrib = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']


print(atrib[:3])