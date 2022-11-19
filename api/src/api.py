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
from dotenv import load_dotenv  # esto para las variables de entorno .env
import os
from flask import Flask, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
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
    # si encuentra un usuario con ese username manda error
    if mongo.db.users.find_one({'username': json['username']}) != None:
        return {'msj': 'ya existe este username', 'ERROR': 'si'}
    # si encuentro un usuario con este email mando error
    if mongo.db.users.find_one({'email': json['email'].lower()}) != None:
        return {'msj': 'ya esta en uso este correo', 'ERROR': 'si'}

    if json['username'] and json['password'] and json['email'] and (json['username'] != "") and (json['password'] != "") and (json['email'] != ""):
        json['email'] = json['email'].lower()  # ponemos el mail en minusculas
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
# =====================================================================================================

# -----------------------------LOGIN---------------------------------------
# falta cifrado de la contraseña para comparar contraseña cifrada con no cifrada


@app.route('/user/login', methods=['POST'])
def login():
    # recibe usuario/correo y contraseña en un json asi
    # {"username":usuario/correo,, "password": contraseña}
    json = request.json
    # reviso si el usuario puso su username o su correo
    if "@" in json['username']:  # es un correo
        data = mongo.db.users.find_one({'email': json['username'].lower(), 'password': json['password']}, {
                                       '_id': 1, 'username': 1, 'email': 1, 'group': 1, 'type': 1})
    else:
        data = mongo.db.users.find_one({'username': json['username'], 'password': json['password']}, {
                                       '_id': 1, 'username': 1, 'email': 1, 'group': 1, 'type': 1})

    if data == None:
        if "@" in json['username']:
            return {'ERROR': "correo o contraseña incorrecta"}
        else:
            return {'ERROR': "nombre de usuario o contraseña incorrecta"}
    else:
        r = {
            '_id': str(data['_id']),
            'username': data['username'],
            'email': data['email'],
            'type': data['type'],  # 1 admin,   0 normal
            'group': data['group']
        }
        return r
    # regresa el siguiente json {"_id":string, "username": string, "email": string, "type": bool}
    # si el usuario tiene grupo regresa
    #{"_id":string, "username": string, "email": string, "type": bool, "group":string}
# =========================================================================

# -------------------------------Join Group---------------------------------


@app.route('/user/joinGroup', methods=['POST'])
def joinGroup():
    # {_id:"636c330384831804d80d0283, groupCode: "vVlkLalskcjhlk12csda81"}
    json = request.json
    grupo = mongo.db.groups.find_one({'code': json['groupCode']})
    if grupo == None:
        return {"msj": "ERROR Codigo invalido"}

    id = json['_id']
    objId = ObjectId(id)

    user = mongo.db.users.find_one({"_id": objId}, {"group": 1})

    if "group" in user:  # si ya estas en un grupo no te dejara unirte a otro
        return {"msj": "ERROR ya estas en un grupo"}

    # si no estas en un grupo, te mete a el
    mongo.db.users.update_one(
        {"_id": objId},
        {"$set": {"group": grupo["name"]}},
        upsert=False)

    return {"msj": "te uniste al grupo"}
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


@app.route('/user/grades', methods=['POST'])
def checkGrades():
    #{username:leo, _id: 12312412414}
    json = request.json

    objInstance = ObjectId(json['_id'])

    data = mongo.db.users.find_one({'_id': objInstance}, {'grades': 1})
    return data["grades"]
# ========================================================================

# --------------------------Actualizar calificacion----------------------


@app.route('/user/setGrade', methods=['POST'])
def setGrade():
    # {_id:13325fdsf, categorie:letras1, grade:90}
    json = request.json
    id = json["_id"]
    objId = ObjectId(id)

    mongo.db.users.update_one({"_id": objId},
                              {"$set":
                                  {f'grades.{json["categorie"]}': json["grade"]}
                               })
    return {"msj": f'calificación de {json["categorie"]} actualizada a {json["grade"]}'}
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
            r.append(word["name"])
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
                return {"file": word["file"]}
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


    response = {'results': random.shuffle(quiz)}
    return response
# =======================================================================


# =========================================================================
# ===================       GROUP (para admin)     ========================
# =========================================================================
# =========================================================================

# ------quiz con % de personas en el grupo que han terminado el nivel------
# ejemplo /group/John%20Deere
@app.route('/group/<group>', methods=['GET'])
def getPorQuiz(group):
    count = 0
    r = {}

    for i in mongo.db.users.find({'group': group}, {'grades': 1}):
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
        result.append({"name": i, "percentage": r[i]})

    return {"data": result}


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


--------------------------------------------------------------------------------------

use('signaDB')

