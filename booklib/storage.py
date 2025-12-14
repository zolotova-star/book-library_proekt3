"""Модуль для работы с хранением данных книжной библиотеки в PostgreSQL.

Содержит класс LibraryStorage, который обеспечивает взаимодействие
с базой данных PostgreSQL для операций CRUD (создание, чтение, обновление,
удаление) с книгами и цитатами.

Классы:
    LibraryStorage: Основной класс для работы с хранилищем данных.
"""

import psycopg2
from .models import Book


class LibraryStorage:
    """Класс для управления хранением данных книжной библиотеки в PostgreSQL.

    Обеспечивает загрузку, сохранение, обновление и удаление книг и цитат
    из базы данных. Также поддерживает локальный кеш загруженных книг
    для повышения производительности.

    Attributes:
        books (list): Локальный кеш загруженных книг (объектов Book).
    """

    def __init__(self):
        """Инициализирует объект LibraryStorage и загружает книги из БД.

        При создании объекта автоматически загружает все книги
        из базы данных в локальный кеш.
        """
        self.books = self.load_books()

    def _connect(self):
        """Создает подключение к базе данных PostgreSQL.

        Returns:
            psycopg2.extensions.connection: Объект подключения к БД.

        Note:
            Параметры подключения жестко закодированы в методе.
            Для продакшн-окружения рекомендуется выносить их в конфигурационный файл.
        """
        return psycopg2.connect(
            dbname="book_library",
            user="postgres",
            password="11111",
            host="localhost",
            port="5432",
            client_encoding='utf8'
        )

    def load_books(self):
        """Загружает все книги и их цитаты из базы данных.

        Выполняет запросы к таблицам books и quotes для получения
        полной информации о книгах и связанных с ними цитатах.

        Returns:
            list: Список объектов Book, загруженных из базы данных.

        Note:
            В случае ошибки подключения или выполнения запроса
            метод возвращает пустой список.
        """
        books = []
        try:
            conn = self._connect()
            cur = conn.cursor()

            # Выборка всех книг с сортировкой по id
            cur.execute("SELECT id, title, author, year, genre FROM books ORDER BY id")
            books_data = cur.fetchall()

            for book_data in books_data:
                book_id, title, author, year, genre = book_data

                # Загрузка цитат для текущей книги
                cur.execute("SELECT quote FROM quotes WHERE book_id = %s", (book_id,))
                quotes_data = cur.fetchall()
                quotes = [q[0] for q in quotes_data]

                book = Book(title, author, year, genre, quotes)
                book.id = book_id  # Сохраняем связь между объектом Python и записью в БД
                books.append(book)

            cur.close()
            conn.close()

        except Exception as e:
            print(f"Ошибка загрузки: {e}")

        return books

    def get_all_books(self):
        """Возвращает все книги из локального кеша.

        Returns:
            list: Список всех объектов Book, загруженных в память.

        Note:
            Если требуется свежие данные из БД, следует вызвать load_books()
            или пересоздать объект LibraryStorage.
        """
        return self.books

    def add_book(self, book):
        """Добавляет новую книгу в базу данных.

        Сохраняет книгу в таблицу books и все связанные с ней цитаты
        в таблицу quotes. Также обновляет локальный кеш.

        Args:
            book (Book): Объект книги для добавления.

        Note:
            После успешного добавления объекту book присваивается
            сгенерированный БД идентификатор (id).
        """
        try:
            conn = self._connect()
            cur = conn.cursor()

            # Вставка книги и получение сгенерированного id
            cur.execute("""
                INSERT INTO books (title, author, year, genre)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (book.title, book.author, book.year, book.genre))

            book_id = cur.fetchone()[0]

            # Вставка всех цитат книги
            for quote in book.quotes:
                cur.execute("""
                    INSERT INTO quotes (book_id, quote)
                    VALUES (%s, %s)
                """, (book_id, quote))

            conn.commit()
            cur.close()
            conn.close()

            book.id = book_id
            self.books.append(book)

        except Exception as e:
            print(f"Ошибка добавления: {e}")

    def remove_book(self, book_id):
        """Удаляет книгу из базы данных по идентификатору.

        Args:
            book_id (int): Идентификатор книги для удаления.

        Note:
            Благодаря каскадному удалению (ON DELETE CASCADE) все цитаты,
            связанные с книгой, также будут автоматически удалены.
        """
        try:
            conn = self._connect()
            cur = conn.cursor()

            cur.execute("DELETE FROM books WHERE id = %s", (book_id,))
            conn.commit()

            cur.close()
            conn.close()

            # Обновляем локальный кеш
            self.books = [b for b in self.books if b.id != book_id]

        except Exception as e:
            print(f"Ошибка удаления: {e}")

    def add_quote_to_book(self, book_id, quote):
        """Добавляет цитату к существующей книге.

        Args:
            book_id (int): Идентификатор книги, к которой добавляется цитата.
            quote (str): Текст цитаты для добавления.

        Returns:
            None: Метод ничего не возвращает, но обновляет БД и локальный кеш.
        """
        try:
            conn = self._connect()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO quotes (book_id, quote)
                VALUES (%s, %s)
            """, (book_id, quote))

            conn.commit()
            cur.close()
            conn.close()

            # Обновляем локальный кеш
            for book in self.books:
                if book.id == book_id:
                    book.quotes.append(quote)
                    break

        except Exception as e:
            print(f"Ошибка добавления цитаты: {e}")

    def remove_quote(self, book_id, quote_index):
        """Удаляет цитату из книги по индексу.

        Args:
            book_id (int): Идентификатор книги, из которой удаляется цитата.
            quote_index (int): Индекс цитаты в списке (начиная с 0).

        Returns:
            bool: True если цитата успешно удалена, False в противном случае.

        Note:
            Метод удаляет цитату как из базы данных, так и из локального кеша.
        """
        try:
            conn = self._connect()
            cur = conn.cursor()

            # Находим все цитаты книги для получения их id
            cur.execute("SELECT id FROM quotes WHERE book_id = %s ORDER BY id", (book_id,))
            quotes = cur.fetchall()

            if 0 <= quote_index < len(quotes):
                # Получаем id конкретной цитаты по индексу
                quote_id = quotes[quote_index][0]
                cur.execute("DELETE FROM quotes WHERE id = %s", (quote_id,))
                conn.commit()
                success = True
            else:
                success = False

            cur.close()
            conn.close()

            # Обновляем локальный кеш
            if success:
                for book in self.books:
                    if book.id == book_id and quote_index < len(book.quotes):
                        book.quotes.pop(quote_index)
                        break

            return success

        except Exception as e:
            print(f"Ошибка удаления цитаты: {e}")
            return False

    def export_to_csv(self, filename='export.csv'):
        """Экспортирует все книги и цитаты в CSV файл.

        Args:
            filename (str, optional): Имя файла для экспорта.
                По умолчанию 'export.csv'.

        Note:
            Цитаты в файле разделяются символом '|'.
            Файл создается в кодировке UTF-8.
        """
        import csv

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['title', 'author', 'year', 'genre', 'quotes'])

            for book in self.books:
                quotes_str = '|'.join(book.quotes)
                writer.writerow([book.title, book.author, book.year, book.genre, quotes_str])

    def update_book(self, old_book, new_book):
        """Обновляет информацию о книге в базе данных.

        Args:
            old_book (Book): Исходный объект книги (с оригинальными данными).
            new_book (Book): Обновленный объект книги с новыми данными.

        Note:
            Метод обновляет запись в БД и локальный кеш.
            Идентификатор книги (id) остается неизменным.
        """
        try:
            conn = self._connect()
            cur = conn.cursor()

            cur.execute("""
                UPDATE books 
                SET title = %s, author = %s, year = %s, genre = %s
                WHERE id = %s
            """, (new_book.title, new_book.author, new_book.year, new_book.genre, old_book.id))

            conn.commit()
            cur.close()
            conn.close()

            # Обновляем локальный кеш
            for i, book in enumerate(self.books):
                if book.id == old_book.id:
                    self.books[i] = new_book
                    break

        except Exception as e:
            print(f"Ошибка обновления: {e}")