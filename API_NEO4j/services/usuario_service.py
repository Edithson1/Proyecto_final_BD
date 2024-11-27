from repositories.usuario_repository import UsuarioRepository

"""
Servicio que implementa la lógica de negocio para la gestión de usuarios.
Maneja validaciones y orquesta las operaciones del repositorio.
"""

class UsuarioService:
    """
    Clase que contiene la lógica de negocio para operaciones con usuarios.
    Realiza validaciones y manejo de errores antes de ejecutar operaciones en el repositorio.
    """
    
    @staticmethod
    def crear_usuario(data):
        """
        Crea un nuevo usuario con validaciones.
        
        Args:
            data (dict): Datos del usuario a crear
        
        Returns:
            dict: Resultado de la operación o mensaje de error
        """
        # Validar que el ID del usuario sea proporcionado
        if "idPersona" not in data:
            return {"error": "idPersona es obligatorio."}
        return UsuarioRepository.crear(data)

    @staticmethod
    def obtener_usuario(id):
        """
        Obtiene un usuario por su ID.

        Args:
            id (int): El ID del usuario a obtener.

        Returns:
            dict: Un diccionario con el usuario encontrado o un mensaje de error si no se encuentra.
        """
        usuario = UsuarioRepository.obtener_por_id(id)
        if not usuario:
            return {"error": f"Usuario con idPersona {id} no encontrado."}
        return usuario

    @staticmethod
    def actualizar_usuario(id, data):
        """
        Actualiza la información de un usuario.

        Args:
            id (int): El ID del usuario a actualizar.
            data (dict): Un diccionario con los datos a actualizar.

        Returns:
            dict: Un diccionario con el usuario actualizado o un mensaje de error si no se puede actualizar.
        """
        usuario_actual = UsuarioRepository.obtener_por_id(id)
        if not usuario_actual:
            return {"error": f"Usuario con idPersona {id} no encontrado para actualizar."}

        if "idPersona" in data and data["idPersona"] != id:
            nuevo_id = data["idPersona"]
            if UsuarioRepository.obtener_por_id(nuevo_id):
                return {"error": f"El idPersona {nuevo_id} ya está en uso."}

        data_filtered = {k: v for k, v in data.items() if v is not None and v != ""}
        
        if data_filtered:
            return UsuarioRepository.actualizar(id, data_filtered)
        return {"error": "No se proporcionaron datos válidos para actualizar."}

    @staticmethod
    def eliminar_usuario(id):
        """
        Elimina un usuario por su ID.

        Args:
            id (int): El ID del usuario a eliminar.

        Returns:
            dict: Un diccionario con el resultado de la eliminación o un mensaje de error si no se puede eliminar.
        """
        usuario = UsuarioRepository.obtener_por_id(id)
        if not usuario:
            return {"error": f"Usuario con idPersona {id} no encontrado para eliminar."}
        return UsuarioRepository.eliminar(id)

    @staticmethod
    def listar_seguidores(id):
        """
        Lista los seguidores de un usuario.

        Args:
            id (int): El ID del usuario cuyos seguidores se quieren listar.

        Returns:
            dict: Un diccionario con la lista de seguidores o un mensaje de error si no se puede listar.
        """
        try:
            usuario = UsuarioRepository.obtener_por_id(id)
            if not usuario:
                return {"error": f"Usuario con idPersona {id} no encontrado."}
            
            result = UsuarioRepository.listar_relaciones_seguidores(id)
            return {"seguidores": result}
        except Exception as e:
            return {"error": f"Error al listar seguidores: {str(e)}"}

    @staticmethod
    def listar_seguidos(id):
        """
        Lista los usuarios seguidos por un usuario.

        Args:
            id (int): El ID del usuario cuyos seguidos se quieren listar.

        Returns:
            dict: Un diccionario con la lista de seguidos o un mensaje de error si no se puede listar.
        """
        try:
            usuario = UsuarioRepository.obtener_por_id(id)
            if not usuario:
                return {"error": f"Usuario con idPersona {id} no encontrado."}
            
            result = UsuarioRepository.listar_relaciones_seguidos(id)
            return {"seguidos": result}
        except Exception as e:
            return {"error": f"Error al listar seguidos: {str(e)}"}

    @staticmethod
    def seguir_usuario(id, id_seguir):
        """
        Permite a un usuario seguir a otro usuario.

        Args:
            id (int): El ID del usuario que va a seguir.
            id_seguir (int): El ID del usuario a seguir.

        Returns:
            dict: Un diccionario con el resultado de la operación o un mensaje de error si no se puede seguir.
        """
        usuario = UsuarioRepository.obtener_por_id(id)
        if not usuario:
            return {"error": f"Usuario con idPersona {id} no encontrado."}

        usuario_seguir = UsuarioRepository.obtener_por_id(id_seguir)
        if not usuario_seguir:
            return {"error": f"Usuario con idPersona {id_seguir} no encontrado."}

        return UsuarioRepository.seguir_usuario(id, id_seguir)

    @staticmethod
    def dejar_de_seguir_usuario(id, id_seguir):
        """
        Permite a un usuario dejar de seguir a otro usuario.

        Args:
            id (int): El ID del usuario que va a dejar de seguir.
            id_seguir (int): El ID del usuario a dejar de seguir.

        Returns:
            dict: Un diccionario con el resultado de la operación o un mensaje de error si no se puede dejar de seguir.
        """
        usuario = UsuarioRepository.obtener_por_id(id)
        if not usuario:
            return {"error": f"Usuario con idPersona {id} no encontrado."}

        usuario_seguir = UsuarioRepository.obtener_por_id(id_seguir)
        if not usuario_seguir:
            return {"error": f"Usuario con idPersona {id_seguir} no encontrado."}

        return UsuarioRepository.dejar_de_seguir_usuario(id, id_seguir)