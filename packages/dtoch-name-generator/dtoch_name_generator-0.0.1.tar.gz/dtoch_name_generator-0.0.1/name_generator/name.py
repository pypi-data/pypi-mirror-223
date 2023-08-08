from __future__ import unicode_literals
from os.path import abspath, join, dirname
import random
import transliterate


def get_gender() -> str:
    return random.choice(('m', 'f'))


class NameGenerator:
    def __init__(self, gender: str = None, surname: str = None, name: str = None, patronymic: str = None, email: str = None):
        if gender is None:
            self.gender: str = get_gender()
        else:
            self.gender: str = gender

        self.surname: str | None = surname
        self.name: str | None = name
        self.patronymic: str | None = patronymic
        self.email: str | None = email

        self.files: dict = {
            'surname:f': self.__get_dict_path('dist.female.surname'),
            'name:f': self.__get_dict_path('dist.female.name'),
            'patronymic:f': self.__get_dict_path('dist.female.patronymic'),

            'surname:m': self.__get_dict_path('dist.male.surname'),
            'name:m': self.__get_dict_path('dist.male.name'),
            'patronymic:m': self.__get_dict_path('dist.male.patronymic'),
        }

    def __get_dict_path(self, filename: str) -> str:
        return abspath(join(dirname(__file__), 'files', filename))

    def __get_random_line(self, filename: str) -> str:
        lines = open(filename, "r", encoding="utf-8").read().splitlines()
        return random.choice(lines)

    def __get_gender(self, gender: str) -> str:
        if gender is None:
            gender = self.gender
        if gender not in ('m', 'f'):
            raise ValueError("Only 'm' and 'f' are supported as gender")
        return gender

    def get_gender(self) -> str:
        return self.gender

    def get_surname(self, gender: str = None) -> str:
        if self.surname is None:
            gender = self.__get_gender(gender)
            self.surname = self.__get_random_line(self.files['surname:%s' % gender]).capitalize()

        return self.surname

    def get_name(self, gender: str = None) -> str:
        if self.name is None:
            gender = self.__get_gender(gender)
            self.name = self.__get_random_line(self.files['name:%s' % gender]).capitalize()

        return self.name

    def get_patronymic(self, gender: str = None) -> str:
        if self.patronymic is None:
            gender = self.__get_gender(gender)
            self.patronymic = self.__get_random_line(self.files['patronymic:%s' % gender]).capitalize()

        return self.patronymic

    def get_full_name(self, gender: str = None) -> str:
        gender = self.__get_gender(gender)
        return f"{self.get_surname(gender)} {self.get_name(gender)} {self.get_patronymic(gender)}"

    def get_email(self, domain: str = "test.ru") -> str:
        self.email = \
            transliterate.translit(self.name, reversed=True).lower() \
            + "." \
            + transliterate.translit(self.surname, reversed=True).lower() \
            + "@" \
            + domain

        return self.email