db.categories.insertMany([
  {'name':'verboscomunes1', 'words':[
                                        {'name':'trabajar', 'file':'https://drive.google.com/file/d/1hE6KI9x1R8JARjzqGpqwl3q7gSr9epZF/view?usp=share_link'},
                                        {'name':'vender', 'file':'https://drive.google.com/file/d/1d-0rGtR_vCGtMHrvGGcoMGlTRuKKIiOe/view?usp=share_link'},
                                        {'name':'terminar', 'file':'https://drive.google.com/file/d/1Y6bZb5vZQGVxuFST4tHntIpHa0Mubay_/view?usp=share_link'},
                                        {'name':'sentar', 'file':'https://drive.google.com/file/d/1JNA2N4mKh-IRiuuvaEBD2ou9HQ_RqKuN/view?usp=share_link'},
                                        {'name':'ver', 'file':'https://drive.google.com/file/d/16yHdpwYUjhadnViFZ6-1fcSYlZ4cc0e-/view?usp=share_link'},
                                        {'name':'preguntar', 'file':'https://drive.google.com/file/d/1zsv9aENoH7mQZqh6FfWR6nalDMUWyPZe/view?usp=share_link'},
                                        {'name':'vivir', 'file':'https://drive.google.com/file/d/1N1QCts462umG_XaTxBKE_VQJ2uVqWqcw/view?usp=share_link'},
                                        {'name':'olvidar', 'file':'https://drive.google.com/file/d/1J0hw1XUzdDRzqQUyKIX8TPaRKOcpfkFl/view?usp=share_link'},
                                        {'name':'pensar', 'file':'https://drive.google.com/file/d/1J0hw1XUzdDRzqQUyKIX8TPaRKOcpfkFl/view?usp=share_link'}
  ]},
  {'name':'verboscomunes2', 'words':[
                                        {'name':'limpiar', 'file':'https://drive.google.com/file/d/1J0hw1XUzdDRzqQUyKIX8TPaRKOcpfkFl/view?usp=share_link'},
                                        {'name':'jugar', 'file':'https://drive.google.com/file/d/16yIVbzbYGUItoM28aIdCB5JIgq1aFJqN/view?usp=share_link'},
                                        {'name':'hacer', 'file':'https://drive.google.com/file/d/1wk202bGUbrmfys9Ruw1fdclxziXRHtXz/view?usp=share_link'},
                                        {'name':'poder', 'file':'https://drive.google.com/file/d/1mPFtW2_7KscqyCunxGH0t0S35z4sbv-O/view?usp=share_link'},
                                        {'name':'necesitar', 'file':'https://drive.google.com/file/d/1khmC3HBe2cDqYv1VROxII2Vsk5aPhB-n/view?usp=share_link'},
                                        {'name':'platicar', 'file':'https://drive.google.com/file/d/1aSyg8tRERW-NOAnwxS1xHJFCnVlpXogm/view?usp=share_link'},
                                        {'name':'perder', 'file':'https://drive.google.com/file/d/1V5meY2_ZeBrRCrMmLH953L7GYzKBFlaB/view?usp=share_link'},
                                        {'name':'pagar', 'file':'https://drive.google.com/file/d/1LbjI90O4N7l9uEVNvFJgwyUqB6VkzScq/view?usp=share_link'},
                                        {'name':'dormir', 'file':'https://drive.google.com/file/d/1mOXmIHVR7ggYg8CiQQ-M4daSb6F2qX0x/view?usp=share_link'}
  ]},
  {'name':'verboscomunes3', 'words':[
                                        {'name':'esperar', 'file':'https://drive.google.com/file/d/1fWe5eihhYHD-HnrhTgSXTvhN0rm9Q_q3/view?usp=share_link'},
                                        {'name':'hablar', 'file':'https://drive.google.com/file/d/15DMpFHkD1wdTg_lP2U29ZtKHr3HLpx7Y/view?usp=share_link'},
                                        {'name':'explicar', 'file':'https://drive.google.com/file/d/1-yPXEYY8Pi3ly_XVFb8ND5ewC4l67ZKB/view?usp=share_link'},
                                        {'name':'entender', 'file':'https://drive.google.com/file/d/1narMLONGXHiNfl283_5OOZE5PlyQ_Li-/view?usp=share_link'},
                                        {'name':'ensenar', 'file':'https://drive.google.com/file/d/1kX5K-iWh1Z8NzagdA4tH456rmhVi2l5d/view?usp=share_link'},
                                        {'name':'escribir', 'file':'https://drive.google.com/file/d/1PV9DVum475bK86GVEKsPouoMUnDbD2Il/view?usp=share_link'},
                                        {'name':'empezar', 'file':'https://drive.google.com/file/d/1JhJYtrFj7L1jQoIBxWPAb8xBRQ40cWlh/view?usp=share_link'},
                                        {'name':'estudiar', 'file':'https://drive.google.com/file/d/1DAXVO261BxSNfGZQE4UcNHMTIo9DAskO/view?usp=share_link'},
                                        {'name':'descansar', 'file':'https://drive.google.com/file/d/1snVQMRrKa4j6yPTIvQK-IM7TZjgzNs7F/view?usp=share_link'}
  ]},
  {'name':'verboscomunes4', 'words':[
                                        {'name':'decir', 'file':'https://drive.google.com/file/d/1AO-s5POxhvnd9O0FXipYsEHfJLPXHAem/view?usp=share_link'},
                                        {'name':'dar', 'file':'https://drive.google.com/file/d/14kkgbo5JvtDjR4ksGYm6SAGkJGmJdDtL/view?usp=share_link'},
                                        {'name':'comprar', 'file':'https://drive.google.com/file/d/1o_CK3zJDG4-TAvMpGCHlfXZV_STITe94/view?usp=share_link'},
                                        {'name':'cuidar', 'file':'https://drive.google.com/file/d/1j5WE8NHiagQw_jK0o2n5z2rE3MfT2OAS/view?usp=share_link'},
                                        {'name':'comer', 'file':'https://drive.google.com/file/d/1giPqNXADvifbRWuGun_jHRsTsw58tmk_/view?usp=share_link'},
                                        {'name':'avisar', 'file':'https://drive.google.com/file/d/1Wfe-JYnfS434eIzqGTy2Ngf04A5pJjBL/view?usp=share_link'},
                                        {'name':'creer', 'file':'https://drive.google.com/file/d/1QTmDIZFt3fm8A8238Fuu01UTIPCKA33b/view?usp=share_link'},
                                        {'name':'ayudar', 'file':'https://drive.google.com/file/d/1HT2_GvXEMYJM5Bee7UAx_Ftui671XOHB/view?usp=share_link'},
                                        {'name':'aprender', 'file':'https://drive.google.com/file/d/1ETwID4Y1KVu7t0AAoJcAMY-vLC1dSDjj/view?usp=share_link'}
  ]},
  {'name':'letras1', 'words':[
                                        {'name':'A', 'file': 'https://drive.google.com/file/d/1QKqGSkKy5a7CYT0hmX9u-kFHB7wP-5_M/view?usp=share_link'},
                                        {'name':'B', 'file': 'https://drive.google.com/file/d/1dR3s-hLkT2X5vZ018gF5wIQfIrJR5jEV/view?usp=share_link'},
                                        {'name':'C', 'file': 'https://drive.google.com/file/d/1YarH3jcDbTmcsokRw5ZZjGNU2CrXEpmz/view?usp=share_link'},
                                        {'name':'D', 'file': 'https://drive.google.com/file/d/1QKqGSkKy5a7CYT0hmX9u-kFHB7wP-5_M/view?usp=share_link'},
                                        {'name':'E', 'file': 'https://drive.google.com/file/d/1q0LzcnNB7YiEpd-aCL5lzUZJPcNmPKfA/view?usp=share_link'},
                                        {'name':'F', 'file': 'https://drive.google.com/file/d/1Kb5NESMCR8NQMigR8M10r2lsCoPIDRFC/view?usp=share_link'},
                                        {'name':'G', 'file': 'https://drive.google.com/file/d/1Kb5NESMCR8NQMigR8M10r2lsCoPIDRFC/view?usp=share_link'},
                                        {'name':'H', 'file': 'https://drive.google.com/file/d/1kJHbFQuIq4-uEv7ZFvgIB5NTNbPcIPkB/view?usp=share_link'},
                                        {'name':'I', 'file': 'https://drive.google.com/file/d/1kJHbFQuIq4-uEv7ZFvgIB5NTNbPcIPkB/view?usp=share_link'},
                                        {'name':'J', 'file':'https://drive.google.com/file/d/1CUfKsJ6gsPyJUxkSJHch0-CX_Y3AlZ2w/view?usp=share_link'},]},
    {'name':'letras2', 'words':[
                                        {'name':'K', 'file': 'https://drive.google.com/file/d/1t6WZb35qND4_bVG8e69wo0UFBjK1GFKP/view?usp=share_link'},
                                        {'name':'L', 'file': 'https://drive.google.com/file/d/1t6WZb35qND4_bVG8e69wo0UFBjK1GFKP/view?usp=share_link'},
                                        {'name':'LL','file':'https://drive.google.com/file/d/1n486o9HvJbfCDlbpDPvTfz5VocHopLwy/view?usp=share_link'},
                                        {'name':'M', 'file': 'https://drive.google.com/file/d/13XYgt5aH-d0f-4SAniF6RNnIK5sTRxy6/view?usp=share_link'},
                                        {'name':'N', 'file': 'https://drive.google.com/file/d/1LW-Z5_Zu9ndoSewTC_GdSrqbyzTkWcWh/view?usp=share_link'},
                                        {'name':'Ñ', 'file':'https://drive.google.com/file/d/19imxu_cFgZgK5WNuaAj3SAVWE5iAB_AI/view?usp=share_link'},
                                        {'name':'O', 'file': 'https://drive.google.com/file/d/19imxu_cFgZgK5WNuaAj3SAVWE5iAB_AI/view?usp=share_link'},
                                        {'name':'P', 'file': 'https://drive.google.com/file/d/19imxu_cFgZgK5WNuaAj3SAVWE5iAB_AI/view?usp=share_link'},
                                        {'name':'Q', 'file':'https://drive.google.com/file/d/1A3k25-Hf5gmRsYCjkD60Yw4ftDT8VNRD/view?usp=share_link'},
                                        {'name':'R', 'file': 'https://drive.google.com/file/d/1nZpQK8pvLMqtDQpbHrcp2Glb9IX2aIgV/view?usp=share_link'},]},
   {'name':'letras3', 'words':[                                     
                                        {'name':'RR','file':'https://drive.google.com/file/d/1wxFwOHp4fjUXepz16zVrwlAmVN4hFKFd/view?usp=share_link'},
                                        {'name':'S', 'file': 'https://drive.google.com/file/d/1PgAqrE6n1oxsYpaUlgFUqSYNj2A47Zgz/view?usp=share_link'},
                                        {'name':'T', 'file': 'hhttps://drive.google.com/file/d/18DIh-xbUHitO9dPH5DCzim7Hoe8fRKsF/view?usp=share_link'},
                                        {'name':'U', 'file': 'https://drive.google.com/file/d/1QZfGLg0PUTDATc21CiAeQglwhoFgAOub/view?usp=share_link'},
                                        {'name':'V', 'file': 'https://drive.google.com/file/d/1oOShSo09J44A7ffK8grorZM4WbURwtzm/view?usp=share_link'},
                                        {'name':'W', 'file': 'https://drive.google.com/file/d/17BA0BQlvoBuCctby1cgxsO9ajdGrgDRP/view?usp=share_link'},
                                        {'name':'X', 'file':'https://drive.google.com/file/d/1MsKU9mY01oERDzK8SQTCXcRQHhT9pIIT/view?usp=share_link'},
                                        {'name':'Y', 'file': 'https://drive.google.com/file/d/1SuTELApPhQK8hEigmW8tBDLHJYncEhu8/view?usp=share_link'},
                                        {'name':'Z', 'file':'https://drive.google.com/file/d/1rkcHFzQYc--YQZNVLr9SPxvmhWKtrZgq/view?usp=share_link'}
  ]},                
  {'name':'verbosnarrativos1', 'words':[
                                        {'name':'servir', 'file':'https://drive.google.com/file/d/1Ud---J72QE0MUPzd4NH3npIExKbvOZLk/view?usp=share_link'},
                                        {'name':'saber', 'file':'https://drive.google.com/file/d/1ou5i7zNdlvhm7iKqvlEQDLtZhqG-pkrY/view?usp=share_link'},
                                        {'name':'querer', 'file':'https://drive.google.com/file/d/1ELqHMYTt5C_Se9XF129Glz02aVVbVbCu/view?usp=share_link'},
                                        {'name':'poder', 'file':'https://drive.google.com/file/d/169kRhE5eKtu125LMjxK1SQbOsyAZbQpV/view?usp=share_link'},
                                        {'name':'noservir', 'file':'https://drive.google.com/file/d/1fUx9tery_Izc0iUlFuIV7YI5kmd9BJTl/view?usp=sharing'},
                                        {'name':'nosaber', 'file':'https://drive.google.com/file/d/1q4zydlRcIayMwfW69ARDQPvIcW0dvQm_/view?usp=sharing'},
                                        {'name':'noquerer', 'file':'https://drive.google.com/file/d/1c4hMrYxHMH_PY1A81qcfFPOetT3ls-i8/view?usp=share_link'},
                                        {'name':'nopoder', 'file':'https://drive.google.com/file/d/1ssUoQOAOCRXpLb9HWH-E_P8DIGyDUmzL/view?usp=sharing'}
  ]},
  {'name':'verbosnarrativos2', 'words':[
                                        {'name':'nohaber', 'file':'https://drive.google.com/file/d/1GyHPxm-V-S_S0MRJaNFoJk0U3xS5kR1e/view?usp=sharing'},
                                        {'name':'nogustar', 'file':'https://drive.google.com/file/d/103cjwdawHurtShohvLhEg-ChT8M_bS5g/view?usp=sharing'},
                                        {'name':'noentender', 'file':'https://drive.google.com/file/d/1lVljz8BhGWqMfbQpaRTiDg_lK73vRANv/view?usp=share_link'},
                                        {'name':'noconocer', 'file':'https://drive.google.com/file/d/1FARSdS7lP_tdsFrfJAwS7P2BVtPZ7M-H/view?usp=share_link'},
                                        {'name':'haber', 'file':'https://drive.google.com/file/d/1FARSdS7lP_tdsFrfJAwS7P2BVtPZ7M-H/view?usp=share_link'},
                                        {'name':'gustar', 'file':'https://drive.google.com/file/d/1ViagIzPoiRPiT-T3Lb5kGf7UIff9q4to/view?usp=share_link'},
                                        {'name':'entender', 'file':'https://drive.google.com/file/d/16AmiHxTdTB9uK-qNWmr2y8FGcd4ixMc2/view?usp=share_link'},
                                        {'name':'conocer', 'file':'https://drive.google.com/file/d/1ON7LpFIox8Wgw8LdZCoIAxcv_Zbxq-9i/view?usp=share_link'}
  ]},
  {'name':'preposiciones1', 'words':[
                                        {'name':'abajo', 'file':'https://drive.google.com/file/d/1ehxV6X169VEMuCCd9L0gMyXvRZ847Cw8/view?usp=share_link'},
                                        {'name':'aburrido', 'file':'https://drive.google.com/file/d/1URt5j6k3MQNYikBu9WaP9nNR8dADYaVX/view?usp=share_link'},
                                        {'name':'accidente', 'file':'https://drive.google.com/file/d/1nhMgs-138MnRKZDnfrADms8JrelZ4yxe/view?usp=share_link'},
                                        {'name':'adentro', 'file':'https://drive.google.com/file/d/1eAG9MFN2CCUPl6Rl1sQkbbSKLDQWEW5t/view?usp=share_link'},
                                        {'name':'afortunado', 'file':'https://drive.google.com/file/d/1VxS11GQym2rVaRMuFuuIPao0LpZBjt6v/view?usp=share_link'},
                                        {'name':'alegredivertido', 'file':'https://drive.google.com/file/d/1euHYdQb0NZzQ04Y50CI2oXRnWhU-0K3_/view?usp=share_link'},
                                        {'name':'algunos', 'file':'https://drive.google.com/file/d/17D0sg4XWEys8ZydRAmX6511Jbr89Jkem/view?usp=share_link'},
                                        {'name':'altoestatura', 'file':'https://drive.google.com/file/d/1uIoMkwerb_9p8m23zy9S4Az6HJl_mOVq/view?usp=share_link'},
                                        {'name':'amable', 'file':'https://drive.google.com/file/d/1qxLg_1Sl-XUR9USFueyrxz5RhBiPoahj/view?usp=share_link'}
  ]},
  {'name':'preposiciones2', 'words':[
                                        {'name':'antes', 'file':'https://drive.google.com/file/d/1qwHRubYinh7X4AMlE_NwEjNbOda8J0FS/view?usp=share_link'},
                                        {'name':'arriba', 'file':'https://drive.google.com/file/d/1In2_EbTbBD0TSEzo268FgOT3HStQK68P/view?usp=share_link'},
                                        {'name':'asustado', 'file':'https://drive.google.com/file/d/1hOoISfqQ2aRHp_9q5_bqbRDeuRiKGLev/view?usp=share_link'},
                                        {'name':'atencionatento', 'file':'https://drive.google.com/file/d/1ACWP6NIfK0NREDyAWLbcIkRknntvOtmd/view?usp=share_link'},
                                        {'name':'baboso', 'file':'https://drive.google.com/file/d/1_yoC8kKNMlj0ZIkGLg96_tZ1IJW-t1qW/view?usp=share_link'},
                                        {'name':'bonito', 'file':'https://drive.google.com/file/d/1mpHOirn_7lmz9C-XJ_eN7p2-JRgYBh4d/view?usp=share_link'},
                                        {'name':'broma', 'file':'https://drive.google.com/file/d/1yp9TaXY4nEhBR6XxxnGvZxXrWqd-5T_E/view?usp=share_link'},
                                        {'name':'bueno', 'file':'https://drive.google.com/file/d/114hHywQN8-aVI8qnA8mSthJMzsb0QfeM/view?usp=share_link'},
                                        {'name':'cada', 'file':'https://drive.google.com/file/d/1pzTHjAm6DYU0Mn9F6gk0kG2gaO1qGk_V/view?usp=share_link'}
  ]},
  {'name':'preposiciones3', 'words':[
                                        {'name':'caliente', 'file':'https://drive.google.com/file/d/1f8GpcwKsnEXzNAWkc1W5ab58Jn-NfKDg/view?usp=share_link'},
                                        {'name':'cansado', 'file':'https://drive.google.com/file/d/1F2uhztxfGeqQsJ7_HpH88LX6qe70QvUQ/view?usp=share_link'},
                                        {'name':'carino', 'file':'https://drive.google.com/file/d/1_UqKJ5RL-ns7zgmGKjLH8w-1dcAL0Lu0/view?usp=share_link'},
                                        {'name':'celoso', 'file':'https://drive.google.com/file/d/1rUGdwNksyGwuDYLpN80l85ANlKU94e5V/view?usp=share_link'},
                                        {'name':'chaparro', 'file':'https://drive.google.com/file/d/1m6-ympZgLD48ZFUJufiUbaQryz-SFJhj/view?usp=share_link'},
                                        {'name':'chistoso', 'file':'https://drive.google.com/file/d/1SvRlZPYl-MgH6bZpacU9KtlTIXNkiKjk/view?usp=share_link'},
                                        {'name':'cobarde', 'file':'https://drive.google.com/file/d/1iwF5X4LVEZPYg24tFyWf3-s_BM4q1H8_/view?usp=share_link'},
                                        {'name':'contento', 'file':'https://drive.google.com/file/d/1x3Q5GEx6u-B-0-ZuTUL_e3wjPDCK59hC/view?usp=share_link'},
                                        {'name':'curioso', 'file':'https://drive.google.com/file/d/1dgNo1rsPSzoO6AdyUFfKA6dBLj7fuuNB/view?usp=share_link'}
  ]},
  {'name':'preposiciones4', 'words':[
                                        {'name':'debil', 'file':'https://drive.google.com/file/d/1a8_rPbWsbTkNFxajyiqgvLqlk0JCyUbt/view?usp=share_link'},
                                        {'name':'decente', 'file':'https://drive.google.com/file/d/19iOIXapGyX8NXJe1wCEBDk0oEM1H_9D0/view?usp=share_link'},
                                        {'name':'delgado', 'file':'https://drive.google.com/file/d/1y_gXYiH0mMbvRV9-jhuHKcJUCDYszSDy/view?usp=share_link'},
                                        {'name':'despacio', 'file':'https://drive.google.com/file/d/1vMzQIg6U7mzL1JL_j5h8dUDwQZskqtnG/view?usp=share_link'},
                                        {'name':'diferente', 'file':'https://drive.google.com/file/d/19zfOb1l8ycpRBEWpFFkI9plmG418jliI/view?usp=share_link'},
                                        {'name':'dificil', 'file':'https://drive.google.com/file/d/1ArwbF-lLHxGwkeNFaJ7ixiiPTxMoUN9K/view?usp=share_link'},
                                        {'name':'diploma', 'file':'https://drive.google.com/file/d/1ypSehebLvS8Eely4vQpd13sVlsp95Cs9/view?usp=share_link'},
                                        {'name':'duda', 'file':'https://drive.google.com/file/d/1wHcvdV84OBJbSJ-vAjOjq_L3K-mSD5pQ/view?usp=share_link'},
                                        {'name':'egoista', 'file':'https://drive.google.com/file/d/1TwG92j7JVUZwoMKMvAqt39GKbq2JaV6H/view?usp=share_link'}
  ]},
  {'name':'preposiciones5', 'words':[
                                        {'name':'ejemplo', 'file':'https://drive.google.com/file/d/14v2o_5GW_2FGDsGbsosejKBNwtcchkuz/view?usp=share_link'},
                                        {'name':'ejercicio', 'file':'https://drive.google.com/file/d/1Z_hFhz8eK0qFTBWRhKJ2aPmempOTg7No/view?usp=share_link'},
                                        {'name':'enojado', 'file':'https://drive.google.com/file/d/1eXtTtCqJcxKELTixhu13q6NqJBmV1vyT/view?usp=share_link'},
                                        {'name':'envidia', 'file':'https://drive.google.com/file/d/1vNoXTMCwbxFd79VnimbabeYVlXKH2Bb1/view?usp=share_link'},
                                        {'name':'especial', 'file':'https://drive.google.com/file/d/1bmDrI6NST8DbG23Xma_mhV-7PT-FwNSL/view?usp=share_link'},
                                        {'name':'facil', 'file':'https://drive.google.com/file/d/1kwRZbH97RHBUBqGGbGspOAw6O2B0aaxi/view?usp=share_link'},
                                        {'name':'falso', 'file':'https://drive.google.com/file/d/1FT2ZjIOHvkiQXPiIQX0PNsVuWpVNZlDV/view?usp=share_link'},
                                        {'name':'feliz', 'file':'https://drive.google.com/file/d/1wdWwaHfmj367Pf17DswEaAnzqAVkjuK1/view?usp=share_link'},
                                        {'name':'feo', 'file':'https://drive.google.com/file/d/1HWPJ0jdjhw1SYUKIu6QQpYCxqsJwGaeQ/view?usp=share_link'}
  ]},
  {'name':'preposiciones6', 'words':[
                                        {'name':'flojo', 'file':'https://drive.google.com/file/d/1bgsvIRYFIaDxOHKqsCpn9ncnjhqbY3Th/view?usp=share_link'},
                                        {'name':'fuerte', 'file':'https://drive.google.com/file/d/11NEygLTxOZbBhwx7imBgSr7TL0KjfO9j/view?usp=share_link'},
                                        {'name':'fuerza', 'file':'https://drive.google.com/file/d/14o4vV1uiTFn6yTxplbdtZ2nkGdIN9mdQ/view?usp=share_link'},
                                        {'name':'gordo', 'file':'https://drive.google.com/file/d/16sk8T7R5vsDwoUal_XIh_SxClOw9p6E1/view?usp=share_link'},
                                        {'name':'gratis', 'file':'https://drive.google.com/file/d/1Ncy3K75A6hL8o1Lw3NQ1Q4k9XY5GfR0Q/view?usp=share_link'},
                                        {'name':'grosero', 'file':'https://drive.google.com/file/d/1R-NrgIdgIM28qeNbnNa3Om9pA8Dkp3kA/view?usp=share_link'},
                                        {'name':'guapo', 'file':'https://drive.google.com/file/d/1lzqVnzzui5ib-ClKNiUUXghuDE8nyo9x/view?usp=share_link'},
                                        {'name':'hambre', 'file':'https://drive.google.com/file/d/1xJHsF9hh2OVQ_2JLNKthp01UQWDVsA4K/view?usp=share_link'},
                                        {'name':'historia', 'file':'https://drive.google.com/file/d/1pgxyYVUZmqqm1-7X91-nivANTjmmK0_K/view?usp=share_link'}
  ]},
  {'name':'preposiciones7', 'words':[
                                        {'name':'humilde', 'file':'https://drive.google.com/file/d/1HV8b07kjZd2hYyVXvLqKCuTXGCGSmnG5/view?usp=share_link'},
                                        {'name':'importante', 'file':'https://drive.google.com/file/d/1IsAFuzFZLGWzUSHO4EW255-vVLxkIOR0/view?usp=share_link'},
                                        {'name':'inteligente', 'file':'https://drive.google.com/file/d/1ZxgE9F4VOlIuB7tyYGwfaF8LSI7lg4Ul/view?usp=share_link'},
                                        {'name':'jamas', 'file':'https://drive.google.com/file/d/1h-LgBms6G79qRD8poNlM21tPLKhaQS8d/view?usp=share_link'},
                                        {'name':'junta', 'file':'https://drive.google.com/file/d/1XUJisdMxC1vE2oTg1DexBbJC5djEtKjy/view?usp=share_link'},
                                        {'name':'junto', 'file':'https://drive.google.com/file/d/19FgFO7cYtJ20n92aiwtMC7-UkKEu8v3T/view?usp=share_link'},
                                        {'name':'lejos', 'file':'https://drive.google.com/file/d/1XUlO69Rr5H9EBkqJESxfEDWFK5ih-8DB/view?usp=share_link'},
                                        {'name':'libre', 'file':'https://drive.google.com/file/d/1cfLSL5Apxx3d6RqO0k0vrsY_JdPpfC_f/view?usp=share_link'},
                                        {'name':'loco', 'file':'https://drive.google.com/file/d/1N1mplhYBbxoSjikgz7mMGFGcZuNosyom/view?usp=share_link'}
  ]},
  {'name':'preposiciones8', 'words':[
                                        {'name':'lsm', 'file':'https://drive.google.com/file/d/1BpYmPXrCue5aLqsz_cqtru2LczJHscHP/view?usp=share_link'},
                                        {'name':'malo', 'file':'https://drive.google.com/file/d/1UISROGdMnrmz9yJCMirYCG295SUT4PkZ/view?usp=share_link'},
                                        {'name':'mas', 'file':'https://drive.google.com/file/d/1Qc-eTdfhNVHVefU79xhAe_n7CBvK3yvY/view?usp=share_link'},
                                        {'name':'mejor', 'file':'https://drive.google.com/file/d/1axh7r0PPfGD0cO3lOzsnJ04HGhaVLr59/view?usp=share_link'},
                                        {'name':'miedo', 'file':'https://drive.google.com/file/d/1q632PiNFm-t7Y70sIez9CW1iRM5VuMJc/view?usp=share_link'},
                                        {'name':'necio', 'file':'https://drive.google.com/file/d/1og2sjv2gPF5vbnkQbrZYYUGzOViDsTHU/view?usp=share_link'},
                                        {'name':'no', 'file':'https://drive.google.com/file/d/1qe-E0FAbbJ_wlPogjtrsjvD2FTY2rdJK/view?usp=share_link'},
                                        {'name':'nuevo', 'file':'https://drive.google.com/file/d/1pHOp9pQZ_wfQZHAoyp2Lhr4S3zhLz23U/view?usp=share_link'},
                                        {'name':'nunca', 'file':'https://drive.google.com/file/d/13AUYYSV-ZmXGhjPCw_8IiowowQnk-Vis/view?usp=share_link'}
  ]},
  {'name':'preposiciones9', 'words':[
                                        {'name':'ojala', 'file':'https://drive.google.com/file/d/1jzAkzrzanY6dj2xJAnLRcmIgtHr7etkl/view?usp=share_link'},
                                        {'name':'paciencia', 'file':'https://drive.google.com/file/d/1UHmjO1fFUYp9vW94JRZDn6-Gr2O91vN2/view?usp=share_link'},
                                        {'name':'peor', 'file':'https://drive.google.com/file/d/10QIyj3VeFoSQ08megN0WufouY6MD0a9Z/view?usp=share_link'},
                                        {'name':'pero', 'file':'https://drive.google.com/file/d/1lIUKRIXC8Qix54ETr7GUra_gvDI2hwxs/view?usp=share_link'},
                                        {'name':'pobre', 'file':'https://drive.google.com/file/d/1Z3JPGovOolnfQUVwsaf2N8_zLWLEuBV0/view?usp=share_link'},
                                        {'name':'presumido', 'file':'https://drive.google.com/file/d/19936vF4_4EEuwjJyj3VP2W-PBaxjUFgC/view?usp=share_link'},
                                        {'name':'problema', 'file':'https://drive.google.com/file/d/1zHHnrfg_k-LBoNIp5xPOA3a7wBV15GpC/view?usp=share_link'},
                                        {'name':'rapidopronto', 'file':'https://drive.google.com/file/d/126sRCNeFQ_it4zs58zAWTnrkNnlivEi8/view?usp=share_link'},
                                        {'name':'raro', 'file':'https://drive.google.com/file/d/1N5TdYQJl1MgwMS2Q4t0CNtuAc7IKJ2uD/view?usp=share_link'}
  ]},
  {'name':'preposiciones10', 'words':[
                                        {'name':'secreto', 'file':'https://drive.google.com/file/d/1Uq2LAr8iFyiamKkjiAPhK--CrEFRbRCm/view?usp=share_link'},
                                        {'name':'senaproipa', 'file':'https://drive.google.com/file/d/1YyTeBLHHtxA14w5XHgNG1AF5QAUzqEsU/view?usp=share_link'},
                                        {'name':'senas', 'file':'https://drive.google.com/file/d/1Kqgp-esKFR4aUpwSRiWtTx5U6H7AA03J/view?usp=share_link'},
                                        {'name':'si', 'file':'https://drive.google.com/file/d/16WreDaMp5EArOVJAxu3r7f29HTsYmDjs/view?usp=share_link'},
                                        {'name':'sucio', 'file':'https://drive.google.com/file/d/1x5k0_i0eMZwdeKSNaCFDW37Co0webFmw/view?usp=share_link'},
                                        {'name':'suerte', 'file':'https://drive.google.com/file/d/17ls3zgvPuYxSxqW88SMTRMkv8sc6KTjM/view?usp=share_link'}
  ]},
  {'name':'preposiciones11', 'words':[
                                        {'name':'todo', 'file':'https://drive.google.com/file/d/1XrRg__5-IGNKswTsmLgas-nm5VWulPOb/view?usp=share_link'},
                                        {'name':'tonto', 'file':'https://drive.google.com/file/d/1X7NdjYLfK65l4FplV8YyM9rQ_SpwyWhu/view?usp=share_link'},
                                        {'name':'travieso', 'file':'https://drive.google.com/file/d/1byTcpmLj89LolqacI7BLwci15uEcbCz0/view?usp=share_link'},
                                        {'name':'triste', 'file':'https://drive.google.com/file/d/141V4L2fV1molFtSvOV8DvIMC2mpqCzpT/view?usp=share_link'},
                                        {'name':'verdad', 'file':'https://drive.google.com/file/d/1-HpZ_Yvj_cb1QbaEAqjpevHieqbodHqB/view?usp=share_link'},
                                        {'name':'verguenza', 'file':'https://drive.google.com/file/d/1iNY-gv4ZqY_ez7iMqLSNZd05EPgcJlKu/view?usp=share_link'},
                                        
                                        ]}
])


