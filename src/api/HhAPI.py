import requests

from src.api.ApiHandler import ApiHandler
from src.models.Vacancy import Vacancy


class HhAPI(ApiHandler):
    """
    Класс для взаимодействия с API HeadHunter и поиска вакансий.

    Attributes:
        _base_url (str): Базовый URL API HeadHunter.

    Methods:
        get_request(self, search_term: str, city: str = None, experience: str = None, count=None, order_by=None) -> list[Vacancy]:
            Отправляет запрос к API HeadHunter для поиска вакансий с заданными параметрами.

        _parse(data_from_json: dict) -> list:
            Парсит JSON-ответ от API HeadHunter и возвращает список объектов Vacancy.

    """

    def __init__(self):
        self._base_url = 'https://api.hh.ru'

    def get_request(self, search_term: str, city: str = None, experience: str = None, count=None, order_by=None) \
            -> list[Vacancy]:
        """
                Отправляет запрос к API HeadHunter для поиска вакансий.

                :param search_term: Термин поиска или ключевая фраза.
                :type search_term: str

                :param city: Город для фильтрации результатов (по умолчанию None).
                :type city: str or None

                :param experience: Уровень опыта для фильтрации результатов (по умолчанию None).
                :type experience: str or None

                :param count: Количество результатов для запроса (по умолчанию None).
                :type count: int or None

                :param order_by: Параметр сортировки результатов (по умолчанию None).
                :type order_by: str or None

                :return: Список объектов Vacancy, представляющих найденные вакансии.
                :rtype: list[Vacancy]
                """
        try:
            response = requests.get(f"{self._base_url}/vacancies",
                                    params={
                                        "text": search_term,
                                        "area": city,
                                        "experience": experience,
                                        "per_page": count,
                                        "order_by": order_by,
                                    })

            if response.status_code == 200:  # Проверяем статус-код тут
                data_from_json = response.json()  # Парсим JSON-ответ
                if data_from_json['found'] == 0:
                    print("Nothing found")
                    return []
                else:
                    return HhAPI._parse(data_from_json)
            elif response.status_code == 404:
                raise Exception("Request failed (404 status code)")

        except requests.exceptions.RequestException:
            return []

    @staticmethod
    def _parse(data_from_json: dict) -> list:
        """
                Парсит JSON-ответ от API HeadHunter и возвращает список объектов Vacancy.

                :param data_from_json: JSON-ответ от API HeadHunter.
                :type data_from_json: dict

                :return: Список объектов Vacancy, представляющих найденные вакансии.
                :rtype: list[Vacancy]
                """
        vacancy_list = []

        for item in data_from_json.get('items'):
            salary = item.get('salary', {})

            if salary:
                from_salary = float(salary.get('from')) if salary.get('from') is not None else None
                to_salary = float(salary.get('to')) if salary.get('to') is not None else None
                currency = str(salary.get('currency')) if salary.get('currency') is not None else None
            else:
                from_salary = to_salary = currency = None

            vacancy = Vacancy(
                int(item.get('id', "Нет данных")),
                str(item.get('name', "Нет данных")),
                str(item.get('employer', {}).get('name', "Нет данных")),
                str(item.get('snippet', "Нет данных").get('requirement', "Нет данных")),
                from_salary,
                to_salary,
                currency,
                str(item.get('area', {}).get('name', "Нет данных")),
                str(item.get('alternate_url', "Нет данных"))
            )
            vacancy_list.append(vacancy)

        return vacancy_list


class ControllerHH:
    """
        Класс-контроллер для управления параметрами запросов к API HeadHunter.

        Methods:
            get_city_id(city: str):
                Получает идентификатор города по его названию.

            order_by(param: str):
                Возвращает параметр сортировки для запроса.

        """

    @staticmethod
    def get_city_id(city: str):
        """
                Получает идентификатор города по его названию.

                :param city: Название города.
                :type city: str

                :return: Идентификатор города в API HeadHunter.
                :rtype: int or None
                """
        if len(city) == 0:
            return None
        else:
            response = requests.get("https://api.hh.ru/areas").json()

            for area in response:
                for country in area["areas"]:
                    if "areas" in country and country["areas"]:  # Проверяем наличие и непустой список areas
                        for region in country["areas"]:
                            if region["name"] == city:
                                return region["id"]
                    elif country["name"] == city:  # Если список пустой, сравниваем имя страны с городом
                        return country["id"]

    @staticmethod
    def order_by(param: str):
        """
                Возвращает параметр сортировки для запроса.

                :param param: Строковое значение, определяющее параметр сортировки.
                :type param: str

                :return: Параметр сортировки для запроса.
                :rtype: str or None
                """

        if param == "1":
            return "publication_time"
        elif param == "2":
            return "salary_desc"
        else:
            return None
