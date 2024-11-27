from flask import Blueprint, request, jsonify
from services.group_service import GroupService

group_controller = Blueprint('group_controller', __name__)

@group_controller.route('/grupos/registro', methods=['POST'])
def crear_grupo():
    # Intentar obtener datos del body JSON
    data = request.json or {}
    
    # Si no hay datos en el body, usar query params
    if not data:
        data = request.args.to_dict()
    
    # Validar que tengamos los campos requeridos
    required_fields = ['idGrupo', 'nombreGrupo']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    # Convertir idGrupo a entero si viene como string
    if 'idGrupo' in data:
        data['idGrupo'] = int(data['idGrupo'])

    resultado = GroupService.crear_grupo(data)
    return jsonify(resultado), 201

@group_controller.route('/grupos', methods=['GET'])
def listar_grupos():
    filtros = request.args.to_dict()
    grupos = GroupService.listar_grupos(filtros)
    return jsonify(grupos), 200

@group_controller.route('/grupos/<int:idGrupo>', methods=['GET'])
def obtener_grupo(idGrupo):
    resultado = GroupService.obtener_grupo(idGrupo)
    return jsonify(resultado), 200

@group_controller.route('/grupos/<int:idGrupo>', methods=['PUT'])
def actualizar_grupo(idGrupo):
    data = request.json
    resultado = GroupService.actualizar_grupo(idGrupo, data)
    return jsonify(resultado)

@group_controller.route('/grupos/<int:idGrupo>', methods=['DELETE'])
def eliminar_grupo(idGrupo):
    resultado = GroupService.eliminar_grupo(idGrupo)
    return jsonify(resultado)

@group_controller.route('/grupos/<int:idGrupo>/miembros/<int:idUsuario>', methods=['POST'])
def agregar_miembro(idGrupo, idUsuario):
    resultado = GroupService.agregar_miembro(idGrupo, idUsuario)
    return jsonify(resultado)

@group_controller.route('/grupos/<int:idGrupo>/miembros/<int:idUsuario>', methods=['DELETE'])
def eliminar_miembro(idGrupo, idUsuario):
    resultado = GroupService.eliminar_miembro(idGrupo, idUsuario)
    return jsonify(resultado)

@group_controller.route('/grupos/<int:idGrupo>/miembros', methods=['GET'])
def listar_miembros(idGrupo):
    miembros = GroupService.listar_miembros(idGrupo)
    return jsonify(miembros)

@group_controller.route('/grupos/<int:idGrupo>/creador/<int:idUsuario>', methods=['POST'])
def establecer_creador(idGrupo, idUsuario):
    resultado = GroupService.establecer_creador(idGrupo, idUsuario)
    return jsonify(resultado)
