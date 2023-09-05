import os

import requests

from src.api.ApiHandler import ApiHandler
from src.models.Vacancy import Vacancy


class SuperJobAPI(ApiHandler):
    """
    Класс для взаимодействия с API SuperJob и поиска вакансий.

    Attributes:
        _base_url (str): Базовый URL API SuperJob.

    Methods:
        get_request(self, search_term: str, city: str = None, experience: str = None, count=None, order_by=None) -> list[Vacancy]:
            Отправляет запрос к API SuperJob для поиска вакансий с заданными параметрами.

        _parse(raw_response: dict) -> list:
            Парсит JSON-ответ от API SuperJob и возвращает список объектов Vacancy.

    """

    def __init__(self):
        self._base_url = "https://api.superjob.ru/2.0/vacancies/"

    def get_request(self, search_term: str, city: str = None, experience: str = None, count=None, order_by=None) \
            -> list[Vacancy]:
        """
                Отправляет запрос к API SuperJob для поиска вакансий.

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
            params = {
                "keyword": search_term,
                "town": city,
                "experience": experience,
                "count": count,
                "order_field": order_by
            }

            headers = {
                "X-Api-App-Id": os.getenv("SJ_API_KEY")
            }

            response = requests.get(self._base_url, params=params, headers=headers)

            if response.status_code == 200:  # Проверяем статус-код тут
                data = response.json()  # Парсим JSON-ответ
                import pprint
                pprint.pprint(data)  # DEBUG

                if len(data) == 0:
                    print("Nothing found")
                    return []
                else:
                    return SuperJobAPI._parse(data)
            elif response.status_code == 404:
                raise Exception("Request failed (404 status code)")

        except requests.exceptions.RequestException:
            return []

    @staticmethod
    def _parse(raw_response: dict) -> list:
        """
               Парсит JSON-ответ от API SuperJob и возвращает список объектов Vacancy.

               :param raw_response: JSON-ответ от API SuperJob.
               :type raw_response: dict

               :return: Список объектов Vacancy, представляющих найденные вакансии.
               :rtype: list[Vacancy]
        """
        vacancy_list = []

        for item in raw_response.get('objects'):
            from_salary = float(item.get('payment_from')) if item.get('payment_from') != 0 else None
            to_salary = float(item.get('payment_to')) if item.get('payment_to') != 0 else None
            currency = str(item.get('currency'))

            vacancy = Vacancy(
                int(item.get('id', "Нет данных")),
                str(item.get('profession', "Нет данных")),
                str(item.get('employer', {}).get('name', "Нет данных")),
                str(item.get('candidat', "Нет данных")),
                from_salary,
                to_salary,
                currency,
                str(item.get('town', {}).get('title', "Нет данных")),
                str(item.get('link', "Нет данных"))
            )
            vacancy_list.append(vacancy)

        return vacancy_list


class ControllerSuperJob:
    """
        Класс-контроллер для управления параметрами запросов к API SuperJob.

        Methods:
            validate_city(city: str):
                Проверяет, существует ли указанный город в API SuperJob.

            order_by(param: str):
                Возвращает параметр сортировки для запроса.

    """

    @staticmethod
    def validate_city(city: str):
        """
               Проверяет, существует ли указанный город в API SuperJob.

               :param city: Название города.
               :type city: str

               :return: Название города, если он существует, в противном случае - None.
               :rtype: str or None
        """
        if len(city) == 0:
            # if city is empty
            return None
        else:
            url = "https://api.superjob.ru/2.0/towns/"

            headers = {
                "X-Api-App-Id": os.getenv("SJ_API_KEY")
            }
            # Getting JSON with cities
            response = requests.get(url, headers=headers).json()

            # Checking if city exists in json
            for item in response["objects"]:
                if item['title'] == city:
                    return city
        return None

    @staticmethod
    def order_by(param: str):
        """
        Возвращает параметр сортировки для запроса.

        :param param: Строковое значение, определяющее параметр сортировки.
        :type param: str

        :return: Параметр сортировки для запроса.
        :rtype: str
        """
        if param == "1":
            return "date"
        elif param == "2":
            return "payment_desc"
        else:
            return "relevance"
