__author__ = 'Bogdan'
__email__ = 'evstrat.bg@gmail.com'

import re
import os


def text_to_words(text):
    sentences = re.split(r'(?:[.]\s*){3}|[.?!]', text)
    return sentences


def word(sentence):
    return sentence.lower().split()


def collect_paths():
    paths = []
    for root, dirs, files in os.walk('.'):
        for fil in files:
            if fil.endswith('txt'):
                paths.append(root + '/' + fil)
    return paths


trigramms = set()
for path in collect_paths():
    f = open(path, 'r', encoding='utf8')
    f = f.read()
    for sent in text_to_words(f):
        for w in word(sent):
            stripped_word = w.strip('(»),*;&-»/…&”$:--/“«')
            if len(stripped_word) >= 3:
                if len(stripped_word) == 3:
                    trigramms.add(stripped_word)
                else:
                    s = 0
                    for i in range(3, len(stripped_word) + 1):
                        trigramms.add(stripped_word[s:i])
                        s += 1


def count_trigramms():
    d = {}
    for path in collect_paths():
        if path == './requirements.txt':
            continue
        for trigramm in trigramms:
            f = open(path, 'r', encoding='utf8')
            trigramm = re.sub('([)(-*])', '\\' + '\1', trigramm)
            # print(trigramm)
            finds = re.findall(trigramm, f.read(), flags=re.DOTALL)
            c = len(finds)
            if c > 0:
                if trigramm not in d:
                    d[trigramm] = 1
                else:
                    d[trigramm] += c
    return d


for k, v in sorted(count_trigramms(), key=lambda x: count_trigramms()[x], reverse=True)[:10]:
    print(k, v)
