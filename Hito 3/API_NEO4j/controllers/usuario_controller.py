"""
Controlador que maneja las rutas HTTP para la API de usuarios.
Define los endpoints y procesa las peticiones HTTP.
"""

from flask import Blueprint, request, jsonify
from services.usuario_service import UsuarioService

usuario_bp = Blueprint('usuario', __name__)

# Crear un usuario
@usuario_bp.route('/usuarios/registro', methods=['POST'])
def registrar_usuario():
    """
    Endpoint para registrar un nuevo usuario.
    
    Query Params:
        idPersona (int): ID único del usuario
    
    Returns:
        JSON: Resultado de la operación y código HTTP
    """
    id_persona = request.args.get('idPersona')

    # Validar que se haya proporcionado idPersona
    if not id_persona:
        return {"error": "Debe proporcionar un idPersona para registrar el usuario."}, 400

    try:
        id_persona = int(id_persona)  # Convertir a entero si es necesario
    except ValueError:
        return {"error": "idPersona debe ser un número entero."}, 400

    # Crear el usuario
    result = UsuarioService.crear_usuario({"idPersona": id_persona})
    return jsonify(result), 201

# Obtener detalles de un usuario
@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    result = UsuarioService.obtener_usuario(id)
    return jsonify(result), 200

# Actualizar un usuario
@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    # Intentar obtener datos del cuerpo de la solicitud
    data = request.get_json(silent=True) or {}
    
    # Obtener todos los query parameters
    query_params = {}
    for key, value in request.args.items():
        if key == 'idPersona':
            try:
                query_params[key] = int(value)
            except ValueError:
                return {"error": "idPersona debe ser un número entero."}, 400
        else:
            query_params[key] = value
    
    # Combinar datos del body y query parameters
    data.update(query_params)

    # Validar que se proporcionen datos para actualizar
    if not data:
        return {"error": "Debe proporcionar al menos un dato para actualizar."}, 400

    # Llamar al servicio para actualizar el usuario
    result = UsuarioService.actualizar_usuario(id, data)
    return jsonify(result), 200

# Eliminar un usuario
@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    result = UsuarioService.eliminar_usuario(id)
    return jsonify(result), 200

# Listar seguidores de un usuario
@usuario_bp.route('/usuarios/<int:id>/seguidores', methods=['GET'])
def listar_seguidores(id):
    result = UsuarioService.listar_seguidores(id)
    return jsonify(result), 200

# Listar usuarios seguidos
@usuario_bp.route('/usuarios/<int:id>/seguidos', methods=['GET'])
def listar_seguidos(id):
    result = UsuarioService.listar_seguidos(id)
    return jsonify(result), 200

# Seguir a un usuario
@usuario_bp.route('/usuarios/<int:id>/seguir/<int:id_seguir>', methods=['POST'])
def seguir_usuario(id, id_seguir):
    result = UsuarioService.seguir_usuario(id, id_seguir)
    return jsonify(result), 201

# Dejar de seguir a un usuario
@usuario_bp.route('/usuarios/<int:id>/seguir/<int:id_seguir>', methods=['DELETE'])
def dejar_de_seguir_usuario(id, id_seguir):
    result = UsuarioService.dejar_de_seguir_usuario(id, id_seguir)
    return jsonify(result), 200