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
        rest_id INTEGER,
        name TEXT,
        address TEXT,
        phone_no TEXT,
        timings TEXT,
        email_id TEXT
    )
    ''')

    conn.commit()

def insert_into_restaurant(conn):
    
    cursor = conn.cursor()
    rest_id = 1
    name = 'IGNYT - The Beer Station'
    address = '178/6 14th main road, 20th, 50th Main Rd, Kumaraswamy Layout, Bengaluru, Karnataka 560078'
    phone_no = '+91 82177 79517'
    timings = '11AM - 12:30AM'
    email_id = 'ignyttbs@gmail.com'
    cursor.execute('''
    INSERT INTO Restaurant (
        rest_id, 
        name, 
        address, 
        phone_no,
        timings, 
        email_id ) 
        VALUES (?,?,?,?,?,?)
    ''',
    (rest_id, name, address, phone_no, timings, email_id))
    conn.commit()

def get_db_connection():
    conn = create_connection()
    create_tables(conn)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Restaurant')
    count = cursor.fetchone()[0]
    if count == 0:
        insert_into_restaurant(conn)
    conn.close()
    return conn
    