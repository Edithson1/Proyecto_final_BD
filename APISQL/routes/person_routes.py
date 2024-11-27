from flask import Blueprint, request, jsonify, session, redirect, render_template, url_for, current_app
from werkzeug.security import check_password_hash
from services.auth_service import save_user, update_user_data
from services.files_service import obtener_publicaciones_usuario, guardar_publicacion
from services.person_service import obtener_usuarios_excluyendo
from services.mensajes_service import enviar_mensaje_y_obtener_chat, validar_amigos
from flask import Blueprint, request, render_template
from werkzeug.utils import secure_filename
import os
from os import path
import ast
from utils.db import get_connection

person_bp = Blueprint('person', __name__)
 

@person_bp.route('/usuarios-actuales', methods=['GET'])
def obtener_usuarios():
    if 'idPersona' not in session:
        return jsonify({"error": "No session found. Please login."}), 401  # Error si no hay sesión activa

    id_persona_actual = session['idPersona']

    try:
        # Llamar al servicio para obtener los usuarios excluyendo al actual
        usuarios = obtener_usuarios_excluyendo(id_persona_actual)
        return jsonify({"usuarios": usuarios}), 200

    except Exception as e:
        print("Error al obtener usuarios:", e)
        return jsonify({"error": "Error interno del servidor."}), 500


@person_bp.route('/mensajes/<int:receptor_id>', methods=['POST'])
def enviar_mensaje(receptor_id):


    # Verifica si hay una sesión activa
    if 'idPersona' not in session:
        return jsonify({"error": "No session found. Please login."}), 401

    # Obtener datos de la solicitud
    data = request.get_json()
    if not data or 'texto' not in data:
        return jsonify({"error": "Datos incompletos. Se requiere 'texto'."}), 400


    emisor_id = session['idPersona']  # ID del usuario autenticado
    texto = data['texto']

    try:
        # Verificar si los usuarios son amigos en Neo4j
        if not validar_amigos(emisor_id, receptor_id):
            return jsonify({"error": "No se puede enviar mensaje. No son amigos."}), 403

        # Registrar mensaje y obtener historial
        chat = enviar_mensaje_y_obtener_chat(emisor_id, receptor_id, texto)

        return jsonify({"chat": chat}), 200

    except Exception as e:
        print("Error al enviar mensaje:", str(e))
        return jsonify({"error": "Error interno del servidor."}), 500