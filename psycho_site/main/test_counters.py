# Подсчет параметров результата в 3 тесте
def count_res_test3(from_q, to_q, pos_q, data):
    out_res = 35
    for i in range(from_q, to_q):
        res = int(data.get(str(i)))
        if i in pos_q:
            out_res += res
        else:
            out_res -= res
    return out_res


# Подсчет параметров результата в 4 тесте
def count_res_test4(questions, inverse_q, data):
    out_res = 0
    for i in questions:
        res = int(data.get(str(i)))
        if i in inverse_q:
            out_res += 8 - res
        else:
            out_res += res
    return out_res / len(questions)


def count_message_test6(effect: int, low: int, middle: int,
                        name_of_effect: str):
    if effect <= low:
        message = 'Низкий'
    elif effect <= middle:
        message = 'Средний'
    else:
        message = 'Высокий'
    return message + f' уровень {name_of_effect} аффекта.\n'
