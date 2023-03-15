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
    res = colored_text(name, Fore.MAGENTA, bold=True, underline=True) # Добавление названия упражнения
    res += '\n\n' + colored_text(condition, Fore.YELLOW, bold=True) + '\n' # Добавление условия
    for i in enumerate(ansers): # Добавление пронумированных ответов
        res += '\n' + str(i[0] + 1) + ': ' + i[1]
    print(res)

    ############################### Приём ответа ##################################
    u_ansers = set()
    while True:
        print()
        print(colored_text(f'Введите {"вариант" if len(right_indexs) == 1 else "варианты"} ответа: ', Fore.CYAN, bold=True), end='')
        u_ansers = set(map(int, list(input()))) # Приём ответа и запись в set(int) (set был выбран для того, чтобы пользователь мог вводить ответ в разном порядке)
        user_ansers.append(sorted(list(u_ansers))) # Сохранение ответа прользователя
        if u_ansers == right_indexs: # Проверка на правильность
            print(colored_text('Ваш ответ правильный', Fore.GREEN, bold=True))
            return user_ansers, scores # Возврат Истории ответов пользователя и его баллов

        scores -= 0.5 # Вычет баллов в случае не правильности результатов
        
        if scores == 0: # Проверка на количество баллов (завершение если 0)
            print(colored_text('Правильный ответ: ', Fore.YELLOW, bold=True) + str(', '.join(sorted(list(map(str, right_indexs))))))
            return user_ansers, scores # Возврат Истории ответов пользователя и его баллов

        print(colored_text("Ваш ответ не правильгый попробуйте снова.", Fore.RED, bold=True))


def save_res(res: dict, max_scores: float):
    ########## Составление словаря в формате {имя_упражнения: {Баллы: float, Ответы: list(list(int))}, Оценка: str} ##########
    returner = {}
    sum_of_scores = 0
    for i in res.keys(): # Прохождение циклом по названиям теста
        returner[i] = { "Баллы": res[i]['scores'], "Ответы": res[i]['user_ansers']} # Вынимаем нужную информацию
        sum_of_scores += res[i]['scores'] # Прибавляем полученные баллы за упражнение

    ############################### Определение оценки ##################################
    if sum_of_scores / max_scores < 0.4:
        returner['Оценка'] = "Не удовлетварительно"
    elif sum_of_scores / max_scores < 0.6:
        returner['Оценка'] = "Удовлетварительно"
    elif sum_of_scores / max_scores < 0.8:
        returner['Оценка'] = "Хорошо"
    else:
        returner['Оценка'] = "Отлично"

    ############################### Загрузка файла ##################################
    with open('./log.json', 'w') as file:
        json.dump(returner, file, ensure_ascii=False, indent=4)


def get_exercise(file_path):
    ############################### Получение условия задачи из файла "file_path" ##################################
    with open(file_path) as file:
        exs = json.loads(file.read()) 
        return [{'name': ex['name'], 'condition': ex['text'], 'ansers': ex['ansers'], 'right_indexs': set(ex['right']), 'scores': ex['scores']} for ex in exs]


def test(file_path):
    ############################### Функция проведения теста ##################################
    exercises = get_exercise(file_path) # Получаем список условий упражнений
    max_scores = sum(i['scores'] for i in exercises) # Считаем максимальный балл (суммарный)
    scores = dict()
    
    ############################### Провеедени каждого упражнения поочерёдно ##################################
    for exercise in exercises:
        exercise['user_ansers'], exercise['scores'] = conduct_exercise(**exercise) # Проведение упражнения
          
        print('\n')
        scores[exercise['name']] = {'scores': exercise['scores'], 'user_ansers': exercise['user_ansers']}

    ############################### Выввод результатов ##################################
    print('-' * 60)
    res = sum(scores[i]['scores'] for i in scores.keys())
    
    print(colored_text('Результат' + ' ' + str(round(100 * res / max_scores)) + '%', Fore.MAGENTA, bold=True))
    
    save_res(scores, max_scores)



print(open('./hi.txt', 'r').read()) # Вывод приветственного сообщения
test("./test.json") # Запуск теста

