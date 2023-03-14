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


class Exercise:
    """ Класс упражнения """
    def __init__(self, name: str, condition: str, anser: list[str], right_indexs: set[int], scores: int):
        # Инициализатор класса. Принимает название упражнения, его условие, варианты ответов, 
        # правильный(е) вариант(ы) ответа, максимально возможные баллы за упражнение.
        self.name: str = name
        self.condition: str = condition
        self.ansers: list[str] = anser
        self.right: set[int] = right_indexs
        self.max_scores: float = scores
        self.scores: float = scores
        self.user_ansers: list[list[int]] = []


    def print_exercise(self):
        # Метод для вывода условия и вариантов ответов на экран.
        res = colored_text(self.name, Fore.MAGENTA, bold=True, underline=True)
        res += '\n\n' + colored_text(self.condition, Fore.YELLOW, bold=True) + '\n'
        for i in enumerate(self.ansers):
            res += '\n' + str(i[0] + 1) + ': ' + i[1]
        print(res)

    def get_anser(self):
        # Метод для получения ответа от пользователя.
        # Запрашивает ввод пользователем варианта ответа и проверяет его на правильность.
        # Если ответ неверный, уменьшает количество баллов и запрашивает ввод ответа снова.
        ansers = set()
        while True:
            print()
            print(colored_text(f'Введите {"вариант" if len(self.right) == 1 else "варианты"} ответа: ', Fore.CYAN, bold=True), end='')
            ansers = set(map(int, input()))
            self.user_ansers.append(sorted(list(ansers)))
            if ansers == self.right:
                print(colored_text('Ваш ответ правильный', Fore.GREEN, bold=True))
                return
            else:
                self.scores -= 0.5
            
            if self.scores == 0:
                print(colored_text('Правильный ответ: ', Fore.YELLOW, bold=True) + str(', '.join(sorted(list(map(str, self.right))))))
                return
            else:
                print(colored_text("Ваш ответ не правильгый попробуйте снова.", Fore.RED, bold=True))


def save_res(res: list[Exercise]):
    """ Загрузска файла с логами """
    returner = {}
    sum_of_scores = 0
    max_sum_of_scores = 0
    for i in res:
        returner[i.name] = { "Баллы": i.scores, "Ответы": i.user_ansers}
        sum_of_scores, max_sum_of_scores = sum_of_scores + i.scores, max_sum_of_scores + i.max_scores
    if sum_of_scores / max_sum_of_scores < 0.4:
        returner['Оценка'] = "Не удовлетварительно"
    elif sum_of_scores / max_sum_of_scores < 0.6:
        returner['Оценка'] = "Удовлетварительно"
    elif sum_of_scores / max_sum_of_scores < 0.8:
        returner['Оценка'] = "Хорошо"
    else:
        returner['Оценка'] = "Отлично"

    with open('./log.json', 'w') as file:
        json.dump(returner, file, ensure_ascii=False, indent=4)


class Test:
    def __init__(self, file_path):
        self.file_path: str = file_path
        self.exercises: list[Exercise] = self._get_exercise()  # Получение списка заданий из файла
        self.max_scores = sum(i.scores for i in self.exercises)  # Вычисление максимального количества баллов за тест
        self.scores: dict[Exercise, float] = dict()  # Словарь для хранения результатов за каждое задание

    def _get_exercise(self):
        with open(self.file_path) as file:
            exs = json.loads(file.read())  # Чтение данных из файла
        # Создание объектов Exercise для каждого задания
        return [Exercise(ex['name'], ex['text'], ex['ansers'], set(ex['right']), ex['scores']) for ex in exs]

    def start_test(self):
        for exercise in self.exercises:  # Проход по каждому заданию и его решение
            exercise.print_exercise()  # Вывод текста задания
            exercise.get_anser()  # Получение ответа пользователя
            print('\n')
            self.scores[exercise] = exercise.scores  # Сохранение результатов за задание
        return self

    def print_res(self):
        print('-' * 60)
        res = sum(i.scores for i in self.scores)  # Вычисление общего количества набранных баллов
        for i in self.exercises:  # Вывод результатов за каждое задание
            print("{:<30}".format(colored_text(i.name + ' ' + str(i.scores), Fore.MAGENTA, bold=True)), colored_text('#' * int(50 * i.scores / i.max_scores) + '-' * int(50 - 50 * i.scores / i.max_scores), Fore.YELLOW))  # Вывод графического представления результата
        print("\n{:<30}".format(colored_text('Результат' + ' ' + str(round(100 * res / self.max_scores)) + '%', Fore.MAGENTA, bold=True)), colored_text('#' * int(50 * res / self.max_scores) + '-' * int(50 - 50 * res / self.max_scores), Fore.YELLOW))  # Вывод итогового результата
        save_res(self.exercises)


print(open('./hi.txt', 'r').read())
Test("./test.json").start_test().print_res()
