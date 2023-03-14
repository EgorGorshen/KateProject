from colorama import Fore, Style
import json


def colored_text(text, color, bold=False, underline=False):
    """ Функция для раскраски текста """
    style = []
    if bold:
        style.append(Style.BRIGHT)
    if underline:
        style.append('\033[4m')
    return f"{color}{''.join(style)}{text}{Style.RESET_ALL}"


def conduct_exercise(name: str, condition: str, ansers: list[str], right_indexs: set[int], scores: float):
    
    user_ansers: list[list[int]] = []

    ######################### Вывод условия упражнения ###########################
    res = colored_text(name, Fore.MAGENTA, bold=True, underline=True)
    res += '\n\n' + colored_text(condition, Fore.YELLOW, bold=True) + '\n'
    for i in enumerate(ansers):
        res += '\n' + str(i[0] + 1) + ': ' + i[1]
    print(res)

    ############################### Приём ответа ##################################
    u_ansers = set()
    while True:
        print()
        print(colored_text(f'Введите {"вариант" if len(right_indexs) == 1 else "варианты"} ответа: ', Fore.CYAN, bold=True), end='')
        u_ansers = set(map(int, list(input())))
        user_ansers.append(sorted(list(u_ansers)))
        if u_ansers == right_indexs:
            print(colored_text('Ваш ответ правильный', Fore.GREEN, bold=True))
            return user_ansers, scores
        scores -= 0.5
        
        if scores == 0:
            print(colored_text('Правильный ответ: ', Fore.YELLOW, bold=True) + str(', '.join(sorted(list(map(str, right_indexs))))))
            return user_ansers, scores
        print(colored_text("Ваш ответ не правильгый попробуйте снова.", Fore.RED, bold=True))


def save_res(res: dict, max_scores: float):
    """ Загрузска файла с логами """
    returner = {}
    sum_of_scores = 0
    for i in res.keys():
        returner[i] = { "Баллы": res[i]['scores'], "Ответы": res[i]['user_ansers']}
        sum_of_scores += res[i]['scores']
    if sum_of_scores / max_scores < 0.4:
        returner['Оценка'] = "Не удовлетварительно"
    elif sum_of_scores / max_scores < 0.6:
        returner['Оценка'] = "Удовлетварительно"
    elif sum_of_scores / max_scores < 0.8:
        returner['Оценка'] = "Хорошо"
    else:
        returner['Оценка'] = "Отлично"

    with open('./log.json', 'w') as file:
        json.dump(returner, file, ensure_ascii=False, indent=4)


def get_exercise(file_path):
    with open(file_path) as file:
        exs = json.loads(file.read()) 
        return [{'name': ex['name'], 'condition': ex['text'], 'ansers': ex['ansers'], 'right_indexs': set(ex['right']), 'scores': ex['scores']} for ex in exs]


def test(file_path):
    exercises = get_exercise(file_path) 
    max_scores = sum(i['scores'] for i in exercises)
    scores = dict()

    for exercise in exercises:  # Проход по каждому заданию и его решение
        exercise['user_ansers'], exercise['scores'] = conduct_exercise(**exercise)  # Вывод текста задания
          # Получение ответа пользователя
        print('\n')
        scores[exercise['name']] = {'scores': exercise['scores'], 'user_ansers': exercise['user_ansers']}

    print('-' * 60)
    res = sum(scores[i]['scores'] for i in scores.keys())  # Вычисление общего количества набранных баллов
    
    print(colored_text('Результат' + ' ' + str(round(100 * res / max_scores)) + '%', Fore.MAGENTA, bold=True))
    
    save_res(scores, max_scores)


print(open('./hi.txt', 'r').read())
test("./test.json")
