import psycopg2

class Database:
    def __init__(self, url):
        self.connection = psycopg2.connect(url)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            name TEXT,
            description TEXT,
            price TEXT,
            rating TEXT
        )
        ''')

    def insert_book(self, book):
        sql = '''INSERT INTO books (name, description, price, rating) VALUES (%s, %s, %s, %s)'''
        self.cursor.execute(sql, (book['name'], book['description'], book['price'], book['rating']))
