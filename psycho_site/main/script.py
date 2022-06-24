from main.psycho_tests import about_tests

for test in about_tests.values():
    print('---TEST---')
    for q in test['questions']:
        stroka = " ".join(q.split(" ")[1:])
        print(f'"{stroka}",')
