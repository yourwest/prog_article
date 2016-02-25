__author__ = 'angelinaprisyazhnaya'

import csv

#Читаем csv и отдельно записываем данные для каждого автора.
f = open('data.csv', 'r', encoding='utf-8')
f = f.read()
data_471 = []
data_66 = []
data_26 = []
csv_iter = csv.reader(f.split('\n'), delimiter=';')
for row in csv_iter:
    if not row == []:
        if row[0] == '471.0':
            data_471.append(row[:-1])
        elif row[0] == '66.0':
            data_66.append(row[:-1])
        elif row[0] == '26.0':
            data_26.append(row[:-1])


#Читаем csv с данными тестовых текстов.
f_test = open('data_test.csv', 'r', encoding='utf-8')
f_test = f_test.read()
data_test = []
csv_iter = csv.reader(f_test.split('\n'), delimiter=';')
for row in csv_iter:
    if not row == []:
        data_test.append(row[:-1])


#Считаем D.
def count_dissimilarity(profile_1, profile_2):
    length = len(profile_1)
    dissimilarity = 0
    i = 1
    while i < length:
        try:
            d = ((float(profile_1[i]) - float(profile_2[i])) / ((float(profile_1[i]) + float(profile_2[i])) / 2)) ** 2
        except ZeroDivisionError:
            d = 0.0
        dissimilarity += d
        i += 1
    return dissimilarity


#Считаем Dmax.
def find_max_dissimilarity(d_i, data):
    dissimilarities = []
    for profile in data:
        dissimilarity = count_dissimilarity(d_i, profile)
        if dissimilarity != 0:
            dissimilarities.append(dissimilarity)
    max_dissimilarity = max(dissimilarities)
    return max_dissimilarity


def authorship_verification(test_text, known_texts):
    threshold = 0.95
    ratios = []
    for text in known_texts:
        ratio = count_dissimilarity(test_text, text) / find_max_dissimilarity(text, known_texts)
    ratios.append(ratio)
    summ = 0
    for i in ratios:
        summ += i
    mean_ratio = summ / len(ratios)
    print(mean_ratio)
    if mean_ratio < threshold:
        answer = 'Authorship is verified.'
    else:
        answer = 'Authorship is not verified.'
    return answer


for i in data_test:
    print(authorship_verification(i, data_471))
    print(authorship_verification(i, data_66))
    print(authorship_verification(i, data_26))
    print('')