import matplotlib.pyplot as plt
from io import StringIO
import numpy as np
from .models import *

import matplotlib.pyplot as plt
from io import StringIO
import numpy as np


def return_graph1_1(array):  # Первый график первого теста, три линии на одном
    # x = []
    # for a in range(array.audio):
    #     x.append(a)
    x = []

    y1 = []
    y2 = []
    y3 = []
    for n, i in enumerate(array):
        x.append(n)
        y1.append(i.audio)
        y2.append(i.visual)
        y3.append(i.kinest)
    # y1 = array.audio
    # y2 = array.visual
    # y3 = array.kinest

    fig, ax = plt.subplots(1, figsize=(8, 6))
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    axis = plt.gca()
    axis.axes.xaxis.set_ticklabels([])
    plt.xticks(x)
    plt.yticks(np.arange(0, max(y1)+1, 1.0))
    plt.style.use('seaborn-dark-palette')
    ax.plot(y1, color="red")
    ax.plot(y2, color="green")
    ax.plot(y3, color="blue")

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg', transparent=True)
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


def return_graph1_2(array):  # Второй график первого теста, средние значения каналов в виде пирога
    y = [0, 0, 0]

    for i in array:
        y[0] += i.audio
        y[1] += i.visual
        y[2] += i.kinest
    array_len = len(array)
    for i in y:
        i /= array_len
    # y1 = sum(Test1.audio) / len(Test1.audio)
    # y2 = sum(Test1.visual) / len(Test1.visual)
    # y3 = sum(Test1.kinest) / len(Test1.kinest)

    fig, ax = plt.subplots()
    ax.pie(y)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg', transparent=True)
    imgdata.seek(0)
    # Не уверен как будет сохранятся данный график, требуется живой проверки на сайте, не только в отдельном файле
    data = imgdata.getvalue()
    return data


# def return_graph2_1():  # Первый график для второго теста(реактивное), с разделяющими линиями
#     x = []
#     for a in range(Test2.rt):
#         x.append(a)
#
#     y = Test2.rt
#     fig, ax = plt.subplots()
#     ax.fill_between(x, y, color="brown")
#     axis = plt.gca()
#     plt.axhline(y=30, dashes=(6, 4), linewidth=0.8, color="black")
#     plt.axhline(y=35, dashes=(6, 4), linewidth=0.8, color="black")
#     plt.axhline(y=45, dashes=(6, 4), linewidth=0.8, color="black")
#     plt.style.use('seaborn-dark-palette')
#     axis.axes.xaxis.set_ticklabels([])
#     ax.set_ylim(ymin=0)
#     ax.set_xlim(xmin=0)
#     plt.xticks(x)
#     plt.yticks(np.arange(0, max(y) + 1, 5.0))
#
#     imgdata = StringIO()
#     fig.savefig(imgdata, format='svg', transparent=True)
#     imgdata.seek(0)
#     return data
#
#
# def return_graph2_2():  # Второй график для второго теста(личностное), с разделяющими линиями
#     x = []
#     for a in range(Test2.lt):
#         x.append(a)
#
#     y = Test2.lt
#     fig, ax = plt.subplots()
#     ax.fill_between(x, y, color="orange")
#     axis = plt.gca()
#     plt.axhline(y=30, dashes=(6, 4), linewidth=0.8, color="black")
#     plt.axhline(y=35, dashes=(6, 4), linewidth=0.8, color="black")
#     plt.axhline(y=45, dashes=(6, 4), linewidth=0.8, color="black")
#     plt.style.use('seaborn-dark-palette')
#     axis.axes.xaxis.set_ticklabels([])
#     ax.set_ylim(ymin=0)
#     ax.set_xlim(xmin=0)
#     plt.xticks(x)
#     plt.yticks(np.arange(0, max(y) + 1, 5.0))
#
#     imgdata = StringIO()
#     fig.savefig(imgdata, format='svg', transparent=True)
#     imgdata.seek(0)
#     return data
#
#
# def return_graph3():  # График для Третьего теста
#     x = []
#     for a in range(Test3.ud):
#         x.append(a)
#
#     y = Test3.ud
#     fig, ax = plt.subplots()
#     ax.fill_between(x, y, color="green")
#     axis = plt.gca()
#     plt.axhline(y=50, dashes=(6, 4), linewidth=0.8, color="black")
#     plt.axhline(y=60, dashes=(6, 4), linewidth=0.8, color="black")
#     plt.axhline(y=70, dashes=(6, 4), linewidth=0.8, color="black")
#     plt.style.use('seaborn-dark-palette')
#     axis.axes.xaxis.set_ticklabels([])
#     ax.set_ylim(ymin=0)
#     ax.set_xlim(xmin=0)
#     plt.xticks(x)
#     plt.yticks(np.arange(0, max(y) + 1, 5.0))
#
#     imgdata = StringIO()
#     fig.savefig(imgdata, format='svg', transparent=True)
#     imgdata.seek(0)
#
#     return data
#
#
# def return_graph4():
#     x = []
#     for a in range(Test4.activity):
#         x.append(a)
#
#     # График для четвертого тест, сделал три линии на одном графике, если скажешь сделаю раздельных три графика
#     y1 = Test4.activity
#     y2 = Test4.being
#     y3 = Test4.mood
#
#     fig, ax = plt.subplots(1, figsize=(8, 6))
#     axis = plt.gca()
#     axis.axes.xaxis.set_ticklabels([])
#     plt.xticks(x)
#     plt.yticks(np.arange(0, max(y1) + 1, 0.5))
#     plt.style.use('seaborn-dark-palette')
#
#     ax.plot(y1, color="gold")
#     ax.plot(y2, color="olivedrab")
#     ax.plot(y3, color="sandybrown")
#
#     imgdata = StringIO()
#     fig.savefig(imgdata, format='svg', transparent=True)
#     imgdata.seek(0)
#
#     data = imgdata.getvalue()
#     return data
