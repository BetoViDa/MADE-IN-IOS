# API Para la aplicación signa de lenguaje de señas
'''
pasos:
    python3 -m venv venv                         creamos entorno virtual llamado "venv"
    venv\Scripts\activate    en MacOS ejecutar:  source venv/bin/activate
    pip install <lo que se deba instalar>       para linux y macos usar "pip3"
    python3 src/api.py                           corremos la api estando en la carpeta API
'''
# <lo que se debe instalar>
# pip install flask          Componente basico
# pip install pymongo
# pip install flask-pymongo
# pip install flask-cors
# pip install python-dotenv  Para el archivo .env
# pip install pyopenssl      Para https

from dotenv import load_dotenv  # esto para las variables de entorno .env
import os
from flask import Flask, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import hashlib  # para hashear la password con sha256
from flask_cors import CORS
import logging # esta libreria se usa para controlar los logs en un fichero
import random

app = Flask(__name__)  # inicializamos la app
CORS(app)  # se ocupa por ahora

load_dotenv()  # cargamos las variables de entorno


DBpassword = os.getenv("PASSWORD_MONDOGO")
DBuser = os.getenv("USER_MONDOGO")
DataBase = os.getenv("DATABASE_MONDOGO")
Cluster = os.getenv("CLUSTER_MONDOGO")

# =====Conexión a la base de datos=======
app.config['MONGO_URI'] = 'mongodb+srv://'+DBuser+':' + \
                           DBpassword+'@cluster0.'+Cluster+'.mongodb.net/'+DataBase
mongo = PyMongo(app)  # mongo es nuestra base de datos (mongo.db)
# =======================================

#==========Configuración de los logs================
LOG_FILENAME = './tmp/logs.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

#===================================================

@app.route('/ok', methods = ['GET'])
def Server():
   app.logger.debug('Arranque de la aplicacion')
   return {"msj": "hello world"}


# ------------------------------SIGN UP USER----------------------------------
# falta cifrar datos sensibles como password y correo
@app.route('/user/signup', methods=['POST'])
def create_user():
   '''
   {
   "username":"Leopoldo",
   "password": "123",
   "email": "Leopoldo@mail.com"
   }
   '''
   # {"username":nombre,"password":pass,"email":mail,"type":0,}
   json = request.json
   username  =  json["username"]    
   email     =  json["email"].lower() 
   password  =  hashlib.sha256(json["password"].encode()).hexdigest()    # password hasheado
   print(username)
   # si encuentra un usuario con ese username manda error
   if mongo.db.users.find_one({'username': username}) != None:
      return {'msj': 'ya existe este username', 'ERROR': 'si'}
   # si encuentro un usuario con este email mando error
   if mongo.db.users.find_one({'email': email}) != None:
      return {'msj': 'ya esta en uso este correo', 'ERROR': 'si'}
   
   if json['username'] and json['password'] and json['email'] and (json['username'] != "") and (json['password'] != "") and (json['email'] != ""):
      json['email'] = email # ponemos el mail encriptado
      json['username'] = username # ponemos el username encriptado
      json['password'] = password # ponemos la password hasheado
      json["grades"] = {
         "verboscomunes1":   0,
         "verboscomunes2":   0,
         "verboscomunes3":   0,
         "verboscomunes4":   0,
         "letras1":          0,
         "letras2":          0,
         "letras3":          0,
         "verbosnarrativos1": 0,
         "verbosnarrativos2": 0,
         "preposiciones1":   0,
         "preposiciones2":   0,
         "preposiciones3":   0,
         "preposiciones4":   0,
         "preposiciones5":   0,
         "preposiciones6":   0,
         "preposiciones7":   0,
         "preposiciones8":   0,
         "preposiciones9":   0,
         "preposiciones10":  0,
         "preposiciones11":  0
      }
      json["level"] = 0
      json["type"] = 0  # es usuario normal
      json['group'] = ''
      id = mongo.db.users.insert_one(json)
      json['_id'] = str(id.inserted_id)
      return {'msj': 'usuario guardado', 'ERROR': 'no'}  # mensaje de exito
   else:
      return {'msj': 'falta un campo', 'ERROR': 'si'}  # mensaje de error
# ====================================================================================================

# -----------------------------LOGIN---------------------------------------
# falta cifrado de la contraseña para comparar contraseña cifrada con no cifrada


@app.route('/user/login', methods=['POST'])
def login():
   
   # recibe usuario/correo y contraseña en un json asi
   # {"username":usuario/correo,, "password": contraseña}
   json = request.json
   # reviso si el usuario puso su username o su correo
   password = hashlib.sha256(json["password"].encode()).hexdigest()
   if "@" in json['username']:  # es un correo
      email = json["username"].lower()

      data = mongo.db.users.find_one({'email': email, 'password': password}, {
                                      '_id': 1, 'username': 1, 'email': 1, 'group': 1, 'type': 1, 'level':1})
   else:
      username = json["username"]
      data = mongo.db.users.find_one({'username': username, 'password': password}, {
                                      '_id': 1, 'username': 1, 'email': 1, 'group': 1, 'type': 1, 'level':1})
   
   if data == None:
      if "@" in json['username']:
         return {'ERROR': "correo o contraseña incorrecta"}
      else:
         return {'ERROR': "nombre de usuario o contraseña incorrecta"}
   else:
      r = {
         '_id': str(data['_id']),
         'username':data['username'],
         'email': data['email'],
         'type': data['type'],  # 1 admin,   0 normal
         'group': data['group'],
         'lvl': data['level']
      }
      return r
   # regresa el siguiente json {"_id":string, "username": string, "email": string, "type": bool}
   # si el usuario tiene grupo regresa
   #{"_id":string, "username": string, "email": string, "type": bool, "group":string}
