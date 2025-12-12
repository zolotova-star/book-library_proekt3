"""
Модуль для поиска и сортировки книг.
"""

class BookFilter:
    """Класс для фильтрации и сортировки коллекции книг."""

    def search_books(self, books, **kwargs): #любое количество аргументов по типу автор и год, или только автор
        """Универсальный поиск книг по нескольким критериям."""
        results = books #нужно временную переменную, чтобы списки книг обновлялись

        for key, value in kwargs.items(): #key='author', value='Толстой'
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
        """Сортирует книги по указанному полю."""
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