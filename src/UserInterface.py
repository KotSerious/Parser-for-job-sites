from src.VacancyStorage import JsonVacancyStorage, TxtVacancyStorage, CSVVacancyStorage, ExcelVacancyStorage
from src.api.HhAPI import HhAPI
from src.api.SuperJobAPI import SuperJobAPI


class UserInterface:
    """
        Класс, представляющий интерфейс пользователя для взаимодействия с программой.

        Methods:
            get_search_term() -> str:
                Получает запрос пользователя для поиска вакансий.

            get_city_name() -> str:
                Получает название города от пользователя.

            get_experience() -> str:
                Получает уровень опыта работы от пользователя.

            get_count_vacancies() -> int or None:
                Получает минимальное количество вакансий для вывода от пользователя.

            get_order_param() -> str:
                Получает параметр сортировки от пользователя.

            get_site_selection() -> ApiHandler:
                Получает выбор пользователя для использования API (HhAPI или SuperJobAPI).

            print_main_menu() -> str:
                Выводит главное меню и получает выбор пользователя.

            save_to_file_context(filename: str, vacancies_list: list[dict]):
                Получает выбор пользователя для сохранения вакансий в файл.

    """
    @staticmethod
    def get_search_term() -> str:
        """
                Получает запрос пользователя для поиска вакансий.

                :return: Запрос пользователя.
                :rtype: str
        """
        return input("Введите ваш запрос (напр. Python developer): ")

    @staticmethod
    def get_city_name() -> str:
        """
                Получает название города от пользователя.

                :return: Название города.
                :rtype: str
        """
        city = input("\nУкажите город, или оставьте пустым для глобального поиска: ")

        if '-' in city:
            parts = city.split('-')
            parts = [word.lower().title().strip() for word in parts]
            city = "-".join(parts)
        else:
            city = city.lower().title()

        return city

    @staticmethod
    def get_experience():
        """
                Получает уровень опыта работы от пользователя.

                :return: Уровень опыта работы (строка для запроса API).
                :rtype: str
        """
        experience = input("Укажите опыт работы: \n"
                           "1.Без опыта\n"
                           "2.От 1-3\n"
                           "3.От 3-6\n"
                           "4.Более 6\n"
                           "5.Не указывать\n"
                           "Ввод: ")

        match experience:
            case '1':
                return "noExperience"
            case '2':
                return "between1And3"
            case '3':
                return "between3And6"
            case '4':
                return "moreThan6"
            case '5':
                return None
            case _:
                print("Ошибка ввода")
                return None

    @staticmethod
    def get_count_vacancies():
        """
                Получает минимальное количество вакансий для вывода от пользователя.

                :return: Минимальное количество вакансий или None, если пользователь не указал.
                :rtype: int or None
        """
        try:
            count = int(input(
                "\nКакое минимальное количество вакансий вы хотите вывести на экран?\n"
                "(Нажмите Enter если хотите вывести все): "))
        except ValueError:
            count = None

        return count

    @staticmethod
    def get_order_param():
        """
                Получает параметр сортировки от пользователя.

                :return: Параметр сортировки или пустую строку, если пользователь не указал.
                :rtype: str
        """
        param = input("Отсортировать вакансии по:\n"
                      " 1.По времени публикации\n"
                      " 2.По зарплате\n"
                      " Если сортировка не требуется - нажмите Enter\n")
        return param

    @staticmethod
    def get_site_selection():
        """
                Получает выбор пользователя для использования API (HhAPI или SuperJobAPI).

                :return: Объект APIHandler (HhAPI или SuperJobAPI).
                :rtype: ApiHandler
        """
        while True:
            choice = input("С какого сайта вывести вакансии:\n"
                           " 1.hh.ru\n"
                           " 2.SuperJob\n"
                           "Ввод: ")

            if choice == "1":
                return HhAPI()
            elif choice == "2":
                return SuperJobAPI()
            else:
                print("Ошибка ввода")

    @staticmethod
    def print_main_menu():
        """
                Выводит главное меню и получает выбор пользователя.

                :return: Выбор пользователя (строка).
                :rtype: str
        """
        flag = True

        while flag:
            choice = input("1.Поиск вакансий\n"
                           "2.Вывод вакансий из сохранённого json\n"
                           "3.Сравнение двух вакансий\n"
                           "4.Удалить вакансию из JSON\n"
                           "5.Вывести по ключевому слову\n"
                           "0.Выход\n"
                           "Ввод: ")

            if choice in ["0", "1", "2", "3", "4", "5"]:
                return choice
            else:
                print("Ошибка ввода")

    @staticmethod
    def save_to_file_context(filename: str, vacancies_list: list[dict]):
        """
                Получает выбор пользователя для сохранения вакансий в файл.

                :param filename: Имя файла для сохранения.
                :type filename: str

                :param vacancies_list: Список вакансий для сохранения.
                :type vacancies_list: list[dict]
        """
        flag = True

        while flag:
            choice = input("Хотите сохранить эти вакансии?:\n"
                           "1.В JSON\n"
                           "2.В TXT\n"
                           "3.В CSV\n"
                           "4.В EXEL\n"
                           "5.Не сохранять\n"
                           "Ввод: ")
            match choice:
                case "1":
                    json_saver = JsonVacancyStorage(filename + ".json", vacancies_list)
                    json_saver.save_to_file()
                    break
                case "2":
                    txt_saver = TxtVacancyStorage(filename + ".txt", vacancies_list)
                    txt_saver.save_to_file()
                    break
                case "3":
                    txt_saver = CSVVacancyStorage(filename + ".csv", vacancies_list)
                    txt_saver.save_to_file()
                    break
                case "4":
                    txt_saver = ExcelVacancyStorage(filename + ".xls", vacancies_list)
                    txt_saver.save_to_file()
                    break
                case "5":
                    return
                case _:
                    print("Ошибка ввода!")
