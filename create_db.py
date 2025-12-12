import psycopg2

def create_database():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="11111",
            host="localhost",
            port="5432"
        )
        conn.autocommit = True #автоматического сохранения изменений.
        cur = conn.cursor()

        cur.execute("CREATE DATABASE book_library")

        cur.close()
        conn.close()

        conn = psycopg2.connect(
            dbname="book_library",
            user="postgres",
            password="11111",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE books (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER NOT NULL,
                genre TEXT NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE quotes (
                id SERIAL PRIMARY KEY,
                book_id INTEGER NOT NULL,
                quote TEXT NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_database()