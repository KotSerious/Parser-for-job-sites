from src.UserInterface import UserInterface
from src.VacancyStorage import JsonVacancyStorage
from src.api.HhAPI import HhAPI, ControllerHH
from src.api.SuperJobAPI import SuperJobAPI, ControllerSuperJob
from src.models.Vacancy import Vacancy


def search_vacancy():
    """
        Метод для поиска вакансий и сохранения их в файл.

        Использует ввод пользователя для получения параметров поиска,
        таких как: сайт, ключевой запрос, город, опыт, количество вакансий, сортировка.
        После чего, использует соответствующий API для получения данных и выводит их на экран.
        Затем сохраняет результаты в файл в формате JSON, TXT, CSV или Excel.

        :return: None
    """
    website = UserInterface.get_site_selection()

    search_term = UserInterface.get_search_term()

    city = UserInterface.get_city_name()
    if isinstance(website, HhAPI):
        city = ControllerHH.get_city_id(city)
    elif isinstance(website, SuperJobAPI):
        city = ControllerSuperJob.validate_city(city)

    experience = UserInterface.get_experience()

    number_of_vacancies = UserInterface.get_count_vacancies()

    order_by_param = UserInterface.get_order_param()
    if isinstance(website, HhAPI):
        order_by_param = ControllerHH.order_by(order_by_param)
    elif isinstance(website, SuperJobAPI):
        order_by_param = ControllerSuperJob.order_by(order_by_param)

    data = website.get_request(search_term, city, experience, number_of_vacancies, order_by_param)

    print([item.to_dict() for item in data])

    for item in data:
        print(item)
        print("-" * 30)

    UserInterface.save_to_file_context("../data/vacancies",
                                       [item.to_dict() for item in data])


def get_list_of_vacancy_inst():
    """
        Получить список вакансий из файла JSON и вернуть список экземпляров класса Vacancy.

        :return: Список экземпляров Vacancy.
    """
    json_loader = JsonVacancyStorage("../data/vacancies.json")
    json_loader.load_from_file()

    if len(json_loader.instance_vacancies) == 0:
        return []
    return json_loader.instance_vacancies


def vacancies_comparison() -> str:
    """
        Сравнение двух вакансий по их ID.

        Запрашивает у пользователя ID двух вакансий, сравнивает их
        и возвращает информацию о сравнении.

        :return: Строка с информацией о сравнении.
    """
    list_instance = get_list_of_vacancy_inst()

    list_vac_dict = [item.to_dict() for item in list_instance]
    first_id = int(input("\nВведите id первой вакансии: "))
    second_id = int(input("Введите id второй вакансии: "))

    vacancy1 = None  # Инициализация по умолчанию
    vacancy2 = None

    for item in list_vac_dict:
        if first_id == item.get("id_num"):
            vacancy1 = Vacancy(
                int(item.get('id_num', "Нет данных")),
                str(item.get('vacancy_name', "Нет данных")),
                str(item.get('company_name')),
                str(item.get('description', "Нет данных")),
                float(item.get('salary_from')),
                float(item.get('salary_to')),
                str(item.get('salary_currency')),
                str(item.get('area', "Нет данных")),
                str(item.get('url', "Нет данных")),
            )
        if second_id == item.get("id_num"):
            vacancy2 = Vacancy(
                int(item.get('id_num', "Нет данных")),
                str(item.get('vacancy_name', "Нет данных")),
                str(item.get('company_name')),
                str(item.get('description', "Нет данных")),
                float(item.get('salary_from')),
                float(item.get('salary_to')),
                str(item.get('salary_currency')),
                str(item.get('area', "Нет данных")),
                str(item.get('url', "Нет данных")),
            )

    if vacancy1 is None:
        return "Не удалось найти первую вакансию"
    elif vacancy2 is None:
        return "Не удалось найти вторую вакансию"
    elif vacancy1 is None and vacancy2 is None:
        return "Не удалось найти одну или обе вакансии."

    if vacancy1 == vacancy2:
        return "Обе вакансии имеют одинаковые зарплатные условия."
    elif vacancy1 > vacancy2:
        return "Первая вакансия имеет более высокие зарплатные условия."
    elif vacancy1 < vacancy2:
        return "Вторая вакансия имеет более высокие зарплатные условия."
    else:
        return "Зарплатные условия вакансий различны."


def remove_vacancy_from_json():
    """
        Удалить вакансию из JSON по её ID.

        Запрашивает ID вакансии, которую нужно удалить, и удаляет её из файла JSON.

        :return: None
    """
    pk = input("Введите ID вакансии, которую хотите удалить: ")
    jvs = JsonVacancyStorage(path="../data/vacancies.json")

    jvs.remove_vacancy(vacancy_id=pk)


def search_by_criterion():
    """
       Поиск вакансий по ключевому слову в описании.

       Запрашивает ключевое слово у пользователя и ищет вакансии, в описании которых оно встречается.

       :return: None
    """
    criterion = input("Введите ключевое слово для поиска: ")
    jvs = JsonVacancyStorage(path="../data/vacancies.json")
    matched = jvs.get_vacancies(criterion)

    if len(matched) == 0:
        print("К сожалению ничего не найдено")
    else:
        for vacancy in matched:
            print(vacancy)
            print("-" * 100)
