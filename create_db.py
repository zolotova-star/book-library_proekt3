"""Модуль для создания базы данных книжной библиотеки.

Содержит функцию для создания базы данных PostgreSQL с необходимыми
таблицами для хранения книг и цитат. Используется для инициализации
системы хранения данных при первом запуске приложения.

Функции:
    create_database: Основная функция создания БД и таблиц.
"""

import psycopg2


def create_database():
    """Создает базу данных и необходимые таблицы для книжной библиотеки.

    Выполняет следующие операции:
    1. Подключается к серверу PostgreSQL с помощью учетных данных по умолчанию.
    2. Создает новую базу данных 'book_library'.
    3. Подключается к созданной базе данных.
    4. Создает таблицы 'books' и 'quotes' со связью один-ко-многим.
    5. Настраивает каскадное удаление цитат при удалении книги.

    Raises:
        psycopg2.OperationalError: При ошибках подключения к серверу БД.
        psycopg2.errors.DuplicateDatabase: При попытке создать уже существующую БД.
        Exception: При любых других ошибках выполнения SQL-запросов.

    Note:
        - Для работы функции требуется запущенный сервер PostgreSQL.
        - Учетные данные подключения жестко закодированы в функции.
        - Функция создает базу данных с кодировкой UTF-8.
        - Таблица 'quotes' имеет внешний ключ с каскадным удалением.

    Examples:
        create_database()
        База данных успешно создана.

        # При повторном запуске
        create_database()
        Ошибка: база данных "book_library" уже существует
    """
    try:
        # Подключение к системной базе данных postgres для создания новой БД
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="11111",
            host="localhost",
            port="5432",
            client_encoding='utf8'
        )
        conn.autocommit = True  # Включение автоматического сохранения изменений
        cur = conn.cursor()

        # Создание новой базы данных
        cur.execute("CREATE DATABASE book_library")
        print("База данных 'book_library' создана.")

        cur.close()
        conn.close()

        # Подключение к созданной базе данных
        conn = psycopg2.connect(
            dbname="book_library",
            user="postgres",
            password="11111",
            host="localhost",
            port="5432",
            client_encoding='utf8'
        )
        cur = conn.cursor()

        # Создание таблицы для книг
        cur.execute("""
            CREATE TABLE books (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER NOT NULL,
                genre TEXT NOT NULL
            )
        """)
        print("Таблица 'books' создана.")

        # Создание таблицы для цитат с внешним ключом
        cur.execute("""
            CREATE TABLE quotes (
                id SERIAL PRIMARY KEY,
                book_id INTEGER NOT NULL,
                quote TEXT NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
            )
        """)
        print("Таблица 'quotes' создана.")

        conn.commit()
        cur.close()
        conn.close()

        print("База данных успешно инициализирована.")

    except psycopg2.errors.DuplicateDatabase:
        print("Ошибка: база данных 'book_library' уже существует.")
    except psycopg2.OperationalError as e:
        print(f"Ошибка подключения к PostgreSQL: {e}")
        print("Убедитесь, что сервер PostgreSQL запущен.")
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")


if __name__ == "__main__":
    """Точка входа при прямом запуске скрипта.

    При запуске скрипта напрямую (не как модуль) вызывается
    функция создания базы данных.
    """
    create_database()