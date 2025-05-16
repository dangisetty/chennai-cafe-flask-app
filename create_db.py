import sqlite3

def create_tables():
    conn = sqlite3.connect('cafe.db')  # no templates/ prefix
    c = conn.cursor()

    # Create Feedback table
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            dish TEXT,
            message TEXT
        )
    ''')

    # Create Products table
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price REAL,
            quantity INTEGER
        )
    ''')

    # Create Accounts table
    c.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT UNIQUE,
            phone TEXT
        )
    ''')

    # Create Orders table
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            item TEXT,
            quantity INTEGER,
            notes TEXT,
            email TEXT
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
