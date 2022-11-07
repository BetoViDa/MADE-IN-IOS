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
from dotenv import load_dotenv # esto para las variables de entorno .env
import os 
from flask import Flask, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__) #inicializamos la app
CORS(app) # se ocupa por ahora

load_dotenv() # cargamos las variables de entorno


DBpassword = os.getenv("PASSWORD")
DBuser = os.getenv("USER")
DataBase = os.getenv("DATABASE")


#=====Conexión a la base de datos=======
app.config['MONGO_URI'] = 'mongodb+srv://'+DBuser+':'+DBpassword+'@cluster0.sismnd1.mongodb.net/'+DataBase
mongo = PyMongo(app) #mongo es nuestra base de datos (mongo.db)
#=======================================

#-----------CHEQUEO API--------------
@app.route('/', methods=["GET"])
def chequeo():
    return "<p>Hola mundo</p>"
#====================================

#------------------------------SIGN UP USER----------------------------------
#falta cifrar datos sensibles como password y correo
@app.route('/user/signup', methods=['POST'])
def create_user():
    json = request.json
    # si encuentra un usuario con ese username manda error
    if mongo.db.users.find_one({'username':json['username']}) != None:
        return {'ERROR': 'ya existe este username'}
    # si encuentro un usuario con este email mando error
    if mongo.db.users.find_one({'email':json['email']}) != None:
        return {'ERROR': 'ya esta en uso este correo'}
    # si encuentra que ya hay un admin en ese grupo
    if ("group" in json) and mongo.db.users.find_one({
                                '$and': [
                                    {'type': 1},
                                    {'group': json['group']}
                                ]
                            }): # consulta BD para ver si existe o no
        return {'ERROR': 'este grupo ya tiene un administrador'} # regresamos el error
    
    if json['username'] and json['password'] and json['email'] and (json['type'] != None):
        id = mongo.db.users.insert_one(json)
        json['_id'] = str(id.inserted_id)
        return json # regresamos el json que se inserto 
    else:
        return {'msj': 'falta un campo'} # mensaje de error 
#=====================================================================================================

#-----------------------------LOGIN---------------------------------------
#falta cifrado de la contraseña para comparar contraseña cifrada con no cifrada
@app.route('/user/login', methods=['POST'])
def login():
    json = request.json
    #reviso si el usuario puso su username o su correo
    if "@" in json['username']: #es un correo
        data = mongo.db.users.find_one({'email':json['username'], 'password': json['password']})
    else:
        data = mongo.db.users.find_one({'username':json['username'], 'password': json['password']})

    if data == None:
        if "@" in json['username']:
            return {'ERROR': "correo o contraseña incorrecta"}
        else:
            return {'ERROR': "nombre de usuario o contraseña incorrecta"}
    else:
        return{
            '_id': str(data['_id']),
            'username': data['username'],
            'email': data['email']
        }
#=========================================================================    

if __name__ == "__main__":
    app.run(debug=True)




'''
A continuación ejemplo para insertar las palabras en la base de datos
El siguiente comando debe ser ejecutado en un playgroun de mongodb
para eso metete a tu mongo db, y le das a conectarte con vscode
(debes tener la extencion de mongodb instalada en vscode)
luego te va a dar un link, en vscode le das a agruegar connections
y pones el link donde te dice, en el link debes sustituir "<username>" por
el nombre de usuario que hayas creado en mongo y "<password>" por la 
contraseña de ese usuario. ahi te vas a conectar al cluster
en la parte de la izquierda, donde creaste la conexión en vscode
ahi otra opción que dice "create new playgroun",le das click
borras todo lo que tiene y escribes lo siguiente

use('signaDB');

db.word.insertMany([
  {'name':'palabra1', 'video':'link al video', 'img': 'link a la imagen'},
  {'name':'palabra2', 'video':'link al video', 'img': 'link a la imagen'}
])

el use es para decire que base de datos usar, y el insertMany es una
funcion que recibe un arreglo de jsons, los cuales son los datos de las palabras


IMPORTANTE
con el ejemplo anterior tendriamos que crear otra tabla para las categorias
sinembargo hay una alternativa que nos ahorra una tabla, y es hacer
unicamente una tabla de categorias, esta tabla guardaria un arreglo 
de palabras, tendriamos algo asi....

use('signDB')

db.categories.insertMany([
    {'name':'letras', 'level':1, 'words':[
                                        {'name':'A', 'video':'link/A.mp4', 'img': 'link/A.png'},
                                        {'name':'B', 'video':'link/B.mp4', 'img': 'link/B.png'}
                                        ]},
    {'name':'animales', 'level':1, 'words':[
                                        {'name':'perro', 'video':'link/perro.mp4', 'img': 'link/perro.png'},
                                        {'name':'gato', 'video':'link/gato.mp4', 'img': 'link/gato.png'}
                                        ]}                           
])



'''