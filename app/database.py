import sqlite3

def create_connection():
    conn = sqlite3.connect('ignyt.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customer (
            cust_id TEXT PRIMARY KEY,
            cust_name TEXT,
            cust_phone TEXT,
            cust_mail_id TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reservation (
            reserve_id TEXT PRIMARY KEY,
            cust_id TEXT,
            no_of_ppl INTEGER,
            date DATE,
            time TIME,
            FOREIGN KEY (cust_id) REFERENCES Customer(cust_id)
        )
    ''')
    # Create Restaurant table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Restaurant (
        rest_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        address TEXT,
        phone_no TEXT,
        timings TEXT,
        email_id TEXT
    )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = create_connection()
    create_tables(conn)
    return conn
    