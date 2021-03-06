import matplotlib.pyplot as plt
from io import StringIO
import numpy as np
from .models import *


def graph_settings(ax, x, y, s):
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    axis = plt.gca()
    plt.xticks(x)
    plt.yticks(np.arange(0, max(y) + 1, s))
    plt.style.use('bmh')


def graph_settings2(ax, values, s):
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    axis = plt.gca()

    plt.xticks([i for i, value in enumerate(next(i for i in values))])
    maximum_y = max(max(i) for i in values) + 10
    plt.yticks(np.arange(0, maximum_y, s))
    plt.style.use('bmh')


def lines_graph(test_results):
    base_values = [*BaseTestModel.__dict__.keys(), '_state', 'id']
    graph_values = {name: [] for name in test_results[0].__dict__ if name not in base_values}
    for i in test_results:
        for name in graph_values:
            graph_values[name].append(i.__getattribute__(name))
    fig, ax = plt.subplots(1, figsize=(8, 6))
    # graph_settings(ax, [i for i, t in enumerate(test_results)], [20], 5.0)
    for name, value in graph_values.items():
        ax.plot(value, alpha=0.5, linewidth=3, marker='o', label=name)
    ax.grid()
    plt.style.use('bmh')
    ax.legend(loc='upper left')
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg', transparent=True)
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


def return_graph4_1(array):
    # График для четвертого тест, сделал три линии на одном графике
    x = []
    y1 = []
    y2 = []
    y3 = []
    for n, i in enumerate(array):
        x.append(n)
        y1.append(i.activity)
        y2.append(i.being)
        y3.append(i.mood)

    fig, ax = plt.subplots(1, figsize=(8, 6))
    ax.plot(y1, color="gold", alpha=0.5, linewidth=3, marker='o')
    ax.plot(y2, color="dodgerblue", alpha=0.5, linewidth=3, marker='o')
    ax.plot(y3, color="red", alpha=0.5, linewidth=3, marker='o')
    graph_settings(ax, x, y1, 0.5)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg', transparent=True)
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data

def return_graph1_1(array):  # Первый график первого теста, три линии на одном
    x = []
    y1 = []
    y2 = []
    y3 = []
    for n, i in enumerate(array):
        x.append(n)
        y1.append(i.audio)
        y2.append(i.visual)
        y3.append(i.kinest)

    fig, ax = plt.subplots(1, figsize=(8, 6))
    graph_settings(ax, x, y1, 1.0)
    ax.plot(y1, color="aqua", alpha=0.5, linewidth=3, marker='o')
    ax.plot(y2, color="blueviolet", alpha=0.5, linewidth=3, marker='o')
    ax.plot(y3, color="coral", alpha=0.5, linewidth=3, marker='o')
    ax.grid()
    # alpha отвечает за прозрачность(уменьшять в десятичных), linewidth за толщину, увеличивать единицами
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg', transparent=True)
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


def pie_graph(test_results):
    base_values = [*BaseTestModel.__dict__.keys(), '_state', 'id']
    graph_values = {name: 0 for name in test_results[0].__dict__ if name not in base_values}
    for res in test_results:
        for name in graph_values:
            graph_values[name] += getattr(res, name)
    res_len = len(test_results)
    for name in graph_values:
        graph_values[name] /= res_len

    fig, ax = plt.subplots()
    ax.pie(graph_values.values(), autopct="%.2f%%", explode=[0.1 for _ in graph_values], labels=graph_values.keys())
    ax.legend(loc='upper left')
    plt.style.use('bmh')
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

    fig, ax = plt.subplots()
    ax.pie(y, autopct="%.2f%%", explode=(0.1, 0.1, 0.1), colors=('aqua', 'blueviolet', 'coral'))

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg', transparent=True)
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


def fill_line_graph(test_results, param_name, axhlines: list = None):
    base_values = [*BaseTestModel.__dict__.keys(), '_state', 'id']
    graph_values = {name: [] for name in test_results[0].__dict__ if name not in base_values}
    results = [getattr(test, param_name, 0) for test in test_results]
    fig, ax = plt.subplots()
    ax.fill_between([i for i in range(len(results))], results)
    ax.plot([i for i in range(len(results))], results, alpha=0.5, linewidth=3, marker='o')
    for line in (axhlines or []):
        plt.axhline(y=line, dashes=(6, 4), linewidth=0.8, color="black")
    plt.style.use('bmh')

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg', transparent=True)
    imgdata.seek(0)
    data = imgdata.getvalue()
    return data


