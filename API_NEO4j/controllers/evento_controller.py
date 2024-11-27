from flask import Blueprint, request, jsonify
from services.evento_service import EventoService
import datetime


evento_controller = Blueprint('evento_controller', __name__)

# Crear un nuevo evento
@evento_controller.route('/eventos', methods=['POST'])  
def crear_evento():
    datos = request.get_json()
    resultado = EventoService.crear_evento(datos)
    if "error" in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado), 201

# Listar todos los eventos
@evento_controller.route('/eventos', methods=['GET'])
def listar_eventos():
    """
    Endpoint para listar todos los eventos.
    """
    resultado = EventoService.listar_eventos()
    if "error" in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado), 200

# Obtener detalles de un evento por su ID
@evento_controller.route('/eventos/<idEvento>', methods=['GET'])
def obtener_evento_por_id(idEvento):
    """
    Controlador para obtener un evento por su ID.
    """
    resultado = EventoService.obtener_evento_por_id(int(idEvento))  # Asegúrate de convertir a entero si es necesario
    if "error" in resultado:
        return jsonify(resultado), 404
    return jsonify(resultado), 200


# Actualizar información de un evento
@evento_controller.route('/eventos/<idEvento>', methods=['PUT'])
def actualizar_evento(idEvento):
    datos = request.get_json()
    resultado = EventoService.actualizar_evento(idEvento, datos)
    if "error" in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado), 200

# Eliminar un evento
@evento_controller.route('/eventos/<idEvento>', methods=['DELETE'])
def eliminar_evento(idEvento):
    resultado = EventoService.eliminar_evento(idEvento)
    if "error" in resultado:
        return jsonify(resultado), 400
    return jsonify(resultado), 200

# Registrar a una persona como asistente a un evento
@evento_controller.route('/eventos/<idEvento>/asistentes', methods=['POST'])
def registrar_asistente(idEvento):
    try:
        datos = request.get_json()
        idPersona = datos.get("idPersona")
        if not idPersona:
            return jsonify({"error": "Se requiere idPersona"}), 400
        
        resultado = EventoService.registrar_asistente(idEvento, idPersona)
        
        if "error" in resultado:
            return jsonify(resultado), 400
            
        return jsonify({"mensaje": "Asistente registrado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Obtener la lista de asistentes a un evento
@evento_controller.route('/eventos/<idEvento>/asistentes', methods=['GET'])
def listar_asistentes(idEvento):
    try:
        resultado = EventoService.listar_asistentes(idEvento) 
        if isinstance(resultado, dict) and "error" in resultado:
            return jsonify(resultado), 400
        return jsonify({"asistentes": resultado}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# Eliminar a un asistente de un evento
@evento_controller.route('/eventos/<idEvento>/asistentes/<idPersona>', methods=['DELETE'])
def eliminar_asistente(idEvento, idPersona):
    """
    Endpoint para eliminar un asistente de un evento.

    Args:
        idEvento (str): ID del evento en la URL.
        idPersona (str): ID de la persona en la URL. 

    Returns:
        JSON: Resultado de la operación.
    """
    try:
        resultado = EventoService.eliminar_asistente(idEvento, idPersona)
        
        if isinstance(resultado, dict) and "error" in resultado:
            return jsonify(resultado), 404
            
        # Verificar si se eliminó alguna relación
        if isinstance(resultado, list) and len(resultado) > 0:
            if resultado[0].get('eliminado', 0) > 0:
                return jsonify({"mensaje": "Asistente eliminado exitosamente"}), 200
            
        return jsonify({"error": "No se encontró la relación"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Asociar un interés con un evento
@evento_controller.route('/eventos/<int:idEvento>/intereses', methods=['POST'])
def asociar_interes_evento(idEvento):
    """
    Asociar un interés con un evento.
    """
    try:
        datos = request.get_json()
        if not datos or 'nombreInteres' not in datos:
            return jsonify({"error": "Se requiere el campo 'nombreInteres'"}), 400

        nombreInteres = datos.get("nombreInteres")
        if not nombreInteres or not isinstance(nombreInteres, str):
            return jsonify({"error": "El nombre del interés debe ser una cadena válida"}), 400

        resultado = EventoService.asociar_interes_evento(idEvento, nombreInteres)
        
        if "error" in resultado:
            return jsonify(resultado), 400

        return jsonify(resultado), 201

    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500