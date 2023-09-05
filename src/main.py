from src import utils
from src.UserInterface import UserInterface
from src.utils import search_vacancy, vacancies_comparison


def run_program():
    flag = True
    print("Привет! Я помогу найти тебе подходящую вакансию!\n")

    while flag:
        choice = UserInterface.print_main_menu()
        match choice:
            case '1':
                search_vacancy()  # Выполнить поиск вакансий.
            case '2':
                # Вывести сохраненные вакансии из JSON.
                for item in utils.get_list_of_vacancy_inst():
                    print(item)
                    print("-" * 100)
            case '3':
                result = vacancies_comparison()  # Сравнить вакансии по зарплате.
                print(result)
            case '4':
                utils.remove_vacancy_from_json()  # Удалить вакансию из JSON.
            case '5':
                utils.search_by_criterion()  # Поиск вакансий по ключевому слову.
            case "0":
                flag = False  # Завершить программу при выборе "0" (выход).


if __name__ == '__main__':
    run_program()