def return_graph2_1(array):  # Первый график для второго теста(реактивное), с разделяющими линиями
    x = []
    y = []
    for n, i in enumerate(array):
        x.append(n)
        y.append(i.rt)

    fig, ax = plt.subplots()
    ax.fill_between(x, y, color="royalblue")
    plt.axhline(y=30, dashes=(6, 4), linewidth=0.8, color="black")
    plt.axhline(y=45, dashes=(6, 4), linewidth=0.8, color="black")
    graph_settings(ax, x, y, 5.0)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg', transparent=True)
    imgdata.seek(0)
    data = imgdata.getvalue()
    return data


def return_graph2_2(array):  # Второй график для второго теста(личностное), с разделяющими линиями
    x = []
    y = []
    for n, i in enumerate(array):
        x.append(n)
        y.append(i.lt)

    fig, ax = plt.subplots()
    ax.fill_between(x, y, color="orange")
    plt.axhline(y=30, dashes=(6, 4), linewidth=0.8, color="black")
    plt.axhline(y=45, dashes=(6, 4), linewidth=0.8, color="black")
    graph_settings(ax, x, y, 5.0)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg', transparent=True)
    imgdata.seek(0)
    data = imgdata.getvalue()
    return data


def return_graph3(array):  # График для Третьего теста
    x = []
    y = []
    for n, i in enumerate(array):
        x.append(n)
        y.append(i.ud)

    fig, ax = plt.subplots()
    ax.fill_between(x, y, color="green")
    ax.plot(x, y, color="green", alpha=0.5, linewidth=3, marker='o')  # Сделал график, чтобы точка в 0 отображалась
    plt.axhline(y=50, dashes=(6, 4), linewidth=0.8, color="black")
    plt.axhline(y=60, dashes=(6, 4), linewidth=0.8, color="black")
    plt.axhline(y=70, dashes=(6, 4), linewidth=0.8, color="black")
    graph_settings(ax, x, [90], 5.0)  # Выставил максимум

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg', transparent=True)
    imgdata.seek(0)
    data = imgdata.getvalue()
    return data


def return_graph4_2(array):
    y = [0, 0, 0]

    for i in array:
        y[0] += i.activity
        y[1] += i.being
        y[2] += i.mood
    array_len = len(array)
    for i in y:
        i /= array_len

    fig, ax = plt.subplots()
    ax.pie(y, autopct="%.2f%%", explode=(0.1, 0.1, 0.1), colors=('gold', 'dodgerblue', 'red'))

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg', transparent=True)
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


def return_graph_5_1(array):
    x = []
    y = []
    for n, i in enumerate(array):
        x.append(n)
        y.append(i.sincerity)

    fig, ax = plt.subplots()
    ax.plot(x, y, color="mediumvioletred", marker='o')
    ax.grid(axis='y', alpha=0.8)  # Добавил сетку
    graph_settings(ax, x, [10], 1.0)  # Выставил максимум

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg', transparent=True)
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


def return_graph_5_2(array):
    x = []
    y = []
    for n, i in enumerate(array):
        x.append(n)
        y.append(i.extrav)

    fig, ax = plt.subplots()
    ax.plot(x, y, color="deepskyblue", marker='o')
    ax.grid(axis='y', alpha=0.8)  # Добавил сетку
    graph_settings(ax, x, [25], 2.0)  # Выставил максимум

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg', transparent=True)
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


def return_graph_5_3(array):
    x = []
    y = []
    for n, i in enumerate(array):
        x.append(n)
        y.append(i.neuro)

    fig, ax = plt.subplots()
    ax.plot(x, y, color="darkorange", marker='o')
    ax.grid(axis='y', alpha=0.8)  # Добавил сетку
    graph_settings(ax, x, [25], 2.0)  # Выставил максимум

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg', transparent=True)
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data
