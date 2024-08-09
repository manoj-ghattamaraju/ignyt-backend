from flask import Flask, jsonify, request
import json
from database import get_db_connection
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

get_db_connection()

# Function to establish a connection to the database
def db_connection():
    conn = sqlite3.connect('ignyt.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_next_customer_id(cursor):
    cursor.execute('SELECT COUNT(*) FROM Customer')
    count = cursor.fetchone()[0]
    return 'c' + str(count + 1)

def get_next_reservation_id(cursor):
    cursor.execute('SELECT COUNT(*) FROM Reservation')
    count = cursor.fetchone()[0]
    return 'r' + str(count + 1)

# API endpoint to add a new reservation
@app.route('/reserve', methods=['POST'])
def add_reservation():
    db = db_connection()
    cursor = db.cursor()

    data = request.get_json()

    try: 
        cust_id = get_next_customer_id(cursor)

        # Add new customer to Customer table
        cursor.execute('INSERT INTO Customer (cust_id, cust_name, cust_phone, cust_mail_id) VALUES (?, ?, ?, ?)',
                        (cust_id, data['cust_name'], data['cust_phone'], data['cust_mail_id']))

        reserve_id = get_next_reservation_id(cursor)

        # Add new reservation to Reservation table
        cursor.execute('INSERT INTO Reservation (reserve_id, cust_id, no_of_ppl, date, time, message) VALUES (?, ?, ?, ?, ?, ?)',
                        (reserve_id, cust_id, data['no_of_ppl'], data['date'], data['time'], data['message']))

        db.commit()
        db.close()

        return jsonify({'message': 'Reservation added successfully', 'statusCode': 'S'})

    except Exception:
        db.rollback()
        db.close()
        return jsonify({'message': 'Failed to add reservation', 'statusCode': 'F'})

@app.route('/restaurant', methods=['GET'])
def get_restaurant_details():
    db = db_connection()
    cursor = db.cursor()

    details = cursor.execute('SELECT * FROM Restaurant')
    data = [dict(row) for row in details]
    return json.dumps(data)

@app.route('/get-reservations', methods=['GET'])
def get_restaurant_details():
    db = db_connection()
    cursor = db.cursor()

    details = cursor.execute('SELECT * FROM Reservation')
    data = [dict(row) for row in details]
    return json.dumps(data)

if __name__ == '__main__':
    app.run(debug=True)