# =========================================================================

# -------------------------------Users group---------------------------------

@app.route('/user/users/<group>', methods=['GET'])
def usersGroup(group):
   users = mongo.db.users.find({'group': group, 'type': 0}, {'username': 1, '_id':1, 'level':1})
   data = []

   for user in users:
      data.append({"username":user['username'], "_id":str(user["_id"]), "lvl": user["level"]})
   return {"usersL": data}

#============================================================================

# -------------------------------Join Group---------------------------------


@app.route('/user/joinGroup', methods=['POST'])
def joinGroup():
   # {_id:"636c330384831804d80d0283, groupCode: "vVlkLalskcjhlk12csda81"}
   json = request.json
   grupo = mongo.db.groups.find_one({'code': json['groupCode']})
   if grupo == None:
      return {"msj": "ERROR Codigo invalido", "group":"None"}
   id = json['_id']
   objId = ObjectId(id)
   user = mongo.db.users.find_one({"_id": objId}, {"group": 1})
   if user["group"] != "":  # si ya estas en un grupo no te dejara unirte a otro
      return {"msj": "ERROR ya estas en un grupo", "group":"None"}
   # si no estas en un grupo, te mete a el
   mongo.db.users.update_one(
      {"_id": objId},
      {"$set": {"group": grupo["name"]}},
      upsert=False)
   return {"msj": "te uniste al grupo", "group":grupo["name"]}
# =========================================================================

# ----------------------------leave group----------------------------------


@app.route('/user/leaveGroup', methods=['POST'])
def leaveGroup():
   # {"_id":636c330384831804d80d0283}
   id = request.json["_id"]
   objInstance = ObjectId(id)
   mongo.db.users.update_one(
      {"_id": objInstance},
      {"$unset": {"group": 1}}
   )
   return {"msj": "te saliste del grupo"}
# =========================================================================

# --------------------Mostrar grades para niveles-----------------------
@app.route('/user/grades/<_id>', methods=['GET'])
def checkGrades(_id):
   #{username:leo, _id: 12312412414}

   objInstance = ObjectId(_id)
   data = mongo.db.users.find_one({'_id': objInstance}, {'grades': 1})
   r = []
   for key in data["grades"]:
      r.append({"name":key, "grade":data["grades"][key]})
      

   return {"grades": r}
# ========================================================================

# --------------------------Actualizar calificacion----------------------
@app.route('/user/setGrade', methods=['POST'])
def setGrade():
   # {_id:13325fdsf, categorie:letras1, grade:90}
   json = request.json
   id = json["_id"]
   objId = ObjectId(id)
   # para revizar si la nueva calificación es mayor o menor
   calActual = mongo.db.users.find_one(
      {"_id": objId}, {f'grades.{json["categorie"]}': 1, '_id': 0, 'level':1})
   if calActual["grades"][json["categorie"]] < json["grade"]:
      if (calActual["grades"][json["categorie"]] < 70) and (json["grade"] >= 70):
         mongo.db.users.update_one({"_id": objId},
                              {"$set":
                                    {f'grades.{json["categorie"]}': json["grade"], 'level':calActual['level']+1}
                              })
         return {"msj": "Subes de nivel"}
      else:
         mongo.db.users.update_one({"_id": objId},
                                 {"$set":
                                    {f'grades.{json["categorie"]}': json["grade"]}
                                 })
      return {"msj": f'Calificación de {json["categorie"]} actualizada a {json["grade"]:.2f}'}
   return {"msj": f'La calificación de {json["categorie"]} se mantuvo con {calActual["grades"][json["categorie"]]:.2f}'}

# =======================================================================

# ----------------------Numero de niveles arriba de 70-------------------
# =======================================================================


# =========================================================================
# ===================          CATEGORIES          ========================
# =========================================================================
# =========================================================================
# ----------------mostrar todas las palabras--------------
@app.route('/categories/all/<categorie>', methods=['GET'])
def showCategories(categorie):
   # muestra todas las palabras de una categoria completa, ignorando el numero del nivel de categoria
   # por ejemplo, /categories/all/verboscomunes regresa todas las palabras de verboscomunes 1, 2 ,3 y 4
   datas = mongo.db.categories.find(
      {"name": {'$regex': f'^{categorie}'}}, {"words": 1})
   r = []
   for data in datas:
      for word in data["words"]:
         print(word["name"])
         r.append(word["name"])
   r.sort()
   return {"palabra": r}
# ========================================================================

# -----------------mostrar video de una palabra--------------------------
@app.route('/categories/file/<categorie>/<SearchWord>', methods=['GET'])
def getFile(categorie, SearchWord):
   # http://127.0.0.1:5000//categories/file/verboscomunes/explicar
   # regresa
   # https://drive.google.com/file/d/1-yPXEYY8Pi3ly_XVFb8ND5ewC4l67ZKB/view?usp=share_link
   datas = mongo.db.categories.find(
      {"name": {'$regex': f'^{categorie}'}}, {"words": 1})
   r = []
   for data in datas:
      for word in data["words"]:
         if word["name"] == SearchWord:
            return {"file": word["file"], "fileType": word["fileType"]}
   return r
