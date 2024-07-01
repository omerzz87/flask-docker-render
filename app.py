from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = 'garage.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

def check_car_exists(cursor, car_name):
    cursor.execute('SELECT 1 FROM cars WHERE Car = ?', (car_name,))
    return cursor.fetchone() is not None

@app.route('/add', methods=['GET'])
def add_made_up_cars():
    made_up_cars = [
        ("Futuro", "DreamCars", 2099),
        ("SkyFlyer", "SkyMotors", 2105)
    ]
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if cars already exist to prevent duplicates
    cars_to_add = [car for car in made_up_cars if not check_car_exists(cursor, car[0])]
    
    if cars_to_add:
        cursor.executemany('INSERT INTO cars (Car, Make, Year) VALUES (?, ?, ?)', cars_to_add)
        conn.commit()
        message = f"{len(cars_to_add)} made-up cars added successfully."
    else:
        message = "No new cars were added. Cars already exist."
    
    conn.close()
    return jsonify({"message": message}), 200

@app.route('/')
def users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cars')
    cars_data = cursor.fetchall()
    conn.close()
    # Convert the rows to a list of dicts to jsonify
    cars_list = [dict(row) for row in cars_data]
    return jsonify(cars_list)

if __name__ == '__main__':
    app.run(debug=True)