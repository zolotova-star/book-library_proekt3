"""Модуль команд для управления книжной библиотекой через PostgreSQL.

Этот модуль содержит класс LibraryCommands, который предоставляет
действия такие как: удаление, изменение, добавление, для книг и цитат через командную строку.

Для этого испортируем:
    models-Делает класс Book доступным в этом файле, чтобы можно было создавать объекты книг
    storage-Делает доступным класс для работы с хранением данных (PostgreSQL).
    Этот класс отвечает за загрузку и сохранение книг в базу данных
    BookFilter- Делает доступным класс для фильтрации и сортировки книг (поиск по автору, названию)
"""

from .models import Book
from .storage import LibraryStorage
from .filters import BookFilter

class LibraryCommands:
    """Основной класс для управления операциями библиотеки.

    Предоставляет методы для добавления, удаления, поиска, редактирования
    книг и работы с цитатами.

    Attributes:
        storage (LibraryStorage): Объект для работы с базой данных.
    """

    def __init__(self):
        """Инициализирует объект LibraryCommands.

        Создает подключение атрибут - хранилище данных.
        """
        self.storage = LibraryStorage()

    def add_book(self, title, author, year, genre):
        """Добавляет новую книгу в библиотеку.
        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (str or int): Год издания.
            genre (str): Жанр книги.
        Raises:
            ValueError: Если год не может быть преобразован в целое число.
            Exception: При ошибке подключения к базе данных.
        try:
            int(year) — преобразует строку year в целое число
            Book(...) — создает объект класса Book из models.py
            self.storage ранее добавленный объект использует метод add_book(book)
        """
        try:
            year = int(year)
            book = Book(title, author, year, genre)
            self.storage.add_book(book)
            print(f"Книга успешно добавлена в базу данных.")
        except ValueError:
            print("Ошибка, год должен быть числом.")


    def remove_book(self, title=None, author=None):
        """Удаляет книгу из библиотеки по названию или автору (также возможны оба варианта).

        Изначальные значения названия и автора не указаны.

        Если найдено несколько книг, запрашивает у пользователя выбор.

        Args:
            title (str, optional): Часть названия книги для поиска.
            author (str, optional): Часть имени автора для поиска.

        Note:
            Если не указаны ни title, ни author, будут показаны все книги
            для выбора.
            Если указаны оба параметра, ищутся книги, соответствующие обоим критериям.
        """
        books = self.storage.get_all_books()
        books_to_remove = []

        """Сохранение значений в параметрах.
        
            Args:
                 список объектов Book, все книги в библиотеке.
                books_to_remove-Здесь будут накапливаться книги, которые нужно удалить.
        """

        for book in books:
            title_match = title is None or title.lower() in book.title.lower()
            author_match = author is None or author.lower() in book.author.lower()

            if title_match and author_match:
                books_to_remove.append(book)

        if not books_to_remove:
            print("Книги не найдены.")
            return

        if len(books_to_remove) == 1:
            book = books_to_remove[0] #из списка берем только эту книгу
            self.storage.remove_book(book.id)
            print(f"Книга удалена.")
        else:
            print("Найдено несколько книг:")
            for i, book in enumerate(books_to_remove, 1):
                print(f"{i}. {book}")

            try:
                book_num_del = int(input("Номер какой книги вы хотите удалить: ")) - 1
                if 0 <= book_num_del < len(books_to_remove):
                    self.storage.remove_book(books_to_remove[book_num_del].id) #находим книгу, и только затем определяем айди

                    print("Книга удалена.")
            except (ValueError, IndexError):
                print("Неверный выбор.")

    def list_books(self, sort_by='title', reverse=False):
        """Выводит список всех книг в библиотеке с возможностью сортировки.

        Args:
            sort_by (str)-поле для выбора сортировки, по умолчанию "название":
                          'title', 'author', 'year', 'genre'.
            reverse (bool): Если True, сортировка в обратном порядке.

        Note:
            Показывает количество цитат для каждой книги.
        """
        books = self.storage.get_all_books() #вывод всех книг
        sorted_books = BookFilter().sort_books(books, sort_by, reverse) #сортировка списка книг

        if not sorted_books:
            print("Библиотека пуста.")
            return

        print("Список книг в библиотеке:")
        print(f"Всего книг: {len(sorted_books)}")

        for i, book in enumerate(sorted_books, 1):
            quotes_count = len(book.quotes) #считает количество цитат по строчам
            print(f"{i}. '{book.title}' - {book.author} ({book.year}), {book.genre}, количество цитат {quotes_count}.")

    def search_books(self, author=None, title=None, year=None, genre=None):
        """Ищет книги по указанным критериям.

        Args:
            author-Часть имени автора для поиска, указано изначально пусто.
            title-Часть названия книги для поиска.
            year-Точный год издания.
            genre Часть названия жанра для поиска.

        Raises:
            ValueError: Если год не может быть преобразован в целое число.

        Note:
            Поиск по всем критериям чувствителен к регистру.
            Можно комбинировать несколько критериев поиска.
        """
        try:
            if year:
                year = int(year)

            books = self.storage.get_all_books()
            results = BookFilter().search_books(books, author=author, title=title, year=year, genre=genre)
            #.search_books(books, author=None, title="война", year=None, genre=None)

            if not results:
                print("Книги не найдены.")
                return

            print(f"Найдено {len(results)} книг.")
            for i, book in enumerate(results, 1):
                print(f"{i}. {book}")
        except ValueError:
            print("Ошибка, год должен быть числом.")

    def add_quote(self, title, author, quote):
        """
        Добавляет цитату к указанной книге.

        Args:
            title (str): Название книги (частичное совпадение).
            author (str): Автор книги (частичное совпадение).
            quote (str): Текст цитаты для добавления.

        Note:
            Если найдено несколько книг, запрашивает выбор у пользователя.
        """
        books = self.storage.get_all_books()
        filtered_books = BookFilter().search_books(books, title=title, author=author)

        if not filtered_books:
            print("Книга не найдена")
            return

        if len(filtered_books) == 1:
            book = filtered_books[0]
        else:
            print("Найдено несколько книг:")
            for i, book in enumerate(filtered_books, 1):
                print(f"{i}. {book}")

            try:
                choice = int(input("Выберите номер книги: ")) - 1
                book = filtered_books[choice]
            except (ValueError, IndexError):
                print("Неверный выбор")
                return

        self.storage.add_quote_to_book(book.id, quote)
        print(f"Цитата добавлена к книге '{book.title}'")

    def remove_quote(self, title, author, quote_index=None):
        """
        Удаляет цитату из указанной книги.

        Args:
            title (str): Название книги (частичное совпадение).
            author (str): Автор книги (частичное совпадение).
            quote_index (int, optional): Номер цитаты для удаления (начиная с 1).
                                        Если не указан, показывает список цитат.

        Note:
            Если найдено несколько книг, запрашивает выбор у пользователя.
            Если quote_index не указан, показывает все цитаты для выбора.
        """
        books = self.storage.get_all_books()
        filtered_books = BookFilter().search_books(books, title=title, author=author)

        if not filtered_books:
            print("Книга не найдена")
            return

        if len(filtered_books) == 1:
            book = filtered_books[0]
        else:
            print("Найдено несколько книг:")
            for i, book in enumerate(filtered_books, 1):
                print(f"{i}. {book}")

            try:
                choice = int(input("Выберите номер книги: ")) - 1
                book = filtered_books[choice]
            except (ValueError, IndexError):
                print("Неверный выбор")
                return

        if not book.quotes:
            print("У книги нет цитат")
            return

        if quote_index is None:
            print(f"Цитаты книги '{book.title}':")
            for i, quote in enumerate(book.quotes, 1):
                print(f"{i}. {quote}")

            try:
                quote_index = int(input("Выберите номер цитаты для удаления: ")) - 1
            except ValueError:
                print("Ошибка: введите число")
                return

        if self.storage.remove_quote(book.id, quote_index):
            print("Цитата удалена.")
        else:
            print("Неверный номер цитаты")

    def show_quotes(self, title=None, author=None):
        """
        Показывает цитаты для указанной книги или всех книг.

        Args:
            title (str, optional): Название книги для фильтрации.
            author (str, optional): Автор книги для фильтрации.

        Note:
            Если не указаны ни title, ни author, показывает цитаты всех книг.
        """
        books = self.storage.get_all_books()

        if title or author:
            filtered_books = BookFilter().search_books(books, title=title, author=author)
            books = filtered_books

        if not books:
            print("Книги не найдены")
            return

        found_quotes = False
        for book in books:
            if book.quotes:
                print(f"\nЦитаты из книги '{book.title}':")
                for i, quote in enumerate(book.quotes, 1):
                    print(f"{i}. {quote}")
                found_quotes = True

        if not found_quotes:
            print("Цитаты не найдены")

    def export_to_csv(self,filename='export.csv'):
        """
        Экспортирует все данные из базы данных в CSV файл.

        Note:
            Создает файл 'library_export.csv' в текущей директории.
            Формат: title,author,year,genre,quotes
        """
        self.storage.export_to_csv(filename)


    def clear_database(self):
        """
        Очищает все данные из таблиц базы данных.

        Warning:
            Удаляет все книги и цитаты, но оставляет структуру базы данных.
            Требует подтверждения пользователя.
        """
        confirm = input("Удалить все книги и цитаты? (yes/no): ")

        if confirm.lower() == 'yes':
            try:
                import psycopg2
                conn = psycopg2.connect(
                    dbname="book_library",
                    user="postgres",
                    password="11111",
                    host="localhost",
                    port="5432"
                )
                cur = conn.cursor()

                cur.execute("DELETE FROM books")
                conn.commit()

                cur.close()
                conn.close()

                self.storage.books = [] #ощищаем кеш локальной памяти

                print("Все данные удалены.")

            except Exception as e:
                print(f"Ошибка: {e}")
        else:
            print("Очистка отменена")

    def edit_book(self, title, author, new_title=None, new_author=None, new_year=None, new_genre=None):
        """
        Редактирует существующую книгу.

        Args:
            title (str): Текущее название книги.
            author (str): Текущий автор книги.
            new_title (str, optional): Новое название книги.
            new_author (str, optional): Новый автор книги.
            new_year (int, optional): Новый год издания.
            new_genre (str, optional): Новый жанр книги.

        Raises:
            ValueError: Если new_year не может быть преобразован в целое число.

        Note:
            Если найдено несколько книг, запрашивает выбор у пользователя.
            Обновляет только указанные поля.
        """
        books = self.storage.get_all_books()
        filtered_books = BookFilter().search_books(books, title=title, author=author)

        if not filtered_books:
            print("Книга не найдена")
            return

        if len(filtered_books) > 1:
            print("Найдено несколько книг:")
            for i, book in enumerate(filtered_books, 1):
                print(f"{i}. {book}")
            try:
                choice = int(input("Выберите номер книги для редактирования: ")) - 1
                book = filtered_books[choice]
            except (ValueError, IndexError):
                print("Неверный выбор")
                return
        else:
            book = filtered_books[0]

        old_title, old_author = book.title, book.author

        if new_title:
            book.title = new_title
        if new_author:
            book.author = new_author
        if new_year:
            try:
                book.year = int(new_year)
            except ValueError:
                print("Ошибка: год должен быть числом")
                return
        if new_genre:
            book.genre = new_genre

        try:
            import psycopg2
            conn = psycopg2.connect(
                dbname="book_library",
                user="postgres",
                password="11111",
                host="localhost",
                port="5432"
            )
            cur = conn.cursor()

            cur.execute("""
                UPDATE books 
                SET title = %s, author = %s, year = %s, genre = %s
                WHERE title = %s AND author = %s
            """, (book.title, book.author, book.year, book.genre, old_title, old_author))

            conn.commit()
            cur.close()
            conn.close()

            print(f"Книга '{old_title}' успешно обновлена.")

        except Exception as e:
            print(f"Ошибка при обновлении: {e}")