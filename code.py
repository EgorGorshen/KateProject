from colorama import Fore, Style
import json


def colored_text(text, color, bold=False, underline=False):
    """
    Функция для раскраски текста
    """
    style = []
    if bold:
        style.append(Style.BRIGHT)
    if underline:
        style.append('\033[4m')
    return f"{color}{''.join(style)}{text}{Style.RESET_ALL}"


class Exercise:
    """
    Класс упражнения
    """
    def __init__(self, name: str, condition: str, anser: list[str], right_indexs: set[int], scores: int) -> None:
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
            
            self.scores -= 0.5
            
            if self.scores == 0:
                print(colored_text('Правильный ответ: ', Fore.YELLOW, bold=True) + str(', '.join(sorted(list(map(str, self.right))))))
                return
            
            print(colored_text("Ваш ответ не правильгый попробуйте снова.", Fore.RED, bold=True))


def save_res(res: list[Exercise]):
    """
    Загрузска файла с логами
    """
    returner = {}
    sum_of_scores = 0
    max_sum_of_scores = 0
    for i in res:
        returner[i.name] = {
            "Баллы": i.scores,
            "Ответы": i.user_ansers
        }
        sum_of_scores += i.scores
        max_sum_of_scores += i.max_scores
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
    def __init__(self, file_path) -> None:
        self.file_path: str = file_path
        self.exercises: list[Exercise] = self._get_exercise()  # Получение списка заданий из файла
        self.max_scores = sum(i.scores for i in self.exercises)  # Вычисление максимального количества баллов за тест
        self.scores: dict[Exercise, float] = dict()  # Словарь для хранения результатов за каждое задание

    def _get_exercise(self) -> list[Exercise]:
        with open(self.file_path) as file:
            exs = json.loads(file.read())  # Чтение данных из файла
        res = []
        for ex in exs:  # Создание объектов Exercise для каждого задания
            res.append(
                Exercise(
                    ex['name'],  # Название задания
                    ex['text'],  # Текст задания
                    ex['ansers'],  # Варианты ответов
                    set(ex['right']),  # Множество правильных ответов
                    ex['scores']  # Количество баллов за задание
                )
            )
        return res

    def start_test(self):
        for exercise in self.exercises:  # Проход по каждому заданию и его решение
            exercise.print_exercise()  # Вывод текста задания
            exercise.get_anser()  # Получение ответа пользователя
            print()
            print()
            self.scores[exercise] = exercise.scores  # Сохранение результатов за задание

    def print_res(self):
        print('-' * 60)
        res = sum(i.scores for i in self.scores)  # Вычисление общего количества набранных баллов
        for i in self.exercises:  # Вывод результатов за каждое задание
            print(
                "{:<30}".format(colored_text(i.name + ' ' + str(i.scores), Fore.MAGENTA, bold=True)), 
                colored_text('#' * int(50 * i.scores / i.max_scores) + '-' * int(50 - 50 * i.scores / i.max_scores), Fore.YELLOW))  # Вывод графического представления результата
        print()
        print("{:<30}".format(colored_text('Результат' + ' ' + str(round(100 * res / self.max_scores)) + '%', Fore.MAGENTA, bold=True)),
              colored_text('#' * int(50 * res / self.max_scores) + '-' * int(50 - 50 * res / self.max_scores), Fore.YELLOW))  # Вывод итогового результата
        
        save_res(self.exercises)


test = Test("./test.json")
test.start_test()
test.print_res()
