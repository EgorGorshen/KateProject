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
    def __init__(self, name: str, condition: str, anser: list[str], right_indexs: set[str], scores: int) -> None:
        self.name: str = name
        self.condition: str = condition
        self.ansers: list[str] = anser
        self.right: set[str] = right_indexs
        self.max_scores: float = scores
        self.scores: float = scores

    def print_exercise(self):
        res = colored_text(self.name, Fore.MAGENTA, bold=True, underline=True)
        res += '\n\n' + colored_text(self.condition, Fore.YELLOW, bold=True) + '\n'
        for i in enumerate(self.ansers):
            res += '\n' + str(i[0] + 1) + ': ' + i[1]
        print(res)

    def get_anser(self):
        ansers = set()
        while self.scores:
            print()
            print(colored_text(f'Введите {"вариант" if len(self.right) == 1 else "варианты"} ответа: ', Fore.CYAN, bold=True), end='')
            ansers = set(map(int, input()))
            if ansers == self.right:
                print(colored_text('Ваш ответ правильный', Fore.GREEN, bold=True))
                return

            print(colored_text("Ваш ответ не правильгый попробуйте снова.", Fore.RED, bold=True))
            self.scores -= 0.5
        print(colored_text('Правильный ответ: ', Fore.YELLOW, bold=True) + str(', '.join(sorted(list(map(str, self.right))))))


class Test:
    def __init__(self, file_path) -> None:
        self.file_path: str = file_path
        self.exercises: list[Exercise] = self._get_exercise()
        self.max_scores = sum(i.scores for i in self.exercises)
        self.scores: dict[Exercise, float] = dict()

    def _get_exercise(self) -> list[Exercise]:
        with open(self.file_path) as file:
            exs = json.loads(file.read())
        res = []
        for ex in exs:
            res.append(
                Exercise(
                    ex['name'], 
                    ex['text'], 
                    ex['ansers'],
                    set(ex['right']),
                    ex['scores']
                )
            )
        return res


    def start_test(self):
        for exercise in self.exercises:
            exercise.print_exercise()
            exercise.get_anser()
            print()
            print()
            self.scores[exercise] = exercise.scores

    def print_res(self):
        print('-' * 60)
        # length = max(len(i.name) for i in self.exercises)
        res = sum(i.scores for i in self.scores)
        for i in self.exercises:
            print(
                "{:<30}".format(colored_text(i.name + ' ' + str(i.scores), Fore.MAGENTA, bold=True)), 
                colored_text('#' * int(50 * i.scores / i.max_scores) + '-' * int(50 - 50 * i.scores / i.max_scores), Fore.YELLOW))
        print()
        print("{:<30}".format(colored_text('Результат' + ' ' + str(round(100 * res / self.max_scores)) + '%', Fore.MAGENTA, bold=True)),
              colored_text('#' * int(50 * res / self.max_scores) + '-' * int(50 - 50 * res / self.max_scores), Fore.YELLOW))


test = Test("./test.json")
test.start_test()
test.print_res()
