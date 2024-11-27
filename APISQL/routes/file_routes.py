from flask import Blueprint, request, jsonify, session, redirect, render_template, url_for, current_app
from werkzeug.security import check_password_hash
from services.auth_service import save_user, get_users, update_user_data
from services.files_service import obtener_publicaciones_usuario, guardar_publicacion, obtener_publicaciones_de_otros
from flask import Blueprint, request, render_template
from werkzeug.utils import secure_filename
import os
from os import path
import ast
from utils.db import get_connection


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

file_bp = Blueprint('files', __name__)



# Función para verificar si el archivo tiene una extensión válida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@file_bp.route('/guardar-foto', methods=['POST'])
def registarArchivo():
    if 'idPersona' not in session:
        return jsonify({"error": "No session found. Please login."}), 401

    id_persona = session['idPersona']

    if 'archivo' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['archivo']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        try:
            file.save(upload_path)
        except Exception as e:
            return jsonify({"error": f"Error al guardar el archivo: {str(e)}"}), 500

        # Obtén la descripción del formulario
        description = request.form.get('descripcion', '')  # Si no hay descripción, queda vacía
        tipo_formato = 'imagen'

        try:
            resultado = guardar_publicacion(filename, tipo_formato, description, id_persona)
            if resultado:
                return jsonify({"message": "Publicación guardada con éxito", "file": filename, "descripcion": description}), 200
            else:
                return jsonify({"error": "Error al guardar la publicación en la base de datos"}), 500
        except Exception as e:
            return jsonify({"error": f"Error interno: {str(e)}"}), 500

    return jsonify({"error": "Formato de archivo no permitido"}), 400


@file_bp.route('/upload')
def upload():
    return render_template("upload_image.html")

@file_bp.route('/subir', methods=['POST']) #subir foto de perfil
def subir():
    if 'image' in request.files:
        image = request.files['image']
        image.save('static/uploads/pfp.jpg')
        return render_template('profile.html')
    return 'Error: No se ha enviado ninguna imagen.'
lista_archivos = []


@file_bp.route('/delete/<int:idPublicacion>', methods=['DELETE'])
def eliminar_publicacion(idPublicacion):
    if 'idPersona' not in session:
        return jsonify({"error": "No session found. Please login."}), 401  # Error si no hay sesión activa

    id_persona = session['idPersona']

    try:
        # Llamar al servicio para eliminar la publicación
        from services.files_service import eliminar_publicacion_usuario 
        resultado = eliminar_publicacion_usuario(idPublicacion, id_persona)

        if resultado:
            return jsonify({"message": "Publicación eliminada con éxito."}), 200
        else:
            return jsonify({"error": "Publicación no encontrada o no pertenece al usuario."}), 404

    except Exception as e:
        print("Error al eliminar la publicación:", e)
        return jsonify({"error": "Error interno del servidor."}), 500


@file_bp.route('/mis-publicaciones', methods=['GET'])
def obtener_publicaciones():
    if 'idPersona' not in session:
        return jsonify({"error": "No session found. Please login."}), 401

    # Obtener el idPersona de la sesión
    id_persona = session['idPersona']

    try:
        # Llamar a la función del servicio para obtener publicaciones
        publicaciones = obtener_publicaciones_usuario(id_persona)
        return jsonify({"publicaciones": publicaciones}), 200

    except Exception as e:
        print("Error al obtener las publicaciones:", e)
        return jsonify({"error": "Error al obtener las publicaciones."}), 500


@file_bp.route('/publicaciones-usuarios', methods=['GET'])
def obtener_publicaciones_usuarios():
    if 'idPersona' not in session:
        return jsonify({"error": "No session found. Please login."}), 401  # Error si no hay sesión activa

    id_persona_actual = session['idPersona']

    try:
        # Llamar al servicio para obtener publicaciones de otros usuarios
        publicaciones = obtener_publicaciones_de_otros(id_persona_actual)
        return jsonify({"publicaciones": publicaciones}), 200

    except Exception as e:
        print("Error al obtener publicaciones de otros usuarios:", e)
        return jsonify({"error": "Error interno del servidor."}), 500