==================================

db.categories.insertMany([
  {'name':'verboscomunes1', 'words':[
                                        {'name':'trabajar', 'file':'1tcYRwR7-TW_HrKbFzVu_tv_T60dmXmQ1'},
                                        {'name':'vender', 'file':'1W1xcSIVeu05NqCAFw1ky9tgZ3wfMeP5K'},
                                        {'name':'terminar', 'file':'1PrrUckCLrEn-Xy6eWjLOx4ZVKX8Neq8t'},
                                        {'name':'sentar', 'file':'1Qo9iUabjwh1hUNSK8D2Il6AZNyy9XYgJ'},
                                        {'name':'ver', 'file':'16yHdpwYUjhadnViFZ6-1fcSYlZ4cc0e-'},
                                        {'name':'preguntar', 'file':'1QPw0tfGXe3Oa-dpe73Cebho-rPn77SNd'},
                                        {'name':'vivir', 'file':'1j5pO3MfbnzRDZ4XmnarwMcXiXwxwNZX5'},
                                        {'name':'olvidar', 'file':'1kk2ypAhkvl5mErzZeHdEJBypu2kMQg3S'},
                                        {'name':'pensar', 'file':'15GFkp2n3DJE8L3_9oZBx9Huoz5_6qttv'}
  ]},
  {'name':'verboscomunes2', 'words':[
                                        {'name':'limpiar', 'file':'1YSGyx3CWjXQAnjhyYyZlleywIxzJoiDl'},
                                        {'name':'jugar', 'file':'19nwpa77zl9bL8VOtV4DXDPDJh0hmjVBU'},
                                        {'name':'hacer', 'file':'13B0_4vpidDQXB2PW-TX6CUc_p6pTwjIa'},
                                        {'name':'poder', 'file':'1iv-MH9RIMzcU1pbzvc4uGcgcUS66k5bt'},
                                        {'name':'necesitar', 'file':'1D7HPaXTYNW7jimQUhH6byXsvpGpxULGc'},
                                        {'name':'platicar', 'file':'1z3cmZSxI2z07jmKyPX4pGiQfWzPotrOR'},
                                        {'name':'perder', 'file':'1FdQTvtpCHPUvkVj4_q0fn6H_lCbdkq70'},
                                        {'name':'pagar', 'file':'1RZOCJZHvEeOcIjz0MFsASwqre2q3ZlD2'},
                                        {'name':'dormir', 'file':'1yZ06HrUs8iLkLZLaNBDy3VuZTQzrm8a7'}
  ]},
  {'name':'verboscomunes3', 'words':[
                                        {'name':'esperar', 'file':'1q_wsu6uDzM_sJKebcX2D8Ta4SFnqWk3f'},
                                        {'name':'hablar', 'file':'1Vm3LY7f52ooXjja4Vod1mDBR5KkWC5wz'},
                                        {'name':'explicar', 'file':'14yh2agoxOcE8MD8M7KvYsGZwIEULkWTG'},
                                        {'name':'entender', 'file':'1narMLONGXHiNfl283_5OOZE5PlyQ_Li-'},
                                        {'name':'ensenar', 'file':'10VA78GejwYiMG99TswuunILQhxJmR25R'},
                                        {'name':'escribir', 'file':'1-ov52ractWhgN6D0S8uginy9mGZ1egpu'},
                                        {'name':'empezar', 'file':'1mtDSBRcPSpmwNgGEQIIu5_dVYNqVBQYD'},
                                        {'name':'estudiar', 'file':'1q_wsu6uDzM_sJKebcX2D8Ta4SFnqWk3f'},
                                        {'name':'descansar', 'file':'1GcJJP7RIleNriyKec1V4KYHZA2_7cY_a'}
  ]},
  {'name':'verboscomunes4', 'words':[
                                        {'name':'decir', 'file':'1MiDELxOQOGYs6Bfi4FoijIsKRMUGNpaZ'},
                                        {'name':'dar', 'file':'18XB7dIXL3eOl-tYm6kEagDk9EpZWXg7N'},
                                        {'name':'comprar', 'file':'1mKCyZRI71RjcKQb3FyN_diqNcF8HVXcW'},
                                        {'name':'cuidar', 'file':'1Ot2pd2e65_KYdLyTbZgJH1w9t3PbAwwe'},
                                        {'name':'comer', 'file':'1OwlYlcBEPJ4nnlo-r5G6DMggfiNAuLcy'},
                                        {'name':'avisar', 'file':'1kgcTxgwjwUliTPfoTyNr42hadCs6kbSx'},
                                        {'name':'creer', 'file':'1IaGKc8zge1PsyydVghcggG8mWOQ0ayGo'},
                                        {'name':'ayudar', 'file':'1Qu7wO5AngbRddeLyzjp8TqXGh7D13zuY'},
                                        {'name':'aprender', 'file':'11x8aTxZq647D0DYSYYS4iDitgVHqJDwU'}
  ]},
  {'name':'letras1', 'words':[
                                        {'name':'A', 'file': '1ou7Kmy4Xg_fSDc44uDkB_4tblsmK_Ub1'},
                                        {'name':'B', 'file': '1tKCjpIGoDdDzCHdz7W8Z4Bz_t0_tIVlZ'},
                                        {'name':'C', 'file': '1HONPypOgXdLkiXQW4HjWI9mLarWqqxJ4'},
                                        {'name':'D', 'file': '1HONPypOgXdLkiXQW4HjWI9mLarWqqxJ4'},
                                        {'name':'E', 'file': '1X6f8tsfA4UfrlIkHwExdu6JHRVL85mxe'},
                                        {'name':'F', 'file': '1ZccFRQR-l2E5pbW374NQfoRUJd0povep'},
                                        {'name':'G', 'file': '1Rwf-GvvTY-TvZqGFzagPTgNCxldVtWRd'},
                                        {'name':'H', 'file': '1N-sKQpwHFA8WN9y1v_4iHajqPxMSFFe8'},
                                        {'name':'I', 'file': '1sZaMPpD3jpX7PHwW449oLnyA2LZQf1Or'},
                                        {'name':'J', 'file':'1xsrLa2o_oFXERWY7KAH0_uo_TSPVf9qG'}]},
    {'name':'letras2', 'words':[
			                            {'name':'K', 'file':'1DYQ72t5Xyr0tDx14r0GPScizYLTETDSv'},
                                        {'name':'L', 'file': '1o1736id19a3rdLy0mLOKHstK26Q2I_3X'},
                                        {'name':'LL','file':'1Nho5O9oVKdHuHsaJ2uuqaLMqfASW0Chz'},
                                        {'name':'M', 'file': '1QqhZNjoBCqzTNkgOkuz3aVJbr4-I-COd'},
                                        {'name':'N', 'file': '1L6kg8WFcbn7dIoQFKgA4U0I685emy2SA'},
                                        {'name':'Ñ', 'file':'1Y9cY6rIpHFMzZvcD4SJ4ORhYrC8TqR23'},
                                        {'name':'O', 'file': '1vMdT51TJyWHHv1qMgkZ9CiYrG1jPy6j0'},
                                        {'name':'P', 'file': '1Z7Pp4rRPgIxAArqXcddVpLZZCIGPQUrg'},
                                        {'name':'Q', 'file':'1f-T3A0ZDhCrhqCXjn6X7ATkEh7EvdSHU'},
                                        {'name':'R', 'file': '19WweoR_JXM688W_VuHH_9kCJaQ_iuwWk'}]},
   {'name':'letras3', 'words':[                                     
                                        {'name':'RR','file':'1DkEGIpWEvDMlssFZ04-gcOkJY35ah0am'},
                                        {'name':'S', 'file': '1fg9tziGGnzbIikIbU3M9GpYdtI-OList'},
                                        {'name':'T', 'file': '1t1pz20RzMZHr9xhNYUH6BQ79I6PWiqHf'},
                                        {'name':'U', 'file': '1B1iRhbzH1U0p0IoR_SgMIAU3KgglEBlr'},
                                        {'name':'V', 'file': '1RLs2rbES0kcMCFgCm-t686yu8p8DrGFf'},
                                        {'name':'W', 'file': '1RPBmIN3_U6RZLhw1TA9EBIORrtGQuOij'},
                                        {'name':'X', 'file':'1ASyHj06QMOGVeX29WTrZRm_4MQ1fRpaz'},
                                        {'name':'Y', 'file': '1CiBzqgtUH66aYgkcQRmW0AFE6rDMOmoe'},
                                        {'name':'Z', 'file':'1m9js4flqszhOhN2mAa00brTJAkyPQVn7'}
  ]},                
  {'name':'verbosnarrativos1', 'words':[
                                        {'name':'servir', 'file':'1_hZfXyIyPhwRnyXiCo-Qk49tUIo5-QPh'},
                                        {'name':'saber', 'file':'1I4Frcn6HmLTBF66yk_Y88Lnkm0hdnAV0'},
                                        {'name':'querer', 'file':'1C17G43iKIaxDSDupoDQiTEH2ItbsLahX'},
                                        {'name':'poder', 'file':'1Ck9REvG-LS950k_3N3sapRyb-pL7pVUR'},
                                        {'name':'no servir', 'file':'1apg9CLioaqoeEgJJtPW1SvwSmG5JqO-Z'},
                                        {'name':'no saber', 'file':'1afxu-VnH3I3rqisa-wi8CnbhFXqeURrG'},
                                        {'name':'no querer', 'file':'1e9rb71OIAWOhJTFcXoIH5sANeu0af3iO'},
                                        {'name':'no poder', 'file':'17jiSlroCa5q9_0cq3eF-ZCRKgG8CWXq-'},
  ]},
  {'name':'verbosnarrativos2', 'words':[
                                        {'name':'no haber', 'file':'1f7rSeVNaj5ZPNVdxCXZ2hN7jXe-K-s77'},
                                        {'name':'no gustar', 'file':'1yIkanbC-Ybiibea79ItTNX5HNsNDyWb5'},
                                        {'name':'no entender', 'file':'1wXk1x2s6sDvNHkWvAhAhdTqp07m0CXIG'},
                                        {'name':'no conocer', 'file':'1nLseLOJjV9bIo-3OXNWsiF0spImamdTQ'},
                                        {'name':'haber', 'file':'16f7y7msJqg54j76p6H4S9md9BYlJBa-G'},
                                        {'name':'gustar', 'file':'1cjBY2WFfoXp-2bHIER0ldU2KBIH_ZpnX'},
                                        {'name':'entender', 'file':'1B01IEcnvoprd8K5l8inVdu3QKL4gdmHk'},
                                        {'name':'conocer', 'file':'1AdAvKwAdQy0xBQAyz5Q7smqMhm89g8NH'}
  ]},
 
  {'name':'preposiciones1', 'words':[
                                        {'name':'abajo', 'file':'18lafYZSxJa75PLBA8EOMJkYCRXJdeH2W'},
                                        {'name':'aburrido', 'file':'1WthGauiCsrMYnGqxU0U_a76fTm38N7cr'},
                                        {'name':'accidente', 'file':'1A5iqD-_Ye8OfHB8ShdW25l6xjxi_uN3v'},
                                        {'name':'adentro', 'file':'1HSL8cMBg6i0MYvwsM7xGCAGWSVNUjFnF'},
                                        {'name':'afortunado', 'file':'1EZMASe09g9KYkJLd9ORHP-t0v4RHnI2_'},
                                        {'name':'alegre divertido', 'file':'1bxHG4-qMxmfaUtRdWWfiDuQ8P4pzvobN'},
                                        {'name':'algunos', 'file':'1H-PlVeB5RktuJrN0BF3pTHcSnpDKdDv9'},
                                        {'name':'alto estatura', 'file':'1WuIyds3NyPC3s0QSi__N6NKJUJJ-3a1B'},
                                        {'name':'amable', 'file':'1kUlTtfLcOHk21kEbv_OmCmkRzotaOv-u'}
  ]},
  {'name':'preposiciones2', 'words':[
                                        {'name':'antes', 'file':'1AT5YwJtEG0gCXtj49yIPEMLQVH30MJ9b'},
                                        {'name':'arriba', 'file':'1xcMQfxKXmkQxqjCNvchthQxLwEXBxYTl'},
                                        {'name':'asustado', 'file':'17ccpxzNtbft19JA1n2Eci9vbPocZhvTV'},
                                        {'name':'atencion atento', 'file':'1zrFW_P0zmhUYAP1HtED3ESjDhcLsLkug'},
                                        {'name':'baboso', 'file':'1ZfK_8JueCp3IqshlGngodwIImxn8S6Ci'},
                                        {'name':'bonito', 'file':'17rsyZMkRWKaA7txv-u8j3ylPw5OmH20i'},
                                        {'name':'broma', 'file':'1FiamrKkXhL_V9ISAODiTPok9RwiSGdVz'},
                                        {'name':'bueno', 'file':'16STInDRuLaDiElOsJ6W_p4mkCv_MHgpt'},
                                        {'name':'cada', 'file':'1_jHteCbQLMxdPbyDk_xM4qExL9g5U5RP'}
  ]},
  {'name':'preposiciones3', 'words':[
                                        {'name':'caliente', 'file':'1xd8-mGp-ikEOQvFzO_E6O_TC3nf5lQrq'},
                                        {'name':'cansado', 'file':'1d_t6pADthXPYyVnrsOuvfaPVByX0xGnI'},
                                        {'name':'carino', 'file':'1dsBV34CIQG0fnL7OUaHnNNRlt5HkKnN0'},
                                        {'name':'celoso', 'file':'1igPEHfUlFHuzJj6Y2Z2il_ubGpeRUhIo'},
                                        {'name':'chaparro', 'file':'17F_tzdln6lqmyuOEBAMCUMhdEEhnlx8a'},
                                        {'name':'chistoso', 'file':'1cq5rhwtNWR2ljC9GiiceczxUL0b8tauF'},
                                        {'name':'cobarde', 'file':'1D61Q_YM206AMiovoY3iJBAlNBfSus9Bp'},
                                        {'name':'contento', 'file':'1V6VOXvlClPWJaHKa1fXtwfMLCF2xOw2Z'},
                                        {'name':'curioso', 'file':'1fgvcsQozxzHvsjoG0odkDJB_oEoIK5Ax'}
  ]},
  {'name':'preposiciones4', 'words':[
                                        {'name':'debil', 'file':'1gtzLCxMobSIim5L8VlxNEklSCPe4tSUm'},
                                        {'name':'decente', 'file':'1iBLnBfG3jwYxBbdePkvecxlUOqKirYUh'},
                                        {'name':'delgado', 'file':'179QcN83CgFTIDOW3plWGXvb5UGbJ4sD4'},
                                        {'name':'despacio', 'file':'1HDiNOnP_fKzuWddBXiJLafJQfva_BVFl'},
                                        {'name':'diferente', 'file':'1fwjznopswbFUHAnWYzIZXIE1TPIPPWkp'},
                                        {'name':'dificil', 'file':'1q5GQFiJdwIb2z7V8BZjVjOunlb-_53nF'},
                                        {'name':'diploma', 'file':'1vKCY_Rowa1YwDpA40PHPPScc2Ov0PSCi'},
                                        {'name':'duda', 'file':'18r56BDPlnkQM1NIkRLJnCefhuOOXS8xd'},
                                        {'name':'egoista', 'file':'17iSK6tG05pQgUD8pbhyFDo4C4jrpoDBz'}
  ]},
  {'name':'preposiciones5', 'words':[
                                        {'name':'ejemplo', 'file':'1l53JpwChIaZFDGUMLLnX9L4D36AaVVS8'},
                                        {'name':'ejercicio', 'file':'1GS3oRr1egeGDaxaZHgpRBAfTuv-XNq3a'},
                                        {'name':'enojado', 'file':'1W-XAqB9Y7_5YAL4uUwe4-1yH-hLNhFuh'},
                                        {'name':'envidia', 'file':'1J7tvRv1feAbB6bQCx8XG0l2EbHT-4Xbz'},
                                        {'name':'especial', 'file':'1Ye9lRSy1BG2hWGT299u9z-l7tKXhCwRt'},
                                        {'name':'facil', 'file':'1Vn7cf-sSbxTvQ6EMEXbJOKsX5ahZzTrS
                                        {'name':'falso', 'file':'1k8YXhkBZ4JMUbJkplFwLw2e-Wjo9Dl1n'},
                                        {'name':'feliz', 'file':'1qdioiY_YhDxSedckUXcTJLiflq54nRw3'},
                                        {'name':'feo', 'file':'1QvLD7bbYOV_0wIe5mEcgj5Fer0Jj2quO'}
  ]},
  {'name':'preposiciones6', 'words':[
                                        {'name':'flojo', 'file':'1isBRMaq4R9RPPDGM4lV22QSKStwzs01S'},
                                        {'name':'fuerte', 'file':'1JFXe_iKqzOV0ZgJiVoJlFvVjfvFSKZ0m'},
                                        {'name':'fuerza', 'file':'1SgvShY5VF82Ugtf99a4SdDLhofB6bipf'},
                                        {'name':'gordo', 'file':'1TD2dXutm5tVCxBF1YTihjDgIkdrPxTOA'},
                                        {'name':'gratis', 'file':'1ZOiFVyhP4gC2qcZxZ_4NHLwGrDC9jW4s'},
                                        {'name':'grosero', 'file':'1pBqbgEwe9cG_zehQcgdc9xw7VGMR2B2N'},
                                        {'name':'guapo', 'file':'1hEAZJYogNuX3vV60ZlMlAB5vT_culQEZ'},
                                        {'name':'hambre', 'file':'1v2uO3z3aUAdgkd2i5WZ76pHxustLA027'},
                                        {'name':'historia', 'file':'1VHEjZgbY8Vy51zxdxTkPh23pLaXBZ39p'}
  ]},
  {'name':'preposiciones7', 'words':[
                                        {'name':'humilde', 'file':'1eN1nZ8uLtncWQQOaj4aXkJCI7W59fe4_'},
                                        {'name':'importante', 'file':'1o9-x0-GWB9u7lhQ4vM3R7pddPw4R8vSE'},
                                        {'name':'inteligente', 'file':'1ect02AwpEIwiaEHKj3zhRouRIfsi8LHM'},
                                        {'name':'jamas', 'file':'12bJ27VMy8gN2nWMUxT_Ln7L_lUN_Fw0c'},
                                        {'name':'junta', 'file':'1fRjJAHwAx-yh-TfSAeDoNk3qR-U5JjAU'},
                                        {'name':'junto', 'file':'1-vqnNC4enoniOvMmkzqxu-SkddjP78Vx'},
                                        {'name':'lejos', 'file':'17YoVA3RVj5pLaOKEGqR9hdu0yvS1fkUw'},
                                        {'name':'libre', 'file':'1YMl4gf9uQzDAIlPkSxMgciLQj46JtMf8'},
                                        {'name':'loco', 'file':'12OJM5e1JJrQjBZO29okXzK0JXEBJ8I6R'}
  ]},
  {'name':'preposiciones8', 'words':[
                                        {'name':'lsm', 'file':'1dyIeuHpicUjHO3O8LuDLjRKwZTtobB-A'},
                                        {'name':'malo', 'file':'1UpWvJ7UmPPF6v6vkcE-2csytw4g3N4EH'},
                                        {'name':'mas', 'file':'1xqi0j9dyfqsDOlXlVnA4FZjpUmVgt5fz'},
                                        {'name':'mejor', 'file':'1pNDcI2mg5pbU2sC9Qm7zn-_1KqboiEPx'},
                                        {'name':'miedo', 'file':'1DMcNWgVWXJ11w8HBD7A2mLsjylUWhaTi'},
                                        {'name':'necio', 'file':'10KykUFtY-yebnXKwfFI4Jb6U94bEWB8l'},
                                        {'name':'no', 'file':'1Y5MLmGi_8Dhv6yApsPs6-BWkODv39Vek'},
                                        {'name':'nuevo', 'file':'19IH4U-dlTt7G2VoJIxTy9-qPzEzA0Hwy'},
                                        {'name':'nunca', 'file':'1KWRgC9ModW14glzhh456QbUdnmtoPUBU'}
  ]},
  {'name':'preposiciones9', 'words':[
                                        {'name':'ojala', 'file':'19uR51zBEK-0vK4X0p6iDK1nhaEQKlwoh'},
                                        {'name':'paciencia', 'file':'1m3ewZC_gg-MeTC3DR3O0ZW1Iv490GqIy'},
                                        {'name':'peor', 'file':'1G-a43lMMdaMPKAfLaAFywjEz6srWFDr0'},
                                        {'name':'pero', 'file':'1B12wEe1QyH21UwlAcFjE8AD8F5-67dt8'},
                                        {'name':'pobre', 'file':'1FS6yknoK6ft7MOyIMJQmFh0jruNTG3HU'},
                                        {'name':'presumido', 'file':'1o3cbZzlMtm0iVjVSDtQPGKd4_IEq5hbp'},
                                        {'name':'problema', 'file':'1iAHMpERA7_dseLqjqSBdKPKHc2f4S10G'},
                                        {'name':'rapido pronto', 'file':'1y2MjPzQFqjvHr4Cv9OTh-jBZrSuqJecS'},
                                        {'name':'raro', 'file':'1d6nHGX5l1c2lVW-OUQ3EL5q04xsDtdgO'}
  ]},
  {'name':'preposiciones10', 'words':[
                                        {'name':'secreto', 'file':'1xmEVZVmxpWqRne3y86yxEoNQPC7mKt_h'},
                                        {'name':'sena propia', 'file':'1XMKCWXI1Ow41Gw5KMJeblP00kjzxkVcA'},
                                        {'name':'senas', 'file':'12T3Qsxdn3IpUZLd7sPCj7Ym2OMQVwCIG'},
                                        {'name':'si', 'file':'1Avo9ZeNYLJfcKUQ-GeYkp9FygQ7qadf7'},
                                        {'name':'sucio', 'file':'1K9qeygejb0yh3vqERWCy95YjOeT7m6Ug'},
                                        {'name':'suerte', 'file':'1TNSlUhKCPzDjNvXsdVZDmn15RuQ0EVFS'}
  ]},
  {'name':'preposiciones11', 'words':[
                                        {'name':'todo', 'file':'1KQkq4oZ6u2lDjpeMT3Do0E5g21m93ub4'},
                                        {'name':'tonto', 'file':'1JzDFM9l_l7-1zZGKwxKDXKF3gw8woyS-'},
                                        {'name':'travieso', 'file':'1_10NsKrjoxj-3Fhd2l1__3EYCALg-6QA'},
                                        {'name':'triste', 'file':'1KwVR_g5Wide_YKJzG6TUDxubA0AomkMr'},
                                        {'name':'verdad', 'file':'1oiE7UPduyJKmoDRcdwLQem-AN8ryZ_BP'},
                                        {'name':'verguenza', 'file':'1-VsRJfdokJsOIkPJ50tz_hNt2zqPp6iO'} ]}
])

'''
