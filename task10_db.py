import pyodbc


def initialize_sqlite3():
    try:
        connection = pyodbc.connect('DRIVER={SQLite3 ODBC Driver};'
                                    'SERVER=localhost;'
                                    'DATABASE=news.sqlite;')
        cursor = connection.cursor()

        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE DEFAULT CURRENT_DATE,
                city TEXT,
                text TEXT,
                CONSTRAINT unique_news_record UNIQUE (date, text, city)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE DEFAULT CURRENT_DATE,
                text TEXT,
                expiration_date DATE, 
                CONSTRAINT unique_ads_record UNIQUE (date, text, expiration_date)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE DEFAULT CURRENT_DATE,
                city TEXT,
                temperature INT,
                CONSTRAINT unique_weather_record UNIQUE (date, city, temperature)
            )
        ''')

        connection.commit()
        print("SQLite3 tables created successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    initialize_sqlite3()
