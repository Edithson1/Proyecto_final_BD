from utils.neo4j_utils import (crear_nodo, obtener_nodo_por_id, 
                               actualizar_nodo, eliminar_nodo, 
                               listar_relaciones, listar_nodos)
from config.neo4j_driver import neo4j_driver
from datetime import datetime

class PublicationRepository:

    @staticmethod
    def crear_publicacion(data):
        return crear_nodo('Publicacion', data)

    @staticmethod
    def listar_publicaciones(filtros=None):
        return listar_nodos('Publicacion', filtros)

    @staticmethod
    def obtener_publicacion(idPublicacion):
        return obtener_nodo_por_id('Publicacion', 'idPublicacion', int(idPublicacion))

    @staticmethod
    def actualizar_publicacion(idPublicacion, nuevas_propiedades):
        return actualizar_nodo('Publicacion', 'idPublicacion', int(idPublicacion), nuevas_propiedades)

    @staticmethod
    def eliminar_publicacion(idPublicacion):
        return eliminar_nodo('Publicacion', 'idPublicacion', idPublicacion)

    @staticmethod
    def gestionar_reaccion(idPublicacion, data, accion):
        try:
            data['idPersona'] = int(data['idPersona'])  # Convertir a entero
            if accion == "crear":
                data['tipoReaccion'] = data['tipoReaccion'].strip().title()  # Normalizar tipoReaccion
        except ValueError:
            return {"error": "idPersona debe ser un entero"}

        if accion == "crear":
            tipo_map = {
                "Me Gusta": "like",
                "No Me Gusta": "dislike",
                "Me Encanta": "love"
            }
            id_reaccion_map = {
                "No Me Gusta": 1,
                "Me Gusta": 2,
                "Me Encanta": 3
            }
            data['idReaccion'] = id_reaccion_map.get(data['tipoReaccion'], 0)
            data.setdefault('nombreReaccion', tipo_map.get(data['tipoReaccion'], 'unknown'))
            query = """
            MATCH (p:Persona {idPersona: $idPersona}), (pub:Publicacion {idPublicacion: $idPublicacion})
            CREATE (p)-[:REACCIONA {tipoReaccion: $tipoReaccion, idReaccion: $idReaccion, nombreReaccion: $nombreReaccion}]->(pub)
            RETURN p, pub
            """
            params = {
                "idPersona": data['idPersona'],
                "idPublicacion": idPublicacion,
                "tipoReaccion": data['tipoReaccion'],
                "idReaccion": data['idReaccion'],
                "nombreReaccion": data['nombreReaccion']
            }
            return neo4j_driver.query(query, params)
        elif accion == "eliminar":
            try:
                query = """
                MATCH (p:Persona {idPersona: $idPersona})-[r:REACCIONA]->(pub:Publicacion {idPublicacion: $idPublicacion})
                DELETE r
                RETURN COUNT(r) AS eliminado
                """
                params = {
                    "idPersona": data['idPersona'],
                    "idPublicacion": idPublicacion
                }
                result = neo4j_driver.query(query, params)
                if isinstance(result, list) and len(result) > 0:
                    eliminado = result[0].get("eliminado", 0)
                    return {"eliminado": eliminado}
                else:
                    return {"error": "No se pudo eliminar la reacción."}
            except Exception as e:
                return {"error": f"Error al eliminar la reacción: {str(e)}"}
        else:
            return {"error": "Acción no válida. Use 'crear' o 'eliminar'."}

    @staticmethod
    def listar_reacciones(idPublicacion):
        query = """
        MATCH (p:Persona)-[r:REACCIONA]->(pub:Publicacion {idPublicacion: $idPublicacion})
        RETURN properties(p) AS persona, properties(r) AS reaccion
        """
        params = {"idPublicacion": idPublicacion}
        resultados = neo4j_driver.query(query, params)
        # Convertir los resultados a un formato serializable correctamente
        return [
            {
                "persona": record["persona"],
                "reaccion": record["reaccion"] if record["reaccion"] else {}
            }
            for record in resultados
        ]

    @staticmethod
    def agregar_comentario(idPublicacion, data):
        """
        Crear un comentario y establecer las relaciones en la base de datos.
        """
        try:
            query = """
            MATCH (p:Persona {idPersona: $idPersona}), (pub:Publicacion {idPublicacion: $idPublicacion})
            CREATE (comentario:Comentario {texto: $texto, fechaComentario: datetime()})
            CREATE (p)-[:ESCRIBE]->(comentario)-[:PERTENECE_A]->(pub)
            RETURN properties(comentario) AS comentario
            """
            params = {
                "idPersona": data["idPersona"],
                "idPublicacion": idPublicacion,
                "texto": data["texto"]
            }
            result = neo4j_driver.query(query, params)

            # Verificar si el comentario fue creado y devolverlo
            if result and len(result) > 0:
                return {"comentario": result[0]["comentario"]}
            else:
                return {"error": "No se pudo crear el comentario."}
        except Exception as e:
            return {"error": f"Error al agregar comentario: {str(e)}"}



    @staticmethod
    def eliminar_comentario(idComentario):
        query = """
        MATCH (comentario:Comentario {idComentario: $idComentario})
        DETACH DELETE comentario
        RETURN COUNT(comentario) AS eliminado
        """
        params = {"idComentario": idComentario}
        try:
            result = neo4j_driver.query(query, params)
            if result and result[0].get("eliminado", 0) > 0:
                return {"mensaje": "Comentario eliminado exitosamente."}
            else:
                return {"error": "Comentario no encontrado o no se pudo eliminar."}
        except Exception as e:
            return {"error": f"Error al eliminar comentario: {str(e)}"}

    @staticmethod
    def listar_comentarios(idPublicacion):
        query = """
        MATCH (comentario:Comentario)-[:PERTENECE_A]->(pub:Publicacion {idPublicacion: $idPublicacion})
        RETURN properties(comentario) AS comentario
        """
        params = {"idPublicacion": idPublicacion}
        try:
            result = neo4j_driver.query(query, params)
            return [record["comentario"] for record in result]
        except Exception as e:
            return {"error": f"Error al listar comentarios: {str(e)}"}

    @staticmethod
    def listar_intereses(idPublicacion):
        return listar_relaciones('Publicacion', 'idPublicacion', idPublicacion, 'RELACIONADA_CON', 'Interes')