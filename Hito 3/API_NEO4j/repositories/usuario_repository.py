from utils.neo4j_utils import (
    crear_nodo,
    obtener_nodo_por_id,
    actualizar_nodo,
    eliminar_nodo,
    listar_relaciones,
    gestionar_relacion
)

"""
Repositorio para gestionar operaciones CRUD de usuarios en Neo4j.
Actúa como una capa de abstracción entre los servicios y las utilidades de Neo4j.
"""

class UsuarioRepository:
    """
    Clase que encapsula todas las operaciones de base de datos relacionadas con usuarios.
    Utiliza las funciones de neo4j_utils para realizar operaciones en la base de datos.
    """
    
    @staticmethod
    def crear(data):
        """
        Crea un nuevo usuario en la base de datos.
        
        Args:
            data (dict): Datos del usuario a crear
        
        Returns:
            dict: Información del usuario creado
        """
        return crear_nodo("Persona", data)

    @staticmethod
    def obtener_por_id(id):
        """
        Obtiene un nodo de la base de datos por su ID.

        Args:
            id (int): El ID del nodo a obtener.

        Returns:
            dict: Un diccionario con los datos del nodo encontrado.
        """
        return obtener_nodo_por_id("Persona", "idPersona", id)

    @staticmethod
    def actualizar(id, data):
        """
        Actualiza un nodo en la base de datos.

        Args:
            id (int): El ID del nodo a actualizar.
            data (dict): Un diccionario con los datos a actualizar.

        Returns:
            dict: Un diccionario con los datos del nodo actualizado.
        """
        return actualizar_nodo("Persona", "idPersona", id, data)

    @staticmethod
    def eliminar(id):
        """
        Elimina un nodo de la base de datos por su ID.

        Args:
            id (int): El ID del nodo a eliminar.

        Returns:
            dict: Un diccionario con el resultado de la eliminación.
        """
        return eliminar_nodo("Persona", "idPersona", id)

    @staticmethod
    def listar_relaciones_seguidores(id):
        """
        Obtiene los usuarios que siguen al usuario con el ID proporcionado.

        Args:
            id (int): El ID del usuario cuyos seguidores se quieren listar.

        Returns:
            list: Una lista de diccionarios con los datos de los seguidores.
        """
        return listar_relaciones("Persona", "idPersona", id, "SIGUE", "Persona", derecha=True)

    @staticmethod
    def listar_relaciones_seguidos(id):
        """
        Obtiene los usuarios que son seguidos por el usuario con el ID proporcionado.

        Args:
            id (int): El ID del usuario cuyos seguidos se quieren listar.

        Returns:
            list: Una lista de diccionarios con los datos de los seguidos.
        """
        return listar_relaciones("Persona", "idPersona", id, "SIGUE", "Persona", derecha=False)

    @staticmethod
    def seguir_usuario(id, id_seguir):
        """
        Crea una relación de seguimiento entre dos usuarios.

        Args:
            id (int): El ID del usuario que va a seguir.
            id_seguir (int): El ID del usuario a seguir.

        Returns:
            dict: Un diccionario con el resultado de la operación.
        """
        return gestionar_relacion("Persona", "idPersona", id, "Persona", "idPersona", id_seguir, "SIGUE", accion="crear")

    @staticmethod
    def dejar_de_seguir_usuario(id, id_seguir):
        """
        Elimina una relación de seguimiento entre dos usuarios.

        Args:
            id (int): El ID del usuario que va a dejar de seguir.
            id_seguir (int): El ID del usuario a dejar de seguir.

        Returns:
            dict: Un diccionario con el resultado de la operación.
        """
        return gestionar_relacion("Persona", "idPersona", id, "Persona", "idPersona", id_seguir, "SIGUE", accion="eliminar")