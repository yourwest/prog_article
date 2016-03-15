import re
import os
import numpy as np
# import matplotlib.pyplot as plt

all_paths = ['./471/', './66/', './26/']

def text_to_words(text):
    text = re.sub('[1-9a-zA-Z]|0|#|,|\.|\{|:|\(|\)|\}|\]|\[|;|=|&|\||!|\?|"|\'|/|_|»|«|–|-|—|\*', '', text)
    sentences = re.split(r'(?:[.]\s*){3}|[.?!]', text)
    return sentences


def word(sentence):
    return sentence.lower().split()

# Собираем все триграммы из всех текстов.
# Здесь и дальше все переменные названы для триграмм, потому что мы сначала рассматривали только их,
# а биграммы и четырех граммы добавили потом.
def collect_trigrams(paths):
    all_texts = ''
    trigramms = set()
    #fourgrams_list = open('fourgrams_list.csv', 'w', encoding='utf-8')
    #trigrams_list = open('trigrams_list.csv', 'w', encoding='utf-8')
    #bigrams_list = open('trigrams_list.csv', 'w', encoding='utf-8')
    for path in paths:
        files = os.listdir(path=path)
        for file_name in files:
            if file_name.endswith('.txt'):
                f = open(path + file_name, 'r', encoding='utf8')
                f = f.read()
                for sent in text_to_words(f):
                    for w in word(sent):
                        all_texts += w
                        all_texts += ' '
                        stripped_word = w.strip('(»),*;&-»/…&”$:--/“«')
                        if len(stripped_word) >= 3:
                            if len(stripped_word) == 3:
                                trigramms.add(stripped_word)
                                #fourgrams_list.write(stripped_word + ';')
                                #trigrams_list.write(stripped_word + ';')
                                #bigrams_list.write(stripped_word + ';')
                            else:
                                s = 0
                                for i in range(3, len(stripped_word) + 1):
                                    trigramms.add(stripped_word[s:i])
                                    #fourgrams_list.write(stripped_word[s:i] + ';')
                                    #trigrams_list.write(stripped_word[s:i] + ';')
                                    #bigrams_list.write(stripped_word[s:i] + ';')
                                    s += 1
    #fourgrams_list.close()
    #trigrams_list.close()
    #bigrams_list.close()                                
    freqs = []
    final_trigrams = []
    # Оставляем только те триграмы, частоты которых превышает порог.
    for trigram in trigrams:
        find = re.findall(trigram, all_texts, flags=re.DOTALL)
        amount = len(find)
        freq = amount / len(all_texts.split())
        freqs.append(freq)
        if freq > 0.001:  # Этот порог меняли и выбирали наилучший результат.
            final_trigrams.append(trigram)
    # Строили график, чтобы определить пороговое значение для частоты.        
    # plt.plot(sorted(freqs)) 
    # plt.show()
    return final_trigrams

# Считаем частоту рассматриваемых триграм для каждого текста.
def count_trigramms(file_path, trigrams):
    d = {}
    f = open(file_path, 'r', encoding='utf8')
    f = f.read()
    for trigramm in trigramms:
        trigramm = re.sub('([)(-*])', '\\' + '\1', trigramm)
        finds = re.findall(trigramm, f.read(), flags=re.DOTALL)
        c = len(finds)
        if trigramm not in d:
            d[trigramm] = с
        else:
            d[trigramm] += c
    # Считаем нормализованную частоту (делим на количество слов в тексте).
    for i in d:
        d[i] /= len(f.split())
    return d

# Находим триграмы и делаем из множества список.
all_trigrams = collect_trigrams(all_paths)
print(len(all_trigrams))
all_trigrams = list(all_trigrams)

files_471 = os.listdir(path='./471/')
files_66 = os.listdir(path='./66/')
files_26 = os.listdir(path='./26/')

# Отдельно собираем массивы данных для трех авторов.
data_471 = []
data_471_test = []
l = len(files_471)
for file in files_471:
    if file.endswith('.txt'):
        file_path = './471/' + file
        d = count_trigrams(file_path, all_trigrams)
        file_data = [471]
        for i in d:
            file_data.append(d[i])
        if l > 4:
            data_471.append(file_data)
        else:
            data_471_test.append(file_data)
    l -= 1

data_66 = []
data_66_test = []
l = len(files_66)
for file in files_66:
    if file.endswith('.txt'):
        file_path = './66/' + file
        d = count_trigrams(file_path, all_trigrams)
        file_data = [66]
        for i in d:
            file_data.append(d[i])
        if l > 4:
            data_66.append(file_data)
        else:
            data_66_test.append(file_data)
    l -= 1

data_26 = []
data_26_test = []
l = len(files_26)
for file in files_26:
    if file.endswith('.txt'):
        file_path = './26/' + file
        d = count_trigrams(file_path, all_trigrams)
        file_data = [26]
        for i in d:
            file_data.append(d[i])
        if l > 4:
            data_26.append(file_data)
        else:
            data_26_test.append(file_data)
    l -= 1

# Собираем все вместе и записываев в csv.
data = open('data.csv', 'w', encoding='utf-8')
all_data = np.vstack((data_471, data_66, data_26))
for k in all_data:
    for l in k:
        data.write(str(l) + ';')
    data.write('\r\n')
data.close()

data_test = open('data_test.csv', 'w', encoding='utf-8')
all_data_test = np.vstack((data_471_test, data_66_test, data_26_test))
for k in all_data_test:
    for l in k:
        data_test.write(str(l) + ';')
    data_test.write('\r\n')
data_test.close()
