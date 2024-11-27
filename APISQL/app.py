from flask import Flask
from routes.auth_routes import auth_bp
from flask import Flask, render_template, url_for, redirect, request, session, send_from_directory, jsonify
from routes.file_routes import file_bp 
from routes.person_routes import person_bp
from usuario_controller import usuario_bp # Si decides separar las rutas de gestión de archivos
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = '08f90b23a5d1616bf319bc298105da20'
liked = False

# Define el directorio donde se guardarán los archivos
UPLOAD_FOLDER = os.path.join('static', 'uploads')
# Verifica si la carpeta de uploads existe, y si no, créala
if not os.path.exists('static/uploads'):
    os.makedirs('static/uploads')

# Configura el UPLOAD_FOLDER en la aplicación principal
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Registrar blueprints
app.register_blueprint(usuario_bp, url_prefix= '/usuario')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(file_bp, url_prefix='/files') 
app.register_blueprint(person_bp,url_prefix= '/person') # Si defines rutas para archivos


@app.route('/')
def like():
    return 'Hola Mundo'


@app.route('/verificar_sesion', methods=['GET'])
def verificar_sesion():
    if 'idPersona' in session:
        return jsonify({"idPersona": session['idPersona']}), 200
    else:
        return jsonify({"error": "No hay sesión activa"}), 401 

if __name__ == '__main__':
    app.run(debug=True)
