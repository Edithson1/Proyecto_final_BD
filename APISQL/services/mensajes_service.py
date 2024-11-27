# Asegúrate de tener una función para ejecutar consultas en Neo4j
from utils.db import get_connection  # Conexión a MySQL
from utils.neo4j import neo4j_conn

def validar_amigos(id_emisor, id_receptor):
    query = """
    MATCH (a:Persona {idPersona: $id_emisor})-[:SIGUE {esAmigo: True}]->(b:Persona {idPersona: $id_receptor}),
          (b)-[:SIGUE {esAmigo: True}]->(a)
    RETURN COUNT(*) AS amistad
    """
    result = neo4j_conn.execute_query(query, {"id_emisor": id_emisor, "id_receptor": id_receptor})
    print(f"Result of friendship check between {id_emisor} and {id_receptor}: {result}")
    return result[0]['amistad'] > 0

def enviar_mensaje_y_obtener_chat(id_emisor, id_receptor, texto):
    """
    Registra un mensaje en la base de datos SQL y devuelve el historial de mensajes entre los usuarios.
    :param id_emisor: ID del emisor en MySQL
    :param id_receptor: ID del receptor en MySQL
    :param texto: Texto del mensaje
    :return: Lista de mensajes entre los usuarios
    """
    connection = get_connection()
    try:
        # Insertar mensaje en la base de datos SQL
        with connection.cursor() as cursor:
            sql_insert = """
            INSERT INTO Mensaje (texto, fechaEnvio, Persona_idEmisor, Persona_idReceptor)
            VALUES (%s, NOW(), %s, %s)
            """
            cursor.execute(sql_insert, (texto, id_emisor, id_receptor))
        
        connection.commit()

        # Obtener historial de mensajes entre los usuarios
        with connection.cursor() as cursor:
            sql_select = """
            SELECT texto, fechaEnvio, Persona_idEmisor AS emisor, Persona_idReceptor AS receptor
            FROM Mensaje
            WHERE (Persona_idEmisor = %s AND Persona_idReceptor = %s)
               OR (Persona_idEmisor = %s AND Persona_idReceptor = %s)
            ORDER BY fechaEnvio ASC
            """
            cursor.execute(sql_select, (id_emisor, id_receptor, id_receptor, id_emisor))
            mensajes = cursor.fetchall()

        # Formatear historial de chat
        chat = [
            {
                "texto": mensaje['texto'],
                "fechaEnvio": mensaje['fechaEnvio'].strftime('%Y-%m-%d %H:%M:%S'),
                "emisor": mensaje['emisor'],
                "receptor": mensaje['receptor']
            }
            for mensaje in mensajes
        ]

        return chat

    except Exception as e:
        connection.rollback()
        print("Error al enviar mensaje:", str(e))
        raise e

    finally:
        connection.close()
