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
import random

app = Flask(__name__) #inicializamos la app
CORS(app) # se ocupa por ahora

load_dotenv() # cargamos las variables de entorno


DBpassword = os.getenv("PASSWORD_MONDOGO")
DBuser = os.getenv("USER_MONDOGO")
DataBase = os.getenv("DATABASE_MONDOGO")
Cluster = os.getenv("CLUSTER_MONDOGO")

#=====Conexión a la base de datos=======
app.config['MONGO_URI'] = 'mongodb+srv://'+DBuser+':'+DBpassword+'@cluster0.'+Cluster+'.mongodb.net/'+DataBase
mongo = PyMongo(app) #mongo es nuestra base de datos (mongo.db)
#=======================================


#------------------------------SIGN UP USER----------------------------------
#falta cifrar datos sensibles como password y correo
@app.route('/user/signup', methods=['POST'])
def create_user():
    '''
    {
    "username":"Leopoldo",
    "password": "123",
    "email": "Leopoldo@mail.com"
    }
    '''
    #{"username":nombre,"password":pass,"email":mail,"type":0,}
    json = request.json
    # si encuentra un usuario con ese username manda error
    if mongo.db.users.find_one({'username':json['username']}) != None:
        return {'msj':'ya existe este username','ERROR': 'si'}
    # si encuentro un usuario con este email mando error
    if mongo.db.users.find_one({'email':json['email'].lower()}) != None:
        return {'msj':'ya esta en uso este correo','ERROR': 'si'}
    
    
    if json['username'] and json['password'] and json['email'] and (json['username'] != "") and (json['password'] != "") and (json['email'] != ""):
        json['email'] = json['email'].lower() # ponemos el mail en minusculas
        json["grades"] = {
            "verboscomunes1":   0,
            "verboscomunes2":   0,
            "verboscomunes3":   0,
            "verboscomunes4":   0,
            "letras1":          0,
            "letras2":          0,
            "letras3":          0,
            "verbosnarrativos1":0,
            "verbosnarrativos2":0,
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
        json["type"] = 0 # es usuario normal
        json['group'] = ''
        id = mongo.db.users.insert_one(json)
        json['_id'] = str(id.inserted_id)
        return {'msj': 'usuario guardado','ERROR':'no'} # mensaje de exito 
    else:
        return {'msj':'falta un campo','ERROR': 'si'} # mensaje de error 
#=====================================================================================================

#-----------------------------LOGIN---------------------------------------
#falta cifrado de la contraseña para comparar contraseña cifrada con no cifrada
@app.route('/user/login', methods=['POST'])
def login():
    # recibe usuario/correo y contraseña en un json asi 
    # {"username":usuario/correo,, "password": contraseña}
    json = request.json
    #reviso si el usuario puso su username o su correo
    if "@" in json['username']: #es un correo
        data = mongo.db.users.find_one({'email':json['username'].lower(), 'password': json['password']},{'_id':1,'username':1,'email':1,'group':1,'type':1})
    else:
        data = mongo.db.users.find_one({'username':json['username'], 'password': json['password']},{'_id':1,'username':1,'email':1,'group':1,'type':1})

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
            'type': data['type'], # 1 admin,   0 normal
            'group': data['group']
        }
        return r
    #regresa el siguiente json {"_id":string, "username": string, "email": string, "type": bool}
    #si el usuario tiene grupo regresa
    #{"_id":string, "username": string, "email": string, "type": bool, "group":string}
#=========================================================================    

#-------------------------------Join Group---------------------------------
@app.route('/user/joinGroup', methods=['POST'])
def joinGroup():
    #{_id:"636c330384831804d80d0283, groupCode: "vVlkLalskcjhlk12csda81"}
    json = request.json
    grupo = mongo.db.groups.find_one({'code': json['groupCode']})
    if grupo == None:
        return {"msj": "ERROR Codigo invalido"}
    
    id = json['_id']
    objId = ObjectId(id)
    
    user = mongo.db.users.find_one({"_id":objId},{"group":1})
    
    if "group" in user: # si ya estas en un grupo no te dejara unirte a otro
        return {"msj": "ERROR ya estas en un grupo"}

    # si no estas en un grupo, te mete a el
    mongo.db.users.update_one(
        {"_id":objId},
        {"$set":{"group":grupo["name"]}}, 
        upsert = False)
    
    return {"msj":"te uniste al grupo"}
#=========================================================================    

#----------------------------leave group----------------------------------
@app.route('/user/leaveGroup', methods=['POST'])
def leaveGroup():
    #{"_id":636c330384831804d80d0283}
    id = request.json["_id"]
    objInstance = ObjectId(id)
    mongo.db.users.update_one(
        {"_id":objInstance},
        {"$unset":{"group":1}}
        )
    return {"msj":"te saliste del grupo"}
#=========================================================================    

#--------------------Mostrar grades para niveles-----------------------
@app.route('/user/grades', methods=['POST'])
def checkGrades():
    #{username:leo, _id: 12312412414}
    json = request.json
    
    objInstance = ObjectId(json['_id'])

    data = mongo.db.users.find_one({'_id':objInstance},{'grades':1})
    return data["grades"]
#========================================================================

#--------------------------Actualizar calificacion----------------------
@app.route('/user/setGrade', methods=['POST'])
def setGrade():
    #{_id:13325fdsf, categorie:letras1, grade:90}
    json = request.json
    id = json["_id"]
    objId = ObjectId(id)
    
    mongo.db.users.update_one({"_id":objId},
                              {"$set":
                                  {f'grades.{json["categorie"]}':json["grade"]}
                                })
    return {"msj": f'calificación de {json["categorie"]} actualizada a {json["grade"]}'}
#=======================================================================

#----------------------Numero de niveles arriba de 70-------------------
#=======================================================================


#=========================================================================
#===================          CATEGORIES          ========================
#=========================================================================
#=========================================================================
#----------------mostrar todas las palabras--------------
@app.route('/categories/all/<categorie>', methods=['GET'])
def showCategories(categorie):
    # muestra todas las palabras de una categoria completa, ignorando el numero del nivel de categoria
    # por ejemplo, /categories/all/verboscomunes regresa todas las palabras de verboscomunes 1, 2 ,3 y 4 
    datas = mongo.db.categories.find({"name":{'$regex':f'^{categorie}'}},{"words":1})
    r = []
    for data in datas:
        for word in data["words"]:
            r.append(word["name"])    
    return r
#========================================================================

#----------------mostrar palabras de una categoria-----------------------
@app.route('/categories/words/<categorie>',methods=['GET'])
def getWords(categorie):
    datas = mongo.db.categories.find_one({"name":categorie})["words"]
    return datas
#========================================================================
  
#---------------------Crear un quiz-------------------------------------
@app.route('/quiz/<categorie>',methods=['GET'])
def createQuiz(categorie):
    words = getWords(categorie)

    quiz = []
    for x in range(len(words)):
        pregutna = {}
        pregutna["file"] = words[x]["file"]
        pregutna["answer"] = words[x]["name"]
        
        pregutna["options"] = []
        #metemos de forma random 3 respuestas incorrectas 
        posiblesOpciones = words.copy() # copias las palabras
        posiblesOpciones.pop(x) # eliminas la palabra que ya esta en la lista de opciones
        for _ in range(3):
            r = random.choice(posiblesOpciones)
            pregutna["options"].append(r["name"])
            posiblesOpciones.remove(r)
        random.shuffle(pregutna["options"])#revolvemos las respuestas

        quiz.append(pregutna)  

    response = {'results':quiz}       
    return response
#=======================================================================
    
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

'''