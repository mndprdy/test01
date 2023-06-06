from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db = mysql.connector.connect(
    host="db",
    user="root",
    password="root",
    database="test_db"
)

def create_user_table():
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))")

@app.route('/users', methods=['GET'])
def get_users():
    create_user_table()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    users_list = []
    for user in users:
        user_dict = {
            'id': user[0],
            'name': user[1],
            'email': user[2]
        }
        users_list.append(user_dict)
    return jsonify(users_list)

@app.route('/users', methods=['POST'])
def add_user():
    create_user_table()
    name = request.json['name']
    email = request.json['email']
    cursor = db.cursor()
    sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
    values = (name, email)
    cursor.execute(sql, values)
    db.commit()
    return jsonify({'message': 'User added successfully'})

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    create_user_table()
    name = request.json['name']
    email = request.json['email']
    cursor = db.cursor()
    sql = "UPDATE users SET name = %s, email = %s WHERE id = %s"
    values = (name, email, user_id)
    cursor.execute(sql, values)
    db.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    create_user_table()
    cursor = db.cursor()
    sql = "DELETE FROM users WHERE id = %s"
    values = (user_id,)
    cursor.execute(sql, values)
    db.commit()
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
    

