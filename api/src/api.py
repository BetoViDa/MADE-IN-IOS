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
        data = mongo.db.users.find_one({'email':json['username'], 'password': json['password']},{'_id':1,'username':1,'email':1,'group':1,'type':1})
    else:
        data = mongo.db.users.find_one({'username':json['username'], 'password': json['password']},{'_id':1,'username':1,'email':1,'group':1,'type':1})

    if data == None:
        if "@" in json['username']:
            return {'ERROR': "correo o contraseña incorrecta"}
        else:
            return {'ERROR': "nombre de usuario o contraseña incorrecta"}
    else:
        return{
            '_id': str(data['_id']),
            'username': data['username'],
            'email': data['email'],
            'group': data['group'],
            'type': data['type']
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

use('signDB')

el use es para decire que base de datos usar, y el insertMany es una
funcion que recibe un arreglo de jsons, los cuales son los datos de las palabras

------------------------------------EJEMPLO-------------------------------------------

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
--------------------------------------------------------------------------------------

db.categories.insertMany([
    {'name':'verboscomunes', 'level':1, 'words':[
                                        {'name':'trabajar', 'video':'https://drive.google.com/file/d/1hE6KI9x1R8JARjzqGpqwl3q7gSr9epZF/view?usp=share_link', 'img': 'null'},
                                        {'name':'vender', 'video':'https://drive.google.com/file/d/1d-0rGtR_vCGtMHrvGGcoMGlTRuKKIiOe/view?usp=share_link', 'img': 'null'},
                                        {'name':'terminar', 'video':'https://drive.google.com/file/d/1Y6bZb5vZQGVxuFST4tHntIpHa0Mubay_/view?usp=share_link', 'img': 'null'},
                                        {'name':'sentar', 'video':'https://drive.google.com/file/d/1JNA2N4mKh-IRiuuvaEBD2ou9HQ_RqKuN/view?usp=share_link', 'img': 'null'},
                                        {'name':'ver', 'video':'https://drive.google.com/file/d/16yHdpwYUjhadnViFZ6-1fcSYlZ4cc0e-/view?usp=share_link', 'img': 'null'},
                                        {'name':'preguntar', 'video':'https://drive.google.com/file/d/1zsv9aENoH7mQZqh6FfWR6nalDMUWyPZe/view?usp=share_link', 'img': 'null'},
                                        {'name':'vivir', 'video':'https://drive.google.com/file/d/1N1QCts462umG_XaTxBKE_VQJ2uVqWqcw/view?usp=share_link', 'img': 'null'},
                                        {'name':'olvidar', 'video':'https://drive.google.com/file/d/1J0hw1XUzdDRzqQUyKIX8TPaRKOcpfkFl/view?usp=share_link', 'img': 'null'},
                                        {'name':'pensar', 'video':'https://drive.google.com/file/d/1J0hw1XUzdDRzqQUyKIX8TPaRKOcpfkFl/view?usp=share_link', 'img': 'null'},
                                        {'name':'limpiar', 'video':'https://drive.google.com/file/d/1J0hw1XUzdDRzqQUyKIX8TPaRKOcpfkFl/view?usp=share_link', 'img': 'null'},
                                        {'name':'jugar', 'video':'https://drive.google.com/file/d/16yIVbzbYGUItoM28aIdCB5JIgq1aFJqN/view?usp=share_link', 'img': 'null'},
                                        {'name':'hacer', 'video':'https://drive.google.com/file/d/1wk202bGUbrmfys9Ruw1fdclxziXRHtXz/view?usp=share_link', 'img': 'null'},
                                        {'name':'poder', 'video':'https://drive.google.com/file/d/1mPFtW2_7KscqyCunxGH0t0S35z4sbv-O/view?usp=share_link', 'img': 'null'},
                                        {'name':'necesitar', 'video':'https://drive.google.com/file/d/1khmC3HBe2cDqYv1VROxII2Vsk5aPhB-n/view?usp=share_link', 'img': 'null'},
                                        {'name':'platicar', 'video':'https://drive.google.com/file/d/1aSyg8tRERW-NOAnwxS1xHJFCnVlpXogm/view?usp=share_link', 'img': 'null'},
                                        {'name':'perder', 'video':'https://drive.google.com/file/d/1V5meY2_ZeBrRCrMmLH953L7GYzKBFlaB/view?usp=share_link', 'img': 'null'},
                                        {'name':'pagar', 'video':'https://drive.google.com/file/d/1LbjI90O4N7l9uEVNvFJgwyUqB6VkzScq/view?usp=share_link', 'img': 'null'},
                                        {'name':'dormir', 'video':'https://drive.google.com/file/d/1mOXmIHVR7ggYg8CiQQ-M4daSb6F2qX0x/view?usp=share_link', 'img': 'null'},
                                        {'name':'esperar', 'video':'https://drive.google.com/file/d/1fWe5eihhYHD-HnrhTgSXTvhN0rm9Q_q3/view?usp=share_link', 'img': 'null'},
                                        {'name':'hablar', 'video':'https://drive.google.com/file/d/15DMpFHkD1wdTg_lP2U29ZtKHr3HLpx7Y/view?usp=share_link', 'img': 'null'},
                                        {'name':'explicar', 'video':'https://drive.google.com/file/d/1-yPXEYY8Pi3ly_XVFb8ND5ewC4l67ZKB/view?usp=share_link', 'img': 'null'},
                                        {'name':'entender', 'video':'https://drive.google.com/file/d/1narMLONGXHiNfl283_5OOZE5PlyQ_Li-/view?usp=share_link', 'img': 'null'},
                                        {'name':'ensenar', 'video':'https://drive.google.com/file/d/1kX5K-iWh1Z8NzagdA4tH456rmhVi2l5d/view?usp=share_link', 'img': 'null'},
                                        {'name':'escribir', 'video':'https://drive.google.com/file/d/1PV9DVum475bK86GVEKsPouoMUnDbD2Il/view?usp=share_link', 'img': 'null'},
                                        {'name':'empezar', 'video':'https://drive.google.com/file/d/1JhJYtrFj7L1jQoIBxWPAb8xBRQ40cWlh/view?usp=share_link', 'img': 'null'},
                                        {'name':'estudiar', 'video':'https://drive.google.com/file/d/1DAXVO261BxSNfGZQE4UcNHMTIo9DAskO/view?usp=share_link', 'img': 'null'},
                                        {'name':'descansar', 'video':'https://drive.google.com/file/d/1snVQMRrKa4j6yPTIvQK-IM7TZjgzNs7F/view?usp=share_link', 'img': 'null'},
                                        {'name':'decir', 'video':'https://drive.google.com/file/d/1AO-s5POxhvnd9O0FXipYsEHfJLPXHAem/view?usp=share_link', 'img': 'null'},
                                        {'name':'dar', 'video':'https://drive.google.com/file/d/14kkgbo5JvtDjR4ksGYm6SAGkJGmJdDtL/view?usp=share_link', 'img': 'null'},
                                        {'name':'comprar', 'video':'https://drive.google.com/file/d/1o_CK3zJDG4-TAvMpGCHlfXZV_STITe94/view?usp=share_link', 'img': 'null'},
                                        {'name':'cuidar', 'video':'https://drive.google.com/file/d/1j5WE8NHiagQw_jK0o2n5z2rE3MfT2OAS/view?usp=share_link', 'img': 'null'},
                                        {'name':'comer', 'video':'https://drive.google.com/file/d/1giPqNXADvifbRWuGun_jHRsTsw58tmk_/view?usp=share_link', 'img': 'null'},
                                        {'name':'avisar', 'video':'https://drive.google.com/file/d/1Wfe-JYnfS434eIzqGTy2Ngf04A5pJjBL/view?usp=share_link', 'img': 'null'},
                                        {'name':'creer', 'video':'https://drive.google.com/file/d/1QTmDIZFt3fm8A8238Fuu01UTIPCKA33b/view?usp=share_link', 'img': 'null'},
                                        {'name':'ayudar', 'video':'https://drive.google.com/file/d/1HT2_GvXEMYJM5Bee7UAx_Ftui671XOHB/view?usp=share_link', 'img': 'null'},
                                        {'name':'aprender', 'video':'https://drive.google.com/file/d/1ETwID4Y1KVu7t0AAoJcAMY-vLC1dSDjj/view?usp=share_link', 'img': 'null'}
                                        ]},
    {'name':'letras', 'level':1, 'words':[
                                          {'name':'A', 'video':'null', 'img': 'https://drive.google.com/file/d/1QKqGSkKy5a7CYT0hmX9u-kFHB7wP-5_M/view?usp=share_link'},
                                          {'name':'B', 'video':'null', 'img': 'https://drive.google.com/file/d/1dR3s-hLkT2X5vZ018gF5wIQfIrJR5jEV/view?usp=share_link'},
                                          {'name':'C', 'video':'null', 'img': 'https://drive.google.com/file/d/1YarH3jcDbTmcsokRw5ZZjGNU2CrXEpmz/view?usp=share_link'},
                                          {'name':'D', 'video':'null', 'img': 'https://drive.google.com/file/d/1QKqGSkKy5a7CYT0hmX9u-kFHB7wP-5_M/view?usp=share_link'},
                                          {'name':'E', 'video':'null', 'img': 'https://drive.google.com/file/d/1q0LzcnNB7YiEpd-aCL5lzUZJPcNmPKfA/view?usp=share_link'},
                                          {'name':'F', 'video':'null', 'img': 'https://drive.google.com/file/d/1Kb5NESMCR8NQMigR8M10r2lsCoPIDRFC/view?usp=share_link'},
                                          {'name':'G', 'video':'null', 'img': 'https://drive.google.com/file/d/1Kb5NESMCR8NQMigR8M10r2lsCoPIDRFC/view?usp=share_link'},
                                          {'name':'H', 'video':'null', 'img': 'https://drive.google.com/file/d/1kJHbFQuIq4-uEv7ZFvgIB5NTNbPcIPkB/view?usp=share_link'},
                                          {'name':'I', 'video':'null', 'img': 'https://drive.google.com/file/d/1kJHbFQuIq4-uEv7ZFvgIB5NTNbPcIPkB/view?usp=share_link'},
                                          {'name':'J', 'video':'https://drive.google.com/file/d/1CUfKsJ6gsPyJUxkSJHch0-CX_Y3AlZ2w/view?usp=share_link', 'img': 'null'},
                                          {'name':'L', 'video':'null', 'img': 'https://drive.google.com/file/d/1t6WZb35qND4_bVG8e69wo0UFBjK1GFKP/view?usp=share_link'},
                                          {'name':'LL', 'video':'https://drive.google.com/file/d/1n486o9HvJbfCDlbpDPvTfz5VocHopLwy/view?usp=share_link', 'img': 'null'},
                                          {'name':'M', 'video':'null', 'img': 'https://drive.google.com/file/d/13XYgt5aH-d0f-4SAniF6RNnIK5sTRxy6/view?usp=share_link'},
                                          {'name':'N', 'video':'null', 'img': 'https://drive.google.com/file/d/1LW-Z5_Zu9ndoSewTC_GdSrqbyzTkWcWh/view?usp=share_link'},
                                          {'name':'Ñ', 'video':'https://drive.google.com/file/d/19imxu_cFgZgK5WNuaAj3SAVWE5iAB_AI/view?usp=share_link', 'img': 'null'},
                                          {'name':'O', 'video':'null', 'img': 'https://drive.google.com/file/d/19imxu_cFgZgK5WNuaAj3SAVWE5iAB_AI/view?usp=share_link'},
                                          {'name':'P', 'video':'null', 'img': 'https://drive.google.com/file/d/19imxu_cFgZgK5WNuaAj3SAVWE5iAB_AI/view?usp=share_link'},
                                          {'name':'Q', 'video':'https://drive.google.com/file/d/1A3k25-Hf5gmRsYCjkD60Yw4ftDT8VNRD/view?usp=share_link', 'img': 'null'},
                                          {'name':'R', 'video':'null', 'img': 'https://drive.google.com/file/d/1nZpQK8pvLMqtDQpbHrcp2Glb9IX2aIgV/view?usp=share_link'},
                                          {'name':'RR', 'video':'https://drive.google.com/file/d/1wxFwOHp4fjUXepz16zVrwlAmVN4hFKFd/view?usp=share_link', 'img': 'null'},
                                          {'name':'S', 'video':'null', 'img': 'https://drive.google.com/file/d/1PgAqrE6n1oxsYpaUlgFUqSYNj2A47Zgz/view?usp=share_link'},
                                          {'name':'T', 'video':'null', 'img': 'hhttps://drive.google.com/file/d/18DIh-xbUHitO9dPH5DCzim7Hoe8fRKsF/view?usp=share_link'},
                                          {'name':'U', 'video':'null', 'img': 'https://drive.google.com/file/d/1QZfGLg0PUTDATc21CiAeQglwhoFgAOub/view?usp=share_link'},
                                          {'name':'V', 'video':'null', 'img': 'https://drive.google.com/file/d/1oOShSo09J44A7ffK8grorZM4WbURwtzm/view?usp=share_link'},
                                          {'name':'W', 'video':'null', 'img': 'https://drive.google.com/file/d/17BA0BQlvoBuCctby1cgxsO9ajdGrgDRP/view?usp=share_link'},
                                          {'name':'X', 'video':'https://drive.google.com/file/d/1MsKU9mY01oERDzK8SQTCXcRQHhT9pIIT/view?usp=share_link', 'img': 'null'},
                                          {'name':'Y', 'video':'null', 'img': 'https://drive.google.com/file/d/1SuTELApPhQK8hEigmW8tBDLHJYncEhu8/view?usp=share_link'},
                                          {'name':'Z', 'video':'https://drive.google.com/file/d/1rkcHFzQYc--YQZNVLr9SPxvmhWKtrZgq/view?usp=share_link', 'img': 'null'}
                                          ]}                      
])


'''