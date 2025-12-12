import psycopg2
from .models import Book


class LibraryStorage:
    def __init__(self):
        self.books = self.load_books()

    def _connect(self):
        return psycopg2.connect(
            dbname="book_library",
            user="postgres",
            password="11111",
            host="localhost",
            port="5432"
        )

    def load_books(self):
        books = []
        try:
            conn = self._connect() #подключаемься
            cur = conn.cursor() #метод подключения - создаем курсор

            cur.execute("SELECT id, title, author, year, genre FROM books ORDER BY id") #выборка по колонкам из таблицы книг и сортировка по возрастанию id
            books_data = cur.fetchall() #возвращает все строки результата запроса в виде списка кортежей

            for book_data in books_data:
                book_id, title, author, year, genre = book_data #book_data = (1, 'Война и мир', 'Толстой', 1869, 'Роман')

                cur.execute("SELECT quote FROM quotes WHERE book_id = %s", (book_id,)) #запрос цитат по айди, получает скрытое введенное значение
                quotes_data = cur.fetchall()
                quotes = [q[0] for q in quotes_data] #цитаты поиск

                book = Book(title, author, year, genre, quotes)
                book.id = book_id #cохраняет связь между объектом Python и записью в БД
                books.append(book)

            cur.close() # закрывает соединение с курсором
            conn.close() # закрывает соединение с базой данных

        except Exception as e:
            print(f"Ошибка загрузки: {e}")

        return books

    def get_all_books(self):
        """Возвращает все книги."""
        return self.books

    def add_book(self, book):
        try:
            conn = self._connect()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO books (title, author, year, genre)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (book.title, book.author, book.year, book.genre))
             #рбращаемься к таблице books, чтобы ввести кортеж book.title, book.author, book.year, book.genre

            book_id = cur.fetchone()[0] #получаем только id

            for quote in book.quotes:
                cur.execute("""
                    INSERT INTO quotes (book_id, quote)
                    VALUES (%s, %s)
                """, (book_id, quote))

            conn.commit() #сохраняем изменения
            cur.close()
            conn.close()

            book.id = book_id
            self.books.append(book)

        except Exception as e:
            print(f"Ошибка добавления: {e}")

    def remove_book(self, book_id):
        """Удаляет книгу по ID."""
        try:
            conn = self._connect()
            cur = conn.cursor()

            cur.execute("DELETE FROM books WHERE id = %s", (book_id,))
            conn.commit()

            cur.close()
            conn.close()

            self.books = [b for b in self.books if b.id != book_id]

        except Exception as e:
            print(f"Ошибка удаления: {e}")

    def add_quote_to_book(self, book_id, quote):
        """Добавляет цитату к книге."""
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

            for book in self.books:
                if book.id == book_id: #Проверяем ID текущей книги равен переданному book_id?
                    book.quotes.append(quote) #в список цитат этой книги добавляем цитату
                    break

        except Exception as e:
            print(f"Ошибка добавления цитаты: {e}")

    def remove_quote(self, book_id, quote_index):
        """Удаляет цитату по индексу."""
        try:
            conn = self._connect()
            cur = conn.cursor()

            # Находим ВСЕ цитаты книги по её book_id
            cur.execute("SELECT id FROM quotes WHERE book_id = %s ORDER BY id", (book_id,))
            quotes = cur.fetchall() # получаем список ВСЕХ ID цитат этой книги

            if 0 <= quote_index < len(quotes):
                # Берём ID конкретной цитаты по её позиции (индексу) в списке
                quote_id = quotes[quote_index][0]
                cur.execute("DELETE FROM quotes WHERE id = %s", (quote_id,)) # Удаляем цитату по её ID
                conn.commit()
                success = True
            else:
                success = False

            cur.close()
            conn.close()

            if success: #нужно удалить книги не только в базе данных
                for book in self.books:
                    if book.id == book_id and quote_index < len(book.quotes):
                        book.quotes.pop(quote_index) #Выполняем удаление элемента по индексу цитаты из локального списка
                        break

            return success

        except Exception as e:
            print(f"Ошибка удаления цитаты: {e}")
            return False

    def export_to_csv(self, filename='export.csv'):
        """Экспортирует данные в CSV файл."""
        import csv

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f) #Преобразовывать списки Python в строки CSV
            writer.writerow(['title', 'author', 'year', 'genre', 'quotes']) #заголовок 1 строки

            for book in self.books:
                quotes_str = '|'.join(book.quotes)
                writer.writerow([book.title, book.author, book.year, book.genre, quotes_str])

    def update_book(self, old_book, new_book):
        """Обновляет книгу в БД."""
        try:
            conn = self._connect()
            cur = conn.cursor()

            cur.execute("""
                UPDATE books 
                SET title = %s, author = %s, year = %s, genre = %s
                WHERE id = %s
            """, (new_book.title, new_book.author, new_book.year, new_book.genre, old_book.id)) #обновляем таблицу, set указывает каке поля менять и на какие значения

            conn.commit()
            cur.close()
            conn.close()

            for i, book in enumerate(self.books):
                if book.id == old_book.id:
                    self.books[i] = new_book
                    break

        except Exception as e:
            print(f"Ошибка обновления: {e}")