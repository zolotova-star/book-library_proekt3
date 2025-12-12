import argparse
from booklib import LibraryCommands

def main():
    parser = argparse.ArgumentParser(description='Книжная библиотека.') #создаем пустой шаблок для объекта с классом, который будет преобразовывать строку
    subparsers = parser.add_subparsers(dest='command')

    # ДОБАВЛЕНО: Команда создания БД
    create_db_parser = subparsers.add_parser('create-db', help='Создать базу данных')

    # ДОБАВЛЕНО: Команда проверки БД
    check_parser = subparsers.add_parser('check', help='Проверить подключение к БД')

    # Команда добавления книги
    add_parser = subparsers.add_parser('add', help='Добавить книгу')
    add_parser.add_argument('--title', required=True) #обязательный аргумент
    add_parser.add_argument('--author', required=True)
    add_parser.add_argument('--year', required=True, type=int)
    add_parser.add_argument('--genre', required=True)

    remove_parser = subparsers.add_parser('remove', help='Удалить книгу')
    remove_parser.add_argument('--title', help='Название')
    remove_parser.add_argument('--author', help='Автор')

    list_parser = subparsers.add_parser('list', help='Список книг')
    list_parser.add_argument('--sort-by', choices=['title', 'author', 'year', 'genre'], default='title') #сколько значений можешь ввести
    list_parser.add_argument('--reverse', action='store_true') #флаг (переключатель), который либо есть, либо его нет.

    search_parser = subparsers.add_parser('search', help='Поиск')
    search_parser.add_argument('--author', help='Автор')
    search_parser.add_argument('--title', help='Название')
    search_parser.add_argument('--year', type=int, help='Год')
    search_parser.add_argument('--genre', help='Жанр')

    add_quote_parser = subparsers.add_parser('add-quote', help='Добавить цитату')
    add_quote_parser.add_argument('--title', required=True)
    add_quote_parser.add_argument('--author', required=True)
    add_quote_parser.add_argument('--quote', required=True)

    remove_quote_parser = subparsers.add_parser('remove-quote', help='Удалить цитату')
    remove_quote_parser.add_argument('--title', required=True)
    remove_quote_parser.add_argument('--author', required=True)
    remove_quote_parser.add_argument('--quote-index', type=int, help='Номер цитаты')

    show_quotes_parser = subparsers.add_parser('show-quotes', help='Показать цитаты')
    show_quotes_parser.add_argument('--title', help='Название')
    show_quotes_parser.add_argument('--author', help='Автор')

    # Команда: экспорт в CSV
    export_parser = subparsers.add_parser('export', help='Экспорт в CSV')
    export_parser.add_argument('--file', default='export.csv', help='Имя файла')

    # Команда: очистить данные
    clear_parser = subparsers.add_parser('clear-db', help='Очистить все данные из таблиц (безопасно)')
    clear_parser.add_argument('--confirm', action='store_true', help='Подтвердить очистку')

    # Команда: редактировать книгу
    edit_parser = subparsers.add_parser('edit', help='Редактировать книгу')
    edit_parser.add_argument('--title', required=True, help='Текущее название')
    edit_parser.add_argument('--author', required=True, help='Текущий автор')
    edit_parser.add_argument('--new-title', help='Новое название')
    edit_parser.add_argument('--new-author', help='Новый автор')
    edit_parser.add_argument('--new-year', type=int, help='Новый год')
    edit_parser.add_argument('--new-genre', help='Новый жанр')

    args = parser.parse_args()

    #если нет введенной команды, выведем справочник команд
    if not args.command:
        parser.print_help()
        return
    #если введено создание базы, то мы загружаем функцию create_database из файла create_db.py
    if args.command == 'create-db':
        from create_db import create_database
        create_database() #начинаем функцию
        return

    if args.command == 'check':
        try:
            from booklib.storage import LibraryStorage # Загружает класс LibraryStorage из файла booklib/storage.py.
            storage = LibraryStorage() #создаем объект
            print(f"база данных подключена")
            print(f"книг в базе: {len(storage.books)}")
        except Exception as e:
            print(f"Ошибка: {e}")
        return

    # Обработка остальных команд
    commands = LibraryCommands()

    # 3. Команды, которые требуют LibraryCommands
    if args.command == 'add':
        commands.add_book(args.title, args.author, args.year, args.genre)
    elif args.command == 'remove':
        commands.remove_book(args.title, args.author)
    elif args.command == 'list':
        commands.list_books(args.sort_by, args.reverse)
    elif args.command == 'search':
        commands.search_books(author=args.author, title=args.title, year=args.year, genre=args.genre)
    elif args.command == 'add-quote':
        commands.add_quote(args.title, args.author, args.quote)
    elif args.command == 'remove-quote':
        commands.remove_quote(args.title, args.author, args.quote_index)
    elif args.command == 'show-quotes':
        commands.show_quotes(args.title, args.author)
    elif args.command == 'export':
        commands.export_to_csv(args.file)  # ← БЕЗ повторного создания!
    elif args.command == 'clear-db':
        if args.confirm:
            commands.clear_database()
        else:
            print("Используйте: python main.py clear-db --confirm")
    elif args.command == 'edit':
        commands.edit_book(
            args.title, args.author,
            args.new_title, args.new_author,
            args.new_year, args.new_genre
        )

if __name__ == '__main__':
    main()