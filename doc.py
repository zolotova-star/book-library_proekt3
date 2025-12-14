"""Скрипт для проверки всех докстрингов."""

print("=" * 80)
print("Проверка пакета booklib")
print("=" * 80)
import booklib
help(booklib)

print("\n" + "=" * 80)
print("Проверка модуля models.py")
print("=" * 80)
from booklib import models
help(models)

print("\n" + "=" * 80)
print("Проверка класса Book")
print("=" * 80)
from booklib.models import Book
help(Book)

print("\n" + "=" * 80)
print("Проверка модуля filters.py")
print("=" * 80)
from booklib import filters
help(filters)

print("\n" + "=" * 80)
print("Проверка модуля storage.py")
print("=" * 80)
from booklib import storage
help(storage)

print("\n" + "=" * 80)
print("Проверка модуля commands.py")
print("=" * 80)
from booklib import commands
help(commands)

print("\n" + "=" * 80)
print("Проверка модуля create_db.py")
print("=" * 80)
import create_db
help(create_db)

print("\n" + "=" * 80)
print("Проверка модуля main.py")
print("=" * 80)
import main
help(main)