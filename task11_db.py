import pyodbc


def initialize_sqlite3():
    try:
        connection = pyodbc.connect('DRIVER={SQLite3 ODBC Driver};'
                                    'SERVER=localhost;'
                                    'DATABASE=coordinates.sqlite;')
        cursor = connection.cursor()

        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS city_coordinates (
                     id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     city TEXT, 
                     latitude REAL, 
                     longitude REAL
            )
        ''')

        connection.commit()
        print("SQLite3 tables created successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    initialize_sqlite3()
