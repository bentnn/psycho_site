# Подсчет параметров результата в 3 тесте
def count_res_test3(from_q, to_q, pos_q, data):
    # a = 35 + sum(int(data.get(str(i))) if i in pos_q else -int(data.get(str(i))) for i in range(1, 2))
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
    # being_q = sum(int(data.get(str(i))) if i in inverse_q else 8 - int(data.get(str(i))) for i in questions) / len(questions)
    out_res = 0
    for i in questions:
        res = int(data.get(str(i)))
        if i in inverse_q:
            out_res += 8 - res
        else:
            out_res += res
    return out_res / len(questions)
