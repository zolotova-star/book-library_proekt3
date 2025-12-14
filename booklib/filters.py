"""Модуль для поиска и сортировки книг.

Содержит класс BookFilter, который предоставляет методы для фильтрации
книг по различным критериям и их сортировки по выбранным полям.

Классы:
    BookFilter: Основной класс для фильтрации и сортировки книг.
"""


class BookFilter:
    """Класс для фильтрации и сортировки коллекций книг.

    Предоставляет методы для поиска книг по различным критериям
    (автор, название, год, жанр) и сортировки результатов.
    """

    def search_books(self, books, **kwargs):
        """Универсальный поиск книг по нескольким критериям.

        Ищет книги в переданной коллекции по указанным критериям.
        Поддерживает поиск по автору, названию, году и жанру.
        Критерии можно комбинировать.

        Args:
            books (list): Список объектов Book для поиска.
            **kwargs: Ключевые аргументы для фильтрации. Возможные ключи:
                author (str, optional): Часть имени автора для поиска.
                title (str, optional): Часть названия книги для поиска.
                year (int, optional): Точный год издания.
                genre (str, optional): Часть названия жанра для поиска.

        Returns:
            list: Список объектов Book, удовлетворяющих всем критериям поиска.

        Note:
            Поиск по строковым полям (автор, название, жанр) не чувствителен
            к регистру. Год проверяется на точное совпадение.
        """
        results = books  # нужно временную переменную, чтобы списки книг обновлялись

        for key, value in kwargs.items():  # key='author', value='Толстой'
            if value is None:
                continue

            if key == 'author':
                results = [b for b in results if value.lower() in b.author.lower()]
            elif key == 'title':
                results = [b for b in results if value.lower() in b.title.lower()]
            elif key == 'year':
                results = [b for b in results if b.year == value]
            elif key == 'genre':
                results = [b for b in results if value.lower() in b.genre.lower()]

        return results

    def sort_books(self, books, sort_by='title', reverse=False):
        """Сортирует книги по указанному полю.

        Сортирует список книг по возрастанию или убыванию (если reverse=True)
        по выбранному полю.

        Args:
            books (list): Список объектов Book для сортировки.
            sort_by (str, optional): Поле для сортировки. Возможные значения:
                'title' - по названию (по умолчанию)
                'author' - по автору
                'year' - по году издания
                'genre' - по жанру
            reverse (bool, optional): Если True, сортировка в обратном порядке.
                По умолчанию False.

        Returns:
            list: Отсортированный список объектов Book.

        Note:
            Если указано неизвестное поле сортировки, возвращается исходный
            список без изменений.
        """
        if sort_by == 'title':
            return sorted(books, key=lambda x: x.title, reverse=reverse)
        elif sort_by == 'author':
            return sorted(books, key=lambda x: x.author, reverse=reverse)
        elif sort_by == 'year':
            return sorted(books, key=lambda x: x.year, reverse=reverse)
        elif sort_by == 'genre':
            return sorted(books, key=lambda x: x.genre, reverse=reverse)
        else:
            return books