# =======================================================================

# ----------------mostrar palabras de una categoria-----------------------


@app.route('/categories/words/<categorie>', methods=['GET'])
def getWords(categorie):
   datas = mongo.db.categories.find_one({"name": categorie})["words"]
   return datas
# ========================================================================

# ---------------------Crear un quiz-------------------------------------


@app.route('/quiz/<categorie>', methods=['GET'])
def createQuiz(categorie):
   words = getWords(categorie)
   quiz = []
   for x in range(len(words)):
      pregutna = {}
      pregutna["file"] = words[x]["file"]
      pregutna["answer"] = words[x]["name"]
      # True = imagen         false =
      pregutna["fileType"] = words[x]["fileType"]
      pregutna["options"] = []
      # metemos de forma random 3 respuestas incorrectas
      posiblesOpciones = words.copy()  # copias las palabras
      # eliminas la palabra que ya esta en la lista de opciones
      posiblesOpciones.pop(x)
      for _ in range(3):
         r = random.choice(posiblesOpciones)
         pregutna["options"].append(r["name"])
         posiblesOpciones.remove(r)
      random.shuffle(pregutna["options"])  # revolvemos las respuestas
      quiz.append(pregutna)
   random.shuffle(quiz)
   response = {'results': quiz}
   return response
# ======================================================================


# =========================================================================
# ===================       GROUP  y calificaciones     ===================
# =========================================================================
# =========================================================================

# ------quiz con % de personas en el grupo que han terminado el nivel------
# ejemplo /group/John%20Deere
@app.route('/group/<group>', methods=['GET'])
def getPorQuiz(group):
   count = 0
   r = {}
   for i in mongo.db.users.find({'group': group, 'type':0}, {'grades': 1}):
      count += 1
      for j in i['grades']:
         if i['grades'][j] > 70:  # si aprobo
            # aumentamos el numero de personas en el dic, el get nos setea en 0 si no existe en el dic
            r[j] = (((r.get(j, 0)/100)*(count-1) + 1)/count)*100
         else:
            r[j] = (((r.get(j, 0)/100)*(count-1))/count)*100
   # lo ponemos en un areglo de jsons
   result = []
   for i in r:  # i guarda la key del dic
      result.append({"name": i, "grade": r[i]})
   return {"grades": result}


@app.route('/UserGrade/<username>', methods=['GET'])
def getUserId(username):
   data = mongo.db.users.fin({'username': username},  {'grades': 1, '_id': 0})
   return data


if __name__ == "__main__":
   #app.run(debug=True)
   #app.run(host='0.0.0.0',debug=True,port='5003')
   app.run(ssl_context = "adhoc" ,debug=True, port='443') # ssl para https


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


--------------------------------------------------------------------------------------

use('signaDB')

