from utils.neo4j_utils import crear_nodo, listar_nodos, obtener_nodo_por_id, actualizar_nodo, eliminar_nodo, gestionar_relacion, listar_relaciones
from neo4j.time import DateTime
from config.neo4j_driver import neo4j_driver

class EventoRepository:
    @staticmethod
    def _serializar_fecha_evento(data):
        """
        Función auxiliar para serializar fechas en eventos
        """
        if isinstance(data, list):
            return [{**item, 'fecha': item['fecha'].isoformat() if isinstance(item.get('fecha'), DateTime) else item.get('fecha')} for item in data]
        elif isinstance(data, dict):
            return {**data, 'fecha': data['fecha'].isoformat() if isinstance(data.get('fecha'), DateTime) else data.get('fecha')}
        return data

    @staticmethod
    def crear_evento(datos):
        return crear_nodo("Evento", datos)

    @staticmethod
    def listar_eventos():
        # Obtener eventos
        eventos = listar_nodos("Evento")
        
        # Convertir objetos DateTime a formato ISO 8601
        for evento in eventos:
            if "fecha" in evento and isinstance(evento["fecha"], DateTime):
                evento["fecha"] = evento["fecha"].isoformat()
        
        return eventos


    @staticmethod
    def obtener_evento_por_id(idEvento):
        """
        Obtener un evento por su ID utilizando la función reutilizable.
        """
        event_id = obtener_nodo_por_id("Evento", "idEvento", idEvento)
        
        # Convertir objetos DateTime a formato ISO 8601
        for event_id in event_id:
            if "fecha" in event_id and isinstance(event_id["fecha"], DateTime):
                event_id["fecha"] = event_id["fecha"].isoformat()

        return event_id


    @staticmethod
    def actualizar_evento(idEvento, nuevas_propiedades):
        """
        Repositorio para actualizar un evento en la base de datos Neo4j.
        """
        return actualizar_nodo(
            etiqueta="Evento",
            id_propiedad="idEvento",
            id_valor=idEvento,
            nuevas_propiedades=nuevas_propiedades
        )

    @staticmethod
    def eliminar_evento(idEvento):
        return eliminar_nodo("Evento", "idEvento", idEvento)

    @staticmethod
    def gestionar_relacion_evento_persona(idPersona, idEvento, tipo_relacion, accion):
        resultado = gestionar_relacion(
            etiqueta1="Persona",
            id_propiedad1="idPersona",
            id_valor1=idPersona,
            etiqueta2="Evento",
            id_propiedad2="idEvento",
            id_valor2=idEvento,
            tipo_relacion=tipo_relacion,
            accion=accion
        )
        return EventoRepository._serializar_fecha_evento(resultado)
        
        
    @staticmethod
    def listar_relaciones_evento_persona(idEvento, tipo_relacion):
        resultado = listar_relaciones(
            etiqueta1="Evento",
            id_propiedad1="idEvento",
            id_valor1=idEvento,
            tipo_relacion=tipo_relacion,
            etiqueta2="Persona",
            derecha=True
        )
        # Procesar el resultado para extraer los datos de las personas
        personas = []
        for record in resultado:
            if 'b' in record:  # 'b' es el alias usado en la consulta para las personas
                personas.append(record['b'])
        return personas 

    @staticmethod
    def eliminar_persona_evento( id_valor1, id_valor2):
        """
        Elimina la relación entre un evento y una persona. 
        La relación va desde Evento hacia Persona (Evento)-[:ASISTE_A]->(Persona)
        """

        query = f"""
        MATCH (a:{"Evento"} {{{"idEvento"}: $id_valor1}})-[r:{"ASISTE_A"}]-(b:{"Persona"} {{{"idPersona"}: $id_valor2}})
        DELETE r
        RETURN COUNT(r) AS eliminado
        """
        return neo4j_driver.query(query, {"id_valor1": id_valor1, "id_valor2": id_valor2})

    @staticmethod
    def gestionar_relacion_evento_interes(idEvento, nombreInteres, accion):
        """
        Gestionar la relación entre un evento y un interés.
        
        Args:
            idEvento (int): ID del evento.
            nombreInteres (str): Nombre del interés.
            accion (str): Acción a realizar ("crear" o "eliminar").
        
        Returns:
            dict: Resultado de la operación.
        """
        try:
            # Validar tipos de datos
            if not isinstance(idEvento, int):
                return {"error": "El ID del evento debe ser un número entero"}
            if not isinstance(nombreInteres, str):
                return {"error": "El nombre del interés debe ser una cadena de texto"}
            if not isinstance(accion, str) or accion not in ["crear", "eliminar"]:
                return {"error": "La acción debe ser 'crear' o 'eliminar'"}

            # Primero verificar si el evento existe
            evento = EventoRepository.obtener_evento_por_id(idEvento)
            if not evento:
                return {"error": f"No se encontró el evento con ID {idEvento}"}

            # Verificar si el interés existe
            query = "MATCH (i:Interes {nombre: $nombre}) RETURN i"
            result = neo4j_driver.query(query, {"nombre": nombreInteres})
            if not result:
                return {"error": f"No se encontró el interés con nombre {nombreInteres}"}

            # Si todo está bien, proceder con la gestión de la relación
            return gestionar_relacion(
                etiqueta1="Evento",
                id_propiedad1="idEvento",
                id_valor1=idEvento,
                etiqueta2="Interes",
                id_propiedad2="nombre",
                id_valor2=nombreInteres,
                tipo_relacion="RELACIONADO_CON",
                accion=accion
            )

        except Exception as e:
            return {"error": f"Error al gestionar la relación: {str(e)}"}