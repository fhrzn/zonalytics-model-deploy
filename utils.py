import bcrypt
from settings import JWT_SECRET_KEY
from flask_mysqldb import MySQLdb
from flask import jsonify

from app import db

import os
import jwt

def validate_user_input(input_type, **kwargs):
    if input_type == "authentication":
        if len(kwargs['email']) <= 255 and len(kwargs['password']) <= 255:
            return True
        else:
            return False

def db_read(query, params=None):
    cursor = db.connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    entries = cursor.fetchall()
    cursor.close()
    content = []

    for entry in entries:
        content.append(entry)

    return content

def db_write(query, params):
    cursor = db.connection.cursor()
    try:
        cursor.execute(query, params)
        db.connection.commit()
        cursor.close()
        return True
        
    except MySQLdb._exceptions.IntegrityError:
        cursor.close()
        return False

def generate_hash(plain_password):
    password_hash = plain_password.encode('utf-8')
    return bcrypt.hashpw(password_hash, bcrypt.gensalt())

def generate_jwt_token(content):
    encoded_content = jwt.encode(content, JWT_SECRET_KEY, algorithm="HS256")
    token = str(encoded_content).split("'")[1]
    return token

def validate_user(email, password):
    current_user = db_read("""SELECT * FROM users WHERE email = %s""", (email,))

    if len(current_user) == 1:
        saved_password = current_user[0]['password']
        # pass_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())        

        # if pass_hash == saved_password:        
        if bcrypt.checkpw(password.encode('utf-8'), saved_password.encode('utf-8')):
            user_id = current_user[0]['id']
            jwt_token = generate_jwt_token({"id": user_id})
            return jsonify({
                "token": jwt_token,
                "user": {
                    "id"    : current_user[0]['id'],
                    "email" : current_user[0]['email']
                }
            })
        else:
            return False
    return False