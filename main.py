"""Основной модуль командной строки для управления книжной библиотекой.

Предоставляет интерфейс командной строки для работы с книжной библиотекой
через PostgreSQL. Поддерживает все основные операции CRUD для книг и цитат,
а также дополнительные функции экспорта, импорта и управления базой данных.

Основные команды:
    create-db-Создание базы данных и таблиц
    check- Проверка подключения и состояния БД
    add-Добавление новой книги
    remove-Удаление книги
    list-Просмотр списка книг с сортировкой
    search-Поиск книг по критериям
    add-quote-Добавление цитаты к книге
    remove-quote-Удаление цитаты из книги
    show-quotes-Просмотр цитат
    export-Экспорт данных в CSV
    clear-db-Очистка всех данных из таблиц
    edit-Редактирование информации о книге

Примеры использования:
    python main.py create-db
    python main.py add --title "Война и мир" --author "Толстой" --year 1869 --genre "Роман"
    python main.py list --sort-by author --reverse
    python main.py search --author "Толстой" --genre "Роман"
"""

import argparse
from booklib import LibraryCommands


def main():
    """Основная функция обработки командной строки.

    Создает парсер аргументов, определяет все доступные команды и их параметры,
    затем вызывает соответствующие методы LibraryCommands для выполнения операций.

    Raises:
        SystemExit: При вызове с флагом --help или при ошибках парсинга аргументов.

    Returns:
        None: Функция ничего не возвращает, но выводит результаты в консоль.
    """
    # Создаем парсер аргументов командной строки
    parser = argparse.ArgumentParser(description='Книжная библиотека.')
    subparsers = parser.add_subparsers(dest='command')

    create_db_parser = subparsers.add_parser('create-db', help='Создать базу данных')
    check_parser = subparsers.add_parser('check', help='Проверить подключение к БД')

    # Команда добавления книги
    add_parser = subparsers.add_parser('add', help='Добавить книгу')
    add_parser.add_argument('--title', required=True)  # обязательный аргумент
    add_parser.add_argument('--author', required=True)
    add_parser.add_argument('--year', required=True, type=int)
    add_parser.add_argument('--genre', required=True)

    # Команда удаления книги
    remove_parser = subparsers.add_parser('remove', help='Удалить книгу')
    remove_parser.add_argument('--title', help='Название')
    remove_parser.add_argument('--author', help='Автор')

    # Команда списка книг
    list_parser = subparsers.add_parser('list', help='Список книг')
    list_parser.add_argument('--sort-by', choices=['title', 'author', 'year', 'genre'],
                             default='title')  # выбор сортировки
    list_parser.add_argument('--reverse', action='store_true')  # флаг обратной сортировки

    # Команда поиска
    search_parser = subparsers.add_parser('search', help='Поиск')
    search_parser.add_argument('--author', help='Автор')
    search_parser.add_argument('--title', help='Название')
    search_parser.add_argument('--year', type=int, help='Год')
    search_parser.add_argument('--genre', help='Жанр')

    # Команда добавления цитаты
    add_quote_parser = subparsers.add_parser('add-quote', help='Добавить цитату')
    add_quote_parser.add_argument('--title', required=True)
    add_quote_parser.add_argument('--author', required=True)
    add_quote_parser.add_argument('--quote', required=True)

    # Команда удаления цитаты
    remove_quote_parser = subparsers.add_parser('remove-quote', help='Удалить цитату')
    remove_quote_parser.add_argument('--title', required=True)
    remove_quote_parser.add_argument('--author', required=True)
    remove_quote_parser.add_argument('--quote-index', type=int, help='Номер цитаты')

    # Команда показа цитат
    show_quotes_parser = subparsers.add_parser('show-quotes', help='Показать цитаты')
    show_quotes_parser.add_argument('--title', help='Название')
    show_quotes_parser.add_argument('--author', help='Автор')

    # Команда экспорта в CSV
    export_parser = subparsers.add_parser('export', help='Экспорт в CSV')
    export_parser.add_argument('--file', default='export.csv', help='Имя файла')

    # Команда очистки данных
    clear_parser = subparsers.add_parser('clear-db', help='Очистить все данные из таблиц (безопасно)')
    clear_parser.add_argument('--confirm', action='store_true', help='Подтвердить очистку')

    # Команда редактирования книги
    edit_parser = subparsers.add_parser('edit', help='Редактировать книгу')
    edit_parser.add_argument('--title', required=True, help='Текущее название')
    edit_parser.add_argument('--author', required=True, help='Текущий автор')
    edit_parser.add_argument('--new-title', help='Новое название')
    edit_parser.add_argument('--new-author', help='Новый автор')
    edit_parser.add_argument('--new-year', type=int, help='Новый год')
    edit_parser.add_argument('--new-genre', help='Новый жанр')

    args = parser.parse_args()

    # Если нет введенной команды, выводим справочник команд
    if not args.command:
        parser.print_help()
        return

    # Если введено создание базы, загружаем функцию из create_db.py
    if args.command == 'create-db':
        from create_db import create_database
        create_database()  # начинаем функцию
        return

    if args.command == 'check':
        try:
            import psycopg2
            conn = psycopg2.connect(
                database="book_library",
                user="postgres",
                password="11111",
                host="localhost",
                client_encoding='utf8'
            )

            cur = conn.cursor()
            cur.execute(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'books')")  # возвращает true или false поиск таблицы книги
            books_table_exists = cur.fetchone()[0]  # t или f

            cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'quotes')")
            quotes_table_exists = cur.fetchone()[0]

            # Считаем количество книг
            if books_table_exists:
                cur.execute("SELECT COUNT(*) FROM books")
                books_count = cur.fetchone()[0]
            else:
                books_count = 0

            cur.close()
            conn.close()

            print(f"Таблица 'books' существует: {'Да' if books_table_exists else 'Нет'}")
            print(f"Таблица 'quotes' существует: {'Да' if quotes_table_exists else 'Нет'}")
            print(f"Книг в базе: {books_count}")

        except psycopg2.OperationalError as e:
            # Ошибка подключения
            print(f"Ошибка подключения: {e}")

    commands = LibraryCommands()

    # Обработка команды добавления книги
    if args.command == 'add':
        commands.add_book(args.title, args.author, args.year, args.genre)

    # Обработка команды удаления книги
    elif args.command == 'remove':
        commands.remove_book(args.title, args.author)

    # Обработка команды списка книг
    elif args.command == 'list':
        commands.list_books(args.sort_by, args.reverse)

    # Обработка команды поиска
    elif args.command == 'search':
        commands.search_books(author=args.author, title=args.title, year=args.year, genre=args.genre)

    # Обработка команды добавления цитаты
    elif args.command == 'add-quote':
        commands.add_quote(args.title, args.author, args.quote)

    # Обработка команды удаления цитаты
    elif args.command == 'remove-quote':
        commands.remove_quote(args.title, args.author, args.quote_index)

    # Обработка команды показа цитат
    elif args.command == 'show-quotes':
        commands.show_quotes(args.title, args.author)

    # Обработка команды экспорта
    elif args.command == 'export':
        commands.export_to_csv(args.file)  # используем переданное имя файла

    # Обработка команды очистки базы данных
    elif args.command == 'clear-db':
        if args.confirm:
            commands.clear_database()
        else:
            print("Используйте: python main.py clear-db --confirm")

    # Обработка команды редактирования книги
    elif args.command == 'edit':
        commands.edit_book(
            args.title, args.author,
            args.new_title, args.new_author,
            args.new_year, args.new_genre
        )


if __name__ == '__main__':
    """Точка входа при прямом запуске скрипта.

    При запуске скрипта напрямую вызывает функцию main(),
    которая обрабатывает аргументы командной строки.
    """
    main()