# API Para la aplicación signa de lenguaje de señas
'''
pasos:
    python -m venv venv            creamos entorno virtual
    venv\Scripts\activate          
    pip install <lo que se deba instalar>
    python src/api.py              corremos la api estando en la carpeta API
'''

# pip install flask          Componente basico 
# pip install pymongo        
# pip install flask-pymongo 
# pip install flask-cors
# pip install python-dotenv  Para el archivo .env

from dotenv import load_dotenv
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def chequeo():
    return "<p>Hola mundo</p>"


if __name__ == "__main__":
    app.run(debug=True)
