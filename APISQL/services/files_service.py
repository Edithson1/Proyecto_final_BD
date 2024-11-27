from utils.db import get_connection

def obtener_publicaciones_usuario(id_persona):
    """
    Consulta todas las publicaciones de un usuario por su ID.
    :param id_persona: ID del usuario
    :return: Lista de publicaciones como diccionarios
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Consulta para obtener las publicaciones del usuario
            sql = """
                SELECT idPublicacion, url, tipoFormato, fechaPublicacion, descripcion 
                FROM Publicacion 
                WHERE idPersonaPub = %s
                ORDER BY fechaPublicacion DESC
            """
            cursor.execute(sql, (id_persona,))
            publicaciones = cursor.fetchall()

        # Procesar los resultados y devolverlos como lista de diccionarios
        return [
            {
                "idPublicacion": pub["idPublicacion"],
                "url": pub["url"].decode('utf-8') if isinstance(pub["url"], bytes) else pub["url"],
                "tipoFormato": pub["tipoFormato"],
                "fechaPublicacion": pub["fechaPublicacion"].strftime('%Y-%m-%d %H:%M:%S'),
                "descripcion": pub["descripcion"]
            }
            for pub in publicaciones
        ]

    except Exception as e:
        print("Error al obtener las publicaciones:", e)
        raise e  # Lanza el error para manejarlo donde se llame la función

    finally:
        connection.close()


def eliminar_publicacion_usuario(idPublicacion, id_persona):
    """
    Elimina una publicación específica de un usuario autenticado.
    :param idPublicacion: ID de la publicación
    :param id_persona: ID del usuario autenticado
    :return: True si la publicación fue eliminada, False si no se encontró
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Verificar si la publicación existe y pertenece al usuario
            sql_verificar = "SELECT idPublicacion FROM Publicacion WHERE idPublicacion = %s AND idPersonaPub = %s"
            cursor.execute(sql_verificar, (idPublicacion, id_persona))
            publicacion = cursor.fetchone()

            if not publicacion:
                return False  # La publicación no existe o no pertenece al usuario

            # Eliminar la publicación
            sql_eliminar = "DELETE FROM Publicacion WHERE idPublicacion = %s AND idPersonaPub = %s"
            cursor.execute(sql_eliminar, (idPublicacion, id_persona))
            connection.commit()
            return True

    except Exception as e:
        connection.rollback()
        print("Error al eliminar la publicación:", e)
        raise e  # Lanza el error para manejarlo en la capa superior

    finally:
        connection.close()


def guardar_publicacion(filename, tipo_formato, descripcion, id_persona):
    """
    Guarda una publicación en la base de datos.
    :param filename: Nombre del archivo guardado
    :param tipo_formato: Formato del archivo (e.g., imagen)
    :param descripcion: Descripción de la publicación
    :param id_persona: ID del usuario que realiza la publicación
    :return: True si la publicación fue guardada exitosamente, False en caso de error
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO Publicacion (url, tipoFormato, fechaPublicacion, descripcion, idPersonaPub) 
                VALUES (%s, %s, CURRENT_TIMESTAMP, %s, %s)
            """
            cursor.execute(sql, (filename, tipo_formato, descripcion, id_persona))
            connection.commit()
            return True

    except Exception as e:
        connection.rollback()
        print("Error al guardar la publicación:", e)
        raise e

    finally:
        connection.close()


def obtener_publicaciones_de_otros(id_persona_actual):
    """
    Obtiene las publicaciones de otros usuarios, excluyendo las del usuario actual.
    :param id_persona_actual: ID del usuario autenticado
    :return: Lista de publicaciones como diccionarios
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Consulta para obtener publicaciones de otros usuarios
            sql = """
                SELECT p.idPublicacion, p.url, p.tipoFormato, p.fechaPublicacion, p.descripcion, u.Nombre AS autor
                FROM Publicacion p
                INNER JOIN Persona u ON p.idPersonaPub = u.idPersona
                WHERE p.idPersonaPub != %s
                ORDER BY p.fechaPublicacion DESC
            """
            cursor.execute(sql, (id_persona_actual,))
            publicaciones = cursor.fetchall()

        # Formatear los resultados como una lista de diccionarios
        return [
            {
                "idPublicacion": pub["idPublicacion"],
                "url": pub["url"] if isinstance(pub["url"], str) else pub["url"].decode('utf-8', errors='ignore'),
                "tipoFormato": pub["tipoFormato"],
                "fechaPublicacion": pub["fechaPublicacion"].strftime('%Y-%m-%d %H:%M:%S'),
                "descripcion": pub["descripcion"],
                "autor": pub["autor"]
            }
            for pub in publicaciones
        ]

    except Exception as e:
        print("Error al obtener publicaciones de otros usuarios:", e)
        raise e  # Lanza el error para manejarlo en la capa superior

    finally:
        connection.close()