db.categories.insertMany([
   {
      "name":"verboscomunes1",
      "words":[
         {
            "name":"trabajar",
            "file":"1tcYRwR7-TW_HrKbFzVu_tv_T60dmXmQ1",
            "fileType": false
         },
         {
            "name":"vender",
            "file":"1pzJg9C-4O-ull87o9oSxu3-wGnt3m5h8",
            "fileType": false
         },
         {
            "name":"terminar",
            "file":"1PrrUckCLrEn-Xy6eWjLOx4ZVKX8Neq8t",
            "fileType": false
         },
         {
            "name":"sentar",
            "file":"1Qo9iUabjwh1hUNSK8D2Il6AZNyy9XYgJ",
            "fileType": false
         },
         {
            "name":"ver",
            "file":"1W1xcSIVeu05NqCAFw1ky9tgZ3wfMeP5K",
            "fileType": false
         },
         {
            "name":"preguntar",
            "file":"1QPw0tfGXe3Oa-dpe73Cebho-rPn77SNd",
            "fileType": false
         },
         {
            "name":"vivir",
            "file":"1j5pO3MfbnzRDZ4XmnarwMcXiXwxwNZX5",
            "fileType": false
         },
         {
            "name":"olvidar",
            "file":"1kk2ypAhkvl5mErzZeHdEJBypu2kMQg3S",
            "fileType": false
         },
         {
            "name":"pensar",
            "file":"15GFkp2n3DJE8L3_9oZBx9Huoz5_6qttv",
            "fileType": false
         }
      ]
   },
   {
      "name":"verboscomunes2",
      "words":[
         {
            "name":"limpiar",
            "file":"1YSGyx3CWjXQAnjhyYyZlleywIxzJoiDl",
            "fileType": false
         },
         {
            "name":"jugar",
            "file":"19nwpa77zl9bL8VOtV4DXDPDJh0hmjVBU",
            "fileType": false
         },
         {
            "name":"hacer",
            "file":"13B0_4vpidDQXB2PW-TX6CUc_p6pTwjIa",
            "fileType": false
         },
         {
            "name":"poder",
            "file":"1iv-MH9RIMzcU1pbzvc4uGcgcUS66k5bt",
            "fileType": false
         },
         {
            "name":"necesitar",
            "file":"1D7HPaXTYNW7jimQUhH6byXsvpGpxULGc",
            "fileType": false
         },
         {
            "name":"platicar",
            "file":"1z3cmZSxI2z07jmKyPX4pGiQfWzPotrOR",
            "fileType": false
         },
         {
            "name":"perder",
            "file":"1FdQTvtpCHPUvkVj4_q0fn6H_lCbdkq70",
            "fileType": false
         },
         {
            "name":"pagar",
            "file":"1RZOCJZHvEeOcIjz0MFsASwqre2q3ZlD2",
            "fileType": false
         },
         {
            "name":"dormir",
            "file":"1yZ06HrUs8iLkLZLaNBDy3VuZTQzrm8a7",
            "fileType": false
         }
      ]
   },
   {
      "name":"verboscomunes3",
      "words":[
         {
            "name":"esperar",
            "file":"1q_wsu6uDzM_sJKebcX2D8Ta4SFnqWk3f",
            "fileType": false
         },
         {
            "name":"hablar",
            "file":"1Vm3LY7f52ooXjja4Vod1mDBR5KkWC5wz",
            "fileType": false
         },
         {
            "name":"explicar",
            "file":"14yh2agoxOcE8MD8M7KvYsGZwIEULkWTG",
            "fileType": false
         },
         {
            "name":"entender",
            "file":"1j3AYx1SL3bGqbDNquBNb1LQ8S7dAa6Ea",
            "fileType": false
         },
         {
            "name":"ensenar",
            "file":"10VA78GejwYiMG99TswuunILQhxJmR25R",
            "fileType": false
         },
         {
            "name":"escribir",
            "file":"1-ov52ractWhgN6D0S8uginy9mGZ1egpu",
            "fileType": false
         },
         {
            "name":"empezar",
            "file":"1mtDSBRcPSpmwNgGEQIIu5_dVYNqVBQYD",
            "fileType": false
         },
         {
            "name":"estudiar",
            "file":"1q_wsu6uDzM_sJKebcX2D8Ta4SFnqWk3f",
            "fileType": false
         },
         {
            "name":"descansar",
            "file":"1GcJJP7RIleNriyKec1V4KYHZA2_7cY_a",
            "fileType": false
         }
      ]
   },
   {
      "name":"verboscomunes4",
      "words":[
         {
            "name":"decir",
            "file":"1MiDELxOQOGYs6Bfi4FoijIsKRMUGNpaZ",
            "fileType": false
         },
         {
            "name":"dar",
            "file":"18XB7dIXL3eOl-tYm6kEagDk9EpZWXg7N",
            "fileType": false
         },
         {
            "name":"comprar",
            "file":"1mKCyZRI71RjcKQb3FyN_diqNcF8HVXcW",
            "fileType": false
         },
         {
            "name":"cuidar",
            "file":"1Ot2pd2e65_KYdLyTbZgJH1w9t3PbAwwe",
            "fileType": false
         },
         {
            "name":"comer",
            "file":"1OwlYlcBEPJ4nnlo-r5G6DMggfiNAuLcy",
            "fileType": false
         },
         {
            "name":"avisar",
            "file":"1kgcTxgwjwUliTPfoTyNr42hadCs6kbSx",
            "fileType": false
         },
         {
            "name":"creer",
            "file":"1IaGKc8zge1PsyydVghcggG8mWOQ0ayGo",
            "fileType": false
         },
         {
            "name":"ayudar",
            "file":"1Qu7wO5AngbRddeLyzjp8TqXGh7D13zuY",
            "fileType": false
         },
         {
            "name":"aprender",
            "file":"11x8aTxZq647D0DYSYYS4iDitgVHqJDwU",
            "fileType": false
         }
      ]
   },
   {
      "name":"letras1",
      "words":[
         {
            "name":"A",
            "file":"1ou7Kmy4Xg_fSDc44uDkB_4tblsmK_Ub1",
            "fileType": true
         },
         {
            "name":"B",
            "file":"1tKCjpIGoDdDzCHdz7W8Z4Bz_t0_tIVlZ",
            "fileType": true
         },
         {
            "name":"C",
            "file":"1HONPypOgXdLkiXQW4HjWI9mLarWqqxJ4",
            "fileType": true
         },
         {
            "name":"D",
            "file":"1X6f8tsfA4UfrlIkHwExdu6JHRVL85mxe",
            "fileType": true
         },
         {
            "name":"E",
            "file":"1oLwjPOsZ2hxWG4mXJVTzAryllG6oYX30",
            "fileType": true
         },
         {
            "name":"F",
            "file":"1ZccFRQR-l2E5pbW374NQfoRUJd0povep",
            "fileType": true
         },
         {
            "name":"G",
            "file":"1Rwf-GvvTY-TvZqGFzagPTgNCxldVtWRd",
            "fileType": true
         },
         {
            "name":"H",
            "file":"1N-sKQpwHFA8WN9y1v_4iHajqPxMSFFe8",
            "fileType": true
         },
         {
            "name":"I",
            "file":"1sZaMPpD3jpX7PHwW449oLnyA2LZQf1Or",
            "fileType": true
         },
         {
            "name":"J",
            "file":"1xsrLa2o_oFXERWY7KAH0_uo_TSPVf9qG",
            "fileType": false
         }
      ]
   },
   {
      "name":"letras2",
      "words":[
         {
            "name":"K",
            "file":"1DYQ72t5Xyr0tDx14r0GPScizYLTETDSv",
            "fileType": false
         },
         {
            "name":"L",
            "file":"1o1736id19a3rdLy0mLOKHstK26Q2I_3X",
            "fileType": true
         },
         {
            "name":"LL",
            "file":"1Nho5O9oVKdHuHsaJ2uuqaLMqfASW0Chz",
            "fileType": false
         },
         {
            "name":"M",
            "file":"1QqhZNjoBCqzTNkgOkuz3aVJbr4-I-COd",
            "fileType": true
         },
         {
            "name":"N",
            "file":"1L6kg8WFcbn7dIoQFKgA4U0I685emy2SA",
            "fileType": true
         },
         {
            "name":"Ñ",
            "file":"1Y9cY6rIpHFMzZvcD4SJ4ORhYrC8TqR23",
            "fileType": false
         },
         {
            "name":"O",
            "file":"1vMdT51TJyWHHv1qMgkZ9CiYrG1jPy6j0",
            "fileType": true
         },
         {
            "name":"P",
            "file":"1Z7Pp4rRPgIxAArqXcddVpLZZCIGPQUrg",
            "fileType": true
         },
         {
            "name":"Q",
            "file":"1f-T3A0ZDhCrhqCXjn6X7ATkEh7EvdSHU",
            "fileType": false
         },
         {
            "name":"R",
            "file":"19WweoR_JXM688W_VuHH_9kCJaQ_iuwWk",
            "fileType": true
         }
      ]
   },
   {
      "name":"letras3",
      "words":[
         {
            "name":"RR",
            "file":"1DkEGIpWEvDMlssFZ04-gcOkJY35ah0am",
            "fileType": false
         },
         {
            "name":"S",
            "file":"1fg9tziGGnzbIikIbU3M9GpYdtI-OList",
            "fileType": true
         },
         {
            "name":"T",
            "file":"1t1pz20RzMZHr9xhNYUH6BQ79I6PWiqHf",
            "fileType": true
         },
         {
            "name":"U",
            "file":"1B1iRhbzH1U0p0IoR_SgMIAU3KgglEBlr",
            "fileType": true
         },
         {
            "name":"V",
            "file":"1RLs2rbES0kcMCFgCm-t686yu8p8DrGFf",
            "fileType": true
         },
         {
            "name":"W",
            "file":"1RPBmIN3_U6RZLhw1TA9EBIORrtGQuOij",
            "fileType": true
         },
         {
            "name":"X",
            "file":"1ASyHj06QMOGVeX29WTrZRm_4MQ1fRpaz",
            "fileType": false
         },
         {
            "name":"Y",
            "file":"1CiBzqgtUH66aYgkcQRmW0AFE6rDMOmoe",
            "fileType": true
         },
         {
            "name":"Z",
            "file":"1m9js4flqszhOhN2mAa00brTJAkyPQVn7",
            "fileType": false
         }
      ]
   },
   {
      "name":"verbosnarrativos1",
      "words":[
         {
            "name":"servir",
            "file":"1_hZfXyIyPhwRnyXiCo-Qk49tUIo5-QPh",
            "fileType": false
         },
         {
            "name":"saber",
            "file":"1I4Frcn6HmLTBF66yk_Y88Lnkm0hdnAV0",
            "fileType": false
         },
         {
            "name":"querer",
            "file":"1C17G43iKIaxDSDupoDQiTEH2ItbsLahX",
            "fileType": false
         },
         {
            "name":"poder",
            "file":"1Ck9REvG-LS950k_3N3sapRyb-pL7pVUR",
            "fileType": false
         },
         {
            "name":"no servir",
            "file":"1apg9CLioaqoeEgJJtPW1SvwSmG5JqO-Z",
            "fileType": false
         },
         {
            "name":"no saber",
            "file":"1afxu-VnH3I3rqisa-wi8CnbhFXqeURrG",
            "fileType": false
         },
         {
            "name":"no querer",
            "file":"1e9rb71OIAWOhJTFcXoIH5sANeu0af3iO",
            "fileType": false
         },
         {
            "name":"no poder",
            "file":"17jiSlroCa5q9_0cq3eF-ZCRKgG8CWXq-",
            "fileType": false
         }
      ]
   },
   {
      "name":"verbosnarrativos2",
      "words":[
         {
            "name":"no haber",
            "file":"1GyHPxm-V-S_S0MRJaNFoJk0U3xS5kR1e",
            "fileType": false
         },
         {
            "name":"no gustar",
            "file":"103cjwdawHurtShohvLhEg-ChT8M_bS5g",
            "fileType": false
         },
         {
            "name":"no entender",
            "file":"1lVljz8BhGWqMfbQpaRTiDg_lK73vRANv",
            "fileType": false
         },
         {
            "name":"no conocer",
            "file":"1nLseLOJjV9bIo-3OXNWsiF0spImamdTQ",
            "fileType": false
         },
         {
            "name":"haber",
            "file":"1FARSdS7lP_tdsFrfJAwS7P2BVtPZ7M-H",
            "fileType": false
         },
         {
            "name":"gustar",
            "file":"1ViagIzPoiRPiT-T3Lb5kGf7UIff9q4to",
            "fileType": false
         },
         {
            "name":"entender",
            "file":"1j3AYx1SL3bGqbDNquBNb1LQ8S7dAa6Ea",
            "fileType": false
         },
         {
            "name":"conocer",
            "file":"1ON7LpFIox8Wgw8LdZCoIAxcv_Zbxq-9i",
            "fileType": false
         }
      ]
   },
   {
      "name":"preposiciones1",
      "words":[
         {
            "name":"abajo",
            "file":"18lafYZSxJa75PLBA8EOMJkYCRXJdeH2W",
            "fileType": false
         },
         {
            "name":"aburrido",
            "file":"1WthGauiCsrMYnGqxU0U_a76fTm38N7cr",
            "fileType": false
         },
         {
            "name":"accidente",
            "file":"1A5iqD-_Ye8OfHB8ShdW25l6xjxi_uN3v",
            "fileType": false
         },
         {
            "name":"adentro",
            "file":"1HSL8cMBg6i0MYvwsM7xGCAGWSVNUjFnF",
            "fileType": false
         },
         {
            "name":"afortunado",
            "file":"1EZMASe09g9KYkJLd9ORHP-t0v4RHnI2_",
            "fileType": false
         },
         {
            "name":"alegre divertido",
            "file":"1bxHG4-qMxmfaUtRdWWfiDuQ8P4pzvobN",
            "fileType": false
         },
         {
            "name":"algunos",
            "file":"1H-PlVeB5RktuJrN0BF3pTHcSnpDKdDv9",
            "fileType": false
         },
         {
            "name":"alto estatura",
            "file":"1WuIyds3NyPC3s0QSi__N6NKJUJJ-3a1B",
            "fileType": false
         },
         {
            "name":"amable",
            "file":"1kUlTtfLcOHk21kEbv_OmCmkRzotaOv-u",
            "fileType": false
         }
      ]
   },
   {
      "name":"preposiciones2",
      "words":[
         {
            "name":"antes",
            "file":"1AT5YwJtEG0gCXtj49yIPEMLQVH30MJ9b",
            "fileType": false
         },
         {
            "name":"arriba",
            "file":"1xcMQfxKXmkQxqjCNvchthQxLwEXBxYTl",
            "fileType": false
         },
         {
            "name":"asustado",
            "file":"17ccpxzNtbft19JA1n2Eci9vbPocZhvTV",
            "fileType": false
         },
         {
            "name":"atencion atento",
            "file":"1zrFW_P0zmhUYAP1HtED3ESjDhcLsLkug",
            "fileType": false
         },
         {
            "name":"baboso",
            "file":"1ZfK_8JueCp3IqshlGngodwIImxn8S6Ci",
            "fileType": false
         },
         {
            "name":"bonito",
            "file":"17rsyZMkRWKaA7txv-u8j3ylPw5OmH20i",
            "fileType": false
         },
         {
            "name":"broma",
            "file":"1FiamrKkXhL_V9ISAODiTPok9RwiSGdVz",
            "fileType": false
         },
         {
            "name":"bueno",
            "file":"16STInDRuLaDiElOsJ6W_p4mkCv_MHgpt",
            "fileType": false
         },
         {
            "name":"cada",
            "file":"1_jHteCbQLMxdPbyDk_xM4qExL9g5U5RP",
            "fileType": false
         }
      ]
   },
   {
      "name":"preposiciones3",
      "words":[
         {
            "name":"caliente",
            "file":"1xd8-mGp-ikEOQvFzO_E6O_TC3nf5lQrq",
            "fileType": false
         },
         {
            "name":"cansado",
            "file":"1d_t6pADthXPYyVnrsOuvfaPVByX0xGnI",
            "fileType": false
         },
         {
            "name":"carino",
            "file":"1dsBV34CIQG0fnL7OUaHnNNRlt5HkKnN0",
            "fileType": false
         },
         {
            "name":"celoso",
            "file":"1igPEHfUlFHuzJj6Y2Z2il_ubGpeRUhIo",
            "fileType": false
         },
         {
            "name":"chaparro",
            "file":"17F_tzdln6lqmyuOEBAMCUMhdEEhnlx8a",
            "fileType": false
         },
         {
            "name":"chistoso",
            "file":"1cq5rhwtNWR2ljC9GiiceczxUL0b8tauF",
            "fileType": false
         },
         {
            "name":"cobarde",
            "file":"1D61Q_YM206AMiovoY3iJBAlNBfSus9Bp",
            "fileType": false
         },
         {
            "name":"contento",
            "file":"1V6VOXvlClPWJaHKa1fXtwfMLCF2xOw2Z",
            "fileType": false
         },
         {
            "name":"curioso",
            "file":"1fgvcsQozxzHvsjoG0odkDJB_oEoIK5Ax",
            "fileType": false
         }
      ]
   },
   {
      "name":"preposiciones4",
      "words":[
         {
            "name":"debil",
            "file":"1gtzLCxMobSIim5L8VlxNEklSCPe4tSUm",
            "fileType": false
         },
         {
            "name":"decente",
            "file":"1iBLnBfG3jwYxBbdePkvecxlUOqKirYUh",
            "fileType": false
         },
         {
            "name":"delgado",
            "file":"179QcN83CgFTIDOW3plWGXvb5UGbJ4sD4",
            "fileType": false
         },
         {
            "name":"despacio",
            "file":"1HDiNOnP_fKzuWddBXiJLafJQfva_BVFl",
            "fileType": false
         },
         {
            "name":"diferente",
            "file":"1fwjznopswbFUHAnWYzIZXIE1TPIPPWkp",
            "fileType": false
         },
         {
            "name":"dificil",
            "file":"1q5GQFiJdwIb2z7V8BZjVjOunlb-_53nF",
            "fileType": false
         },
         {
            "name":"diploma",
            "file":"1vKCY_Rowa1YwDpA40PHPPScc2Ov0PSCi",
            "fileType": false
         },
         {
            "name":"duda",
            "file":"18r56BDPlnkQM1NIkRLJnCefhuOOXS8xd",
            "fileType": false
         },
         {
            "name":"egoista",
            "file":"17iSK6tG05pQgUD8pbhyFDo4C4jrpoDBz",
            "fileType": false
         }
      ]
   },
   {
      "name":"preposiciones5",
      "words":[
         {
            "name":"ejemplo",
            "file":"1l53JpwChIaZFDGUMLLnX9L4D36AaVVS8",
            "fileType": false
         },
         {
            "name":"ejercicio",
            "file":"1GS3oRr1egeGDaxaZHgpRBAfTuv-XNq3a",
            "fileType": false
         },
         {
            "name":"enojado",
            "file":"1W-XAqB9Y7_5YAL4uUwe4-1yH-hLNhFuh",
            "fileType": false
         },
         {
            "name":"envidia",
            "file":"1J7tvRv1feAbB6bQCx8XG0l2EbHT-4Xbz",
            "fileType": false
         },
         {
            "name":"especial",
            "file":"1Ye9lRSy1BG2hWGT299u9z-l7tKXhCwRt",
            "fileType": false
         },
         {
            "name":"facil",
            "file":"1Vn7cf-sSbxTvQ6EMEXbJOKsX5ahZzTrS",
            "fileType": false
         },
         {
            "name":"falso",
            "file":"1k8YXhkBZ4JMUbJkplFwLw2e-Wjo9Dl1n",
            "fileType": false
         },
         {
            "name":"feliz",
            "file":"1qdioiY_YhDxSedckUXcTJLiflq54nRw3",
            "fileType": false
         },
         {
            "name":"feo",
            "file":"1QvLD7bbYOV_0wIe5mEcgj5Fer0Jj2quO",
            "fileType": false
         }
      ]
   },
   {
      "name":"preposiciones6",
      "words":[
         {
            "name":"flojo",
            "file":"1isBRMaq4R9RPPDGM4lV22QSKStwzs01S",
            "fileType": false
         },
         {
            "name":"fuerte",
            "file":"1JFXe_iKqzOV0ZgJiVoJlFvVjfvFSKZ0m",
            "fileType": false
         },
         {
            "name":"fuerza",
            "file":"1SgvShY5VF82Ugtf99a4SdDLhofB6bipf",
            "fileType": false
         },
         {
            "name":"gordo",
            "file":"1TD2dXutm5tVCxBF1YTihjDgIkdrPxTOA",
            "fileType": false
         },
         {
            "name":"gratis",
            "file":"1ZOiFVyhP4gC2qcZxZ_4NHLwGrDC9jW4s",
            "fileType": false
         },
         {
            "name":"grosero",
            "file":"1pBqbgEwe9cG_zehQcgdc9xw7VGMR2B2N",
            "fileType": false
         },
         {
            "name":"guapo",
            "file":"1hEAZJYogNuX3vV60ZlMlAB5vT_culQEZ",
            "fileType": false
         },
         {
            "name":"hambre",
            "file":"1v2uO3z3aUAdgkd2i5WZ76pHxustLA027",
            "fileType": false
         },
         {
            "name":"historia",
            "file":"1VHEjZgbY8Vy51zxdxTkPh23pLaXBZ39p",
            "fileType": false
         }
      ]
   },
   {
      "name":"preposiciones7",
      "words":[
         {
            "name":"humilde",
            "file":"1eN1nZ8uLtncWQQOaj4aXkJCI7W59fe4_",
            "fileType": false
         },
         {
            "name":"importante",
            "file":"1o9-x0-GWB9u7lhQ4vM3R7pddPw4R8vSE",
            "fileType": false
         },
         {
            "name":"inteligente",
            "file":"1ect02AwpEIwiaEHKj3zhRouRIfsi8LHM",
            "fileType": false
         },
         {
            "name":"jamas",
            "file":"12bJ27VMy8gN2nWMUxT_Ln7L_lUN_Fw0c",
            "fileType": false
         },
         {
            "name":"junta",
            "file":"1fRjJAHwAx-yh-TfSAeDoNk3qR-U5JjAU",
            "fileType": false
         },
         {
            "name":"junto",
            "file":"1-vqnNC4enoniOvMmkzqxu-SkddjP78Vx",
            "fileType": false
         },
         {
            "name":"lejos",
            "file":"17YoVA3RVj5pLaOKEGqR9hdu0yvS1fkUw",
            "fileType": false
         },
         {
            "name":"libre",
            "file":"1YMl4gf9uQzDAIlPkSxMgciLQj46JtMf8",
            "fileType": false
         },
         {
            "name":"loco",
            "file":"12OJM5e1JJrQjBZO29okXzK0JXEBJ8I6R",
            "fileType": false
         }
      ]
   },
   {
      "name":"preposiciones8",
      "words":[
         {
            "name":"lsm",
            "file":"1dyIeuHpicUjHO3O8LuDLjRKwZTtobB-A",
            "fileType": false
         },
         {
            "name":"malo",
            "file":"1UpWvJ7UmPPF6v6vkcE-2csytw4g3N4EH",
            "fileType": false
         },
         {
            "name":"mas",
            "file":"1xqi0j9dyfqsDOlXlVnA4FZjpUmVgt5fz",
            "fileType": false
         },
         {
            "name":"mejor",
            "file":"1pNDcI2mg5pbU2sC9Qm7zn-_1KqboiEPx",
            "fileType": false
         },
         {
            "name":"miedo",
            "file":"1DMcNWgVWXJ11w8HBD7A2mLsjylUWhaTi",
            "fileType": false
         },
         {
            "name":"necio",
            "file":"10KykUFtY-yebnXKwfFI4Jb6U94bEWB8l",
            "fileType": false
         },
         {
            "name":"no",
            "file":"1Y5MLmGi_8Dhv6yApsPs6-BWkODv39Vek",
            "fileType": false
         },
         {
            "name":"nuevo",
            "file":"19IH4U-dlTt7G2VoJIxTy9-qPzEzA0Hwy",
            "fileType": false
         },
         {
            "name":"nunca",
            "file":"1KWRgC9ModW14glzhh456QbUdnmtoPUBU",
            "fileType": false
         }
      ]
   },
   {
      "name":"preposiciones9",
      "words":[
         {
            "name":"ojala",
            "file":"19uR51zBEK-0vK4X0p6iDK1nhaEQKlwoh",
            "fileType": false
         },
         {
            "name":"paciencia",
            "file":"1m3ewZC_gg-MeTC3DR3O0ZW1Iv490GqIy",
            "fileType": false
         },
         {
            "name":"peor",
            "file":"1G-a43lMMdaMPKAfLaAFywjEz6srWFDr0",
            "fileType": false
         },
         {
            "name":"pero",
            "file":"1B12wEe1QyH21UwlAcFjE8AD8F5-67dt8",
            "fileType": false
         },
         {
            "name":"pobre",
            "file":"1FS6yknoK6ft7MOyIMJQmFh0jruNTG3HU",
            "fileType": false
         },
         {
            "name":"presumido",
            "file":"1o3cbZzlMtm0iVjVSDtQPGKd4_IEq5hbp",
            "fileType": false
         },
         {
            "name":"problema",
            "file":"1iAHMpERA7_dseLqjqSBdKPKHc2f4S10G",
            "fileType": false
         },
         {
            "name":"rapido pronto",
            "file":"1y2MjPzQFqjvHr4Cv9OTh-jBZrSuqJecS",
            "fileType": false
         },
         {
            "name":"raro",
            "file":"1d6nHGX5l1c2lVW-OUQ3EL5q04xsDtdgO",
            "fileType": false
         }
      ]
   },
   {
      "name":"preposiciones10",
      "words":[
         {
            "name":"secreto",
            "file":"1xmEVZVmxpWqRne3y86yxEoNQPC7mKt_h",
            "fileType": false
         },
         {
            "name":"sena propia",
            "file":"1XMKCWXI1Ow41Gw5KMJeblP00kjzxkVcA",
            "fileType": false
         },
         {
            "name":"senas",
            "file":"12T3Qsxdn3IpUZLd7sPCj7Ym2OMQVwCIG",
            "fileType": false
         },
         {
            "name":"si",
            "file":"1Avo9ZeNYLJfcKUQ-GeYkp9FygQ7qadf7",
            "fileType": false
         },
         {
            "name":"sucio",
            "file":"1K9qeygejb0yh3vqERWCy95YjOeT7m6Ug",
            "fileType": false
         },
         {
            "name":"suerte",
            "file":"1TNSlUhKCPzDjNvXsdVZDmn15RuQ0EVFS",
            "fileType": false
         }
      ]
   },
   {
      "name":"preposiciones11",
      "words":[
         {
            "name":"todo",
            "file":"1KQkq4oZ6u2lDjpeMT3Do0E5g21m93ub4",
            "fileType": false
         },
         {
            "name":"tonto",
            "file":"1JzDFM9l_l7-1zZGKwxKDXKF3gw8woyS-",
            "fileType": false
         },
         {
            "name":"travieso",
            "file":"1_10NsKrjoxj-3Fhd2l1__3EYCALg-6QA",
            "fileType": false
         },
         {
            "name":"triste",
            "file":"1KwVR_g5Wide_YKJzG6TUDxubA0AomkMr",
            "fileType": false
         },
         {
            "name":"verdad",
            "file":"1oiE7UPduyJKmoDRcdwLQem-AN8ryZ_BP",
            "fileType": false
         },
         {
            "name":"verguenza",
            "file":"1-VsRJfdokJsOIkPJ50tz_hNt2zqPp6iO",
            "fileType": false
         }
      ]
   }
])


'''
