from utils.db import get_connection

def obtener_usuarios_excluyendo(id_persona_actual):
    """
    Obtiene todos los usuarios registrados en la base de datos excluyendo al usuario autenticado.
    :param id_persona_actual: ID del usuario que inició sesión
    :return: Lista de usuarios como diccionarios
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Consulta para obtener todos los usuarios excepto el actual
            sql = """
                SELECT idPersona, Nombre, UserName, descripcion 
                FROM Persona 
                WHERE idPersona != %s
                ORDER BY Nombre
            """
            cursor.execute(sql, (id_persona_actual,))
            usuarios = cursor.fetchall()

        # Formatear los resultados como una lista de diccionarios
        return [
            {
                "idPersona": usuario["idPersona"],
                "Nombre": usuario["Nombre"],
                "UserName": usuario["UserName"],
                "descripcion": usuario["descripcion"]
            }
            for usuario in usuarios
        ]

    except Exception as e:
        print("Error al obtener usuarios:", e)
        raise e  # Lanza el error para manejarlo en la capa superior

    finally:
        connection.close()