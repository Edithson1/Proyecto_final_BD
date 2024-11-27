from flask import Blueprint, request, jsonify
from services.publication_service import PublicationService

publication_controller = Blueprint('publication_controller', __name__)

@publication_controller.route('/publicaciones/registro', methods=['POST'])
def crear_publicacion():
    data = request.json
    resultado = PublicationService.crear_publicacion(data)
    return jsonify(resultado), 201

@publication_controller.route('/publicaciones', methods=['GET'])
def listar_publicaciones():
    filtros = request.args.to_dict()
    publicaciones = PublicationService.listar_publicaciones(filtros)
    return jsonify(publicaciones), 200

@publication_controller.route('/publicaciones/<idPublicacion>', methods=['GET'])
def obtener_publicacion(idPublicacion):
    publicacion = PublicationService.obtener_publicacion(idPublicacion)
    if publicacion:
        return jsonify(publicacion), 200
    return jsonify({"error": "Publicación no encontrada"}), 404

@publication_controller.route('/publicaciones/<idPublicacion>', methods=['PUT'])
def actualizar_publicacion(idPublicacion):
    data = request.json
    resultado = PublicationService.actualizar_publicacion(idPublicacion, data)
    return jsonify(resultado)

@publication_controller.route('/publicaciones/<idPublicacion>', methods=['DELETE'])
def eliminar_publicacion(idPublicacion):
    resultado = PublicationService.eliminar_publicacion(idPublicacion)
    return jsonify(resultado)

@publication_controller.route('/publicaciones/<idPublicacion>/reacciones', methods=['POST'])
def agregar_reaccion(idPublicacion):
    data = request.json
    if not all(k in data for k in ("idPersona", "tipoReaccion")):
        return jsonify({"error": "Faltan campos requeridos: 'idPersona' y 'tipoReaccion'."}), 400
    resultado = PublicationService.agregar_reaccion(idPublicacion, data)
    if "error" in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado), 201

@publication_controller.route('/publicaciones/<idPublicacion>/reacciones', methods=['GET'])
def listar_reacciones(idPublicacion):
    reacciones = PublicationService.listar_reacciones(idPublicacion)
    if isinstance(reacciones, dict) and "error" in reacciones:
        return jsonify(reacciones), 500
    return jsonify(reacciones), 200

@publication_controller.route('/publicaciones/<idPublicacion>/reacciones', methods=['DELETE'])
def eliminar_reaccion(idPublicacion):
    data = request.json
    if 'idPersona' not in data:
        return jsonify({"error": "Falta el campo requerido: 'idPersona'."}), 400
    resultado = PublicationService.eliminar_reaccion(idPublicacion, data)
    if "error" in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado), 200

@publication_controller.route('/publicaciones/<idPublicacion>/comentarios', methods=['POST'])
def agregar_comentario(idPublicacion):
    data = request.json

    # Validar campos requeridos
    if not all(k in data for k in ("idPersona", "texto")):
        return jsonify({"error": "Faltan campos requeridos: 'idPersona' y 'texto'."}), 400

    # Llamar al servicio
    resultado = PublicationService.agregar_comentario(idPublicacion, data)
    if "error" in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado), 201

@publication_controller.route('/comentarios/<idComentario>', methods=['DELETE'])
def eliminar_comentario(idComentario):
    resultado = PublicationService.eliminar_comentario(idComentario)
    if "error" in resultado:
        return jsonify(resultado), 404
    return jsonify(resultado), 200



@publication_controller.route('/publicaciones/<idPublicacion>/comentarios', methods=['GET'])
def listar_comentarios_por_publicacion(idPublicacion):
    """
    Endpoint para listar comentarios relacionados con una publicación específica.

    Args:
        idPublicacion (str): ID de la publicación en la URL.

    Returns:
        JSON: Lista de comentarios o un mensaje de error.
    """
    resultado = PublicationService.listar_comentarios_por_publicacion(idPublicacion)
    if "error" in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado), 200

@publication_controller.route('/publicaciones/<idPublicacion>/intereses', methods=['GET'])
def listar_intereses_por_publicacion(idPublicacion):
    """
    Endpoint para listar los intereses relacionados con una publicación.

    Args:
        idPublicacion (str): ID de la publicación en la URL.

    Returns:
        JSON: Lista de intereses o un mensaje de error.
    """
    resultado = PublicationService.listar_intereses_por_publicacion(idPublicacion)
    if "error" in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado), 200
