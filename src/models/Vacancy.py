class Vacancy:
    """
        Класс, представляющий информацию о вакансии.

        Attributes:
            id_num (int): Уникальный идентификатор вакансии.
            vacancy_name (str): Название вакансии.
            company_name (str): Название компании, разместившей вакансию.
            description (str): Описание вакансии.
            salary_from (float): Минимальная зарплата (если есть) или 0, если информации нет.
            salary_to (float): Максимальная зарплата (если есть) или 0, если информации нет.
            salary_currency (str): Валюта зарплаты (например, "USD", "RUB", "Нет данных").
            area (str): Местоположение вакансии.
            url (str): URL-адрес вакансии.

        Methods:
            _validate_data(self):
                Внутренний метод для проверки корректности данных в объекте.

            __str__(self):
                Возвращает строковое представление объекта.

            to_dict(self):
                Возвращает объект в виде словаря.

            __eq__(self, other):
                Проверяет, равны ли объекты по зарплате.

            __lt__(self, other):
                Сравнивает объекты по минимальной зарплате.

            __le__(self, other):
                Сравнивает объекты по минимальной зарплате (включая равенство).

            __gt__(self, other):
                Сравнивает объекты по максимальной зарплате.

            __ge__(self, other):
                Сравнивает объекты по максимальной зарплате (включая равенство).

        """

    def __init__(self, id_num, vacancy_name, company_name, description, salary_from, salary_to, salary_currency,
                 area, url):
        """
                Инициализирует объект Vacancy.

                :param id_num: Уникальный идентификатор вакансии.
                :type id_num: int

                :param vacancy_name: Название вакансии.
                :type vacancy_name: str

                :param company_name: Название компании, разместившей вакансию.
                :type company_name: str

                :param description: Описание вакансии.
                :type description: str

                :param salary_from: Минимальная зарплата (если есть) или 0, если информации нет.
                :type salary_from: float

                :param salary_to: Максимальная зарплата (если есть) или 0, если информации нет.
                :type salary_to: float

                :param salary_currency: Валюта зарплаты (например, "USD", "RUB", "Нет данных").
                :type salary_currency: str

                :param area: Местоположение вакансии.
                :type area: str

                :param url: URL-адрес вакансии.
                :type url: str
                """
        self.id_num = id_num
        self.vacancy_name = vacancy_name
        self.company_name = company_name
        self.description = description
        self.salary_from = salary_from if salary_from is not None else 0
        self.salary_to = salary_to if salary_to is not None else 0
        self.salary_currency = salary_currency if salary_currency is not None else "Нет данных"
        self.area = area
        self.url = url

        self._validate_data()

    def _validate_data(self):
        """
            Внутренний метод для проверки корректности данных в объекте.
        """
        if not isinstance(self.id_num, int):
            raise ValueError("ID должно быть целым числом")

        if not isinstance(self.vacancy_name, str):
            raise ValueError("Название вакансии должно быть строкой")

        if not isinstance(self.company_name, str):
            raise ValueError("Название компании должно быть строкой")

        if not isinstance(self.description, str):
            raise ValueError("Описание вакансии должно быть строкой")

        if not isinstance(self.salary_from, (int, float)):
            raise ValueError("Зарплата 'from' должна быть числом (целым или десятичным)")

        if not isinstance(self.salary_to, (int, float)):
            raise ValueError("Зарплата 'to' должна быть числом (целым или десятичным) или None")

        if not isinstance(self.salary_currency, str):
            raise ValueError("Валюта зарплаты должна быть строкой")

        if not isinstance(self.area, str):
            raise ValueError("Местоположение должно быть строкой")

        if not isinstance(self.url, str):
            raise ValueError("URL должен быть строкой")

    def __str__(self):
        """
                Возвращает строковое представление объекта.

                :return: Строковое представление объекта.
                :rtype: str
        """
        if self.salary_from == 0 and self.salary_to == 0:
            salary_range = "Информации нет"
        else:
            from_part = f"От {int(self.salary_from)} " if self.salary_from != 0 else ""
            to_part = f"До {int(self.salary_to)} " if self.salary_to != 0 else ""
            salary_range = f"{from_part}{to_part}{self.salary_currency}"

        return f"ID: {self.id_num}\n" \
               f"Название вакансии: {self.vacancy_name}\n" \
               f"Название компании: {self.company_name}\n" \
               f"Описание: {self.description}\n" \
               f"Зарплата: {salary_range}\n" \
               f"Местоположение: {self.area}\n" \
               f"URL: {self.url}"

    def to_dict(self):
        """
                Возвращает объект в виде словаря.

                :return: Словарь, представляющий объект Vacancy.
                :rtype: dict
        """
        return {
            "id_num": self.id_num,
            "vacancy_name": self.vacancy_name,
            "company_name": self.company_name,
            "description": self.description,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "salary_currency": self.salary_currency,
            "area": self.area,
            "url": self.url
        }

    def __eq__(self, other):
        """
                Проверяет, равны ли объекты по зарплате.

                :param other: Другой объект Vacancy для сравнения.
                :type other: Vacancy

                :return: True, если объекты равны по зарплате, в противном случае - False.
                :rtype: bool
        """
        are_salaries_equal = (
                self.salary_from == other.salary_from and
                self.salary_to == other.salary_to and
                self.salary_currency == other.salary_currency
        )
        return are_salaries_equal

    def __lt__(self, other):
        result = self.salary_from < other.salary_from
        return result

    def __le__(self, other):
        result = self.salary_from <= other.salary_from
        return result

    def __gt__(self, other):
        result = self.salary_to > other.salary_to
        return result

    def __ge__(self, other):
        result = self.salary_to >= other.salary_to
        return result
