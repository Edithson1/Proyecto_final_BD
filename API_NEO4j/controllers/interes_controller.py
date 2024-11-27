from flask import Blueprint, request, jsonify
from services.interes_service import InteresService

interes_controller = Blueprint('interes_controller', __name__)

# Listar todos los intereses
@interes_controller.route('/intereses', methods=['GET'])
def listar_intereses():
    resultado = InteresService.listar_intereses()
    if "error" in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado), 200

# Asociar un interés con una persona
@interes_controller.route('/personas/<idPersona>/intereses', methods=['POST'])
def asociar_interes_persona(idPersona):
    datos = request.get_json()
    nombreInteres = datos.get("nombreInteres")
    resultado = InteresService.asociar_interes_persona(idPersona, nombreInteres)
    if "error" in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado), 201

# Eliminar un interés asociado a una persona
@interes_controller.route('/personas/<idPersona>/intereses/<nombreInteres>', methods=['DELETE'])
def eliminar_interes_persona(idPersona, nombreInteres):
    resultado = InteresService.eliminar_interes_persona(idPersona, nombreInteres)
    if "error" in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado), 200

# Obtener los intereses asociados a una persona
@interes_controller.route('/personas/<idPersona>/intereses', methods=['GET'])
def obtener_intereses_persona(idPersona):
    resultado = InteresService.obtener_intereses_persona(idPersona)
    if "error" in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado), 200

# Asociar un interés con una publicación
@interes_controller.route('/publicaciones/<idPublicacion>/intereses', methods=['POST'])
def asociar_interes_publicacion(idPublicacion):
    datos = request.get_json()
    nombreInteres = datos.get("nombreInteres")
    resultado = InteresService.asociar_interes_publicacion(idPublicacion, nombreInteres)
    if "error" in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado), 201

# Eliminar un interés asociado a una publicación
@interes_controller.route('/publicaciones/<idPublicacion>/intereses/<nombreInteres>', methods=['DELETE'])
def eliminar_interes_publicacion(idPublicacion, nombreInteres):
    resultado = InteresService.eliminar_interes_publicacion(idPublicacion, nombreInteres)
    if "error" in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado), 200
