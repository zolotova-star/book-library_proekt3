"""
Скрипт для инициализации базы данных.
Запускать только один раз.
"""

try:
    from booklib.storage import LibraryStorage
    storage = LibraryStorage()
    print(f" База данных успешно подключена.")
    print(f" Загружено книг: {len(storage.books)}")

except Exception as e:
    print(f" Ошибка: {e}")