# API Para la aplicación signa de lenguaje de señas
'''
pasos:
    python3 -m venv venv                         creamos entorno virtual llamado "venv"
    venv\Scripts\activate    en MacOS ejecutar:  source venv/bin/activate
    pip install <lo que se deba instalar> 
    python3 src/api.py                           corremos la api estando en la carpeta API
'''
# <lo que se debe instalar>
# pip install flask          Componente basico 
# pip install pymongo        
# pip install flask-pymongo 
# pip install flask-cors
# pip install python-dotenv  Para el archivo .env

import os
from dotenv import load_dotenv, dotenv_values
from flask import Flask, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

load_dotenv()
DataBase = os.getenv("DATABASE")
DBuser = os.getenv("USER")
DBpassword = os.getenv("PASSWORD")

#CONEXION A LA BASE DE DATOS
app.config['MONGO_URI'] = 'mongodb+srv://'+DBuser+':'+DBpassword+'@cluster0.fabcj3i.mongodb.net/'+DataBase
mongo = PyMongo(app)

@app.route('/')
def chequeo():
    return "<p>Hola mundo</p>"

@app.route('/user/signup', methods=['POST'])
def signup():
    json = request.json
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    type = request.json['type']
    group = request.json['group']
    

    if mongo.db.users.find_one({'username':username}) != None:
        return {'ERROR': 'ya existe este username'}
    if mongo.db.users.find_one({'email':email}) != None:
        return {'ERROR': 'ya existe este email'}
    if mongo.db.users.find_one({'type':1, 'group':group}) != None:
        return {'ERROR': 'este grupo ya tiene un administrador'}
        
    if username and password and email and (type != None):
        return json


if __name__ == "__main__":
    app.run(debug=True)
