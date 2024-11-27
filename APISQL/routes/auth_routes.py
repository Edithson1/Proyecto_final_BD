#Importamos flask así como tambien los servicios de autenticacion.
from flask import Blueprint, request, jsonify, session, redirect, render_template, url_for
from services.auth_service import save_user, get_users, update_user_data, login_user

#Definimos el Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Maneja la autenticación de usuario a través de la ruta /login.
    """
    if request.method == 'POST': 
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Llama a la función de autenticación
        user = login_user(username, password)
        if user:
            """
            Si el login es exitoso, devuelve un JSON con un mensaje de éxito 
            y el nombre del usuario
            """
            session['idPersona'] = user['idPersona']  # Almacenar el ID del usuario en la sesión
            return jsonify({"message": "Inicio de sesión exitoso", "username": username}), 200
        
        else:
            """
            Si el login falla, devuelve un JSON con un mensaje de error indicando que el usuario 
            o la contraseña son incorrectos.
            """
            error = "Usuario o contraseña incorrectos"
            return jsonify({"error": error}), 401


@auth_bp.route('/signup', methods=['GET', 'POST'])
def register():
    """
    Maneja el registro de nuevos usuarios a traves de la ruta /signup

    Metodos soportados:
       - GET: No realiza ninguna acción (puede ser utilizado para devolver una página de registro en el futuro)
       - POST: Procesa los datos enviados para registrar un nuevo usuario. 
    
    Flujo: 
       1. Verifica si la solicitud es de tipo POST
       2. Obtiene los datos enviados en el cuerpo de la solicitud como JSON.
       3. Extrae los campos requeridos para el registro del usuario
       4. Asigamos un valor por defecto a la biografia del usuario
       5. Intenta registrar al usuario llamado a la funcion 'save_user'
       6. Maneja los posibles errores durante el registro:
          - Devuelve un mensaje de exito si el registro es exitoso.
          - Devuelve un mensaje de error especifico si ocurre un 'ValueError'
          - Devuelve un mensaje de error generico si ocurre cualquier otro error.
          
    Returns:
       JSON con el resultado del registro:
          - 201 Created: Si el registro fue exitoso
          - 400 Bad Request: Si hubo un error con los datos enviados
          - 500 Internal Server Error: Si ocurrió un error inesperado en el servidor.
         
    """
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        mail = data.get('mail')
        name = data.get('name')
        bio = "En esta sección puedes escribir tu biografía"
        dob = data.get('dob')
        gender = data.get('gender')
        try:
            save_user(username, password, mail, name, bio, dob, gender)
            return jsonify({"message": "Usuario registrado exitosamente"}), 201
        except ValueError as ve: 
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": "Error interno del servidor"}), 500


@auth_bp.route("/user_settings", methods=['POST'])
def user_settings():
    """
    Maneja el registro de configuracion de un usuario a travez de la ruta /user_settings.

    Datos Requeridos:
        - 'username' (str): Nombre de usuario unico para identificar al usuario.
        - 'password' (str): Nueva contraseña del usuario.
        - 'bio' (str): Nueva biografica del usuario.

    Datos opcionales:
        - `mail` (str): Correo electrónico o número de teléfono del usuario.
        - `name` (str): Nombre completo del usuario. 


    """
    if request.method == 'POST':
        data = request.get_json()

        # Valida que los datos requeridos estén presentes
        username = data.get('username')
        password = data.get('password')
        mail = data.get('mail', None)  # Opcional
        name = data.get('name', None)  # Opcional
        bio = data.get('bio', None)  # Opcional

        if not username or not password or not bio:
            return jsonify({"error": "Faltan datos obligatorios: username, password o bio"}), 400

        try:
            update_user_data(username, password, mail, name, bio)
            return jsonify({"message": "Información actualizada exitosamente"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 404  # Usuario no encontrado
        except Exception as e:
            return jsonify({"error": "Error interno del servidor"}), 500
