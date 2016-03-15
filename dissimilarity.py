__author__ = 'angelinaprisyazhnaya'

import csv
import numpy as np
from sklearn import metrics
from sklearn.preprocessing import label_binarize
import matplotlib.pyplot as plt

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


#Считаем вероятность авторства.
def authorship_verification(test_text, known_texts):
    threshold = 0.9
    c = 0.1
    ratios = []
    for text in known_texts:
        ratio = count_dissimilarity(test_text, text) / find_max_dissimilarity(text, known_texts)
        ratios.append(ratio)
    mean_ratio = np.mean(ratios)
    if mean_ratio == threshold:
        probability = 0.5
    elif mean_ratio <= threshold - c:
        probability = 1
    elif mean_ratio >= threshold + c:
        probability = 0
    else:
        probability = (threshold + c - mean_ratio) / (2 * c)
    answer = 'Probability of authorship is ' + str(probability)
    return answer, probability

#Собираем массивы для ROC-кривых.
y_test = []
y_scores = []
for i in data_test:
    y_score = []
    y_test.append(float(i[0]))
    result_471 = authorship_verification(i, data_471)
    y_score.append(result_471[1])
    print(result_471[0])
    result_66 = authorship_verification(i, data_66)
    y_score.append(result_66[1])
    print(result_66[0])
    result_26 = authorship_verification(i, data_26)
    y_score.append(result_26[1])
    print(result_26[0])
    y_scores.append(y_score)

#Преобразовываем эти массивы.
y_test = label_binarize(y_test, classes=[471.0, 66.0, 26.0])
n_classes = y_test.shape[1]
y = np.array(y_test)
scores = np.array(y_scores)

#Считаем параметры для ROC-кривых.
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i], tpr[i], _ = metrics.roc_curve(y_test[:, i], scores[:, i])
    roc_auc[i] = metrics.auc(fpr[i], tpr[i])

#Строим ROC-кривые.
plt.figure()
for i in range(n_classes):
    plt.plot(fpr[i], tpr[i], label='ROC curve of class {0} (area = {1:0.3f})'
                                   ''.format(i, roc_auc[i]))
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc="lower right")
plt.show()
