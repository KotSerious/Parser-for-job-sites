from abc import ABC, abstractmethod


class ApiHandler(ABC):
    """
    Абстрактный базовый класс для обработки API-запросов.

    Этот класс определяет интерфейс для обработки запросов к API. Он содержит абстрактные методы,
    которые должны быть реализованы в подклассах для конкретных API.

    Атрибуты:
        Нет публичных атрибутов.

    Методы:
        get_request(self, search_term: str, city: str = None, experience: str = None, count=None):
            Абстрактный метод для отправки запроса к API.

            :param search_term: Термин поиска или ключевая фраза.
            :type search_term: str

            :param city: Город для фильтрации результатов (по умолчанию None).
            :type city: str or None

            :param experience: Уровень опыта для фильтрации результатов (по умолчанию None).
            :type experience: str or None

            :param count: Количество результатов для запроса (по умолчанию None).
            :type count: int or None

            :return: Результаты запроса к API.
            :rtype: List[dict]

        _parse(raw_response: dict) -> list:
            Абстрактный статический метод для разбора ответа от API.

            :param raw_response: Словарь с данными от API.
            :type raw_response: dict

            :return: Результаты, полученные из ответа API.
            :rtype: List[dict]

    Пример использования:
        class MyApiHandler(ApiHandler):
            def get_request(self, search_term: str, city: str = None, experience: str = None, count=None):
                # Реализация отправки запроса к конкретному API.

            @staticmethod
            def _parse(raw_response: dict) -> list:
                # Реализация разбора ответа от конкретного API.
    """

    @abstractmethod
    def get_request(self, search_term: str, city: str = None, experience: str = None, count=None):
        pass

    @staticmethod
    @abstractmethod
    def _parse(raw_response: dict) -> list:
        pass
