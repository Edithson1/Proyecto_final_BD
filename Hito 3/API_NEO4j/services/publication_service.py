from repositories.publication_repository import PublicationRepository

class PublicationService:

    @staticmethod
    def crear_publicacion(data):
        # Asegurarse de que 'idPublicacion' es un entero si se requiere
        if 'idPublicacion' in data:
            data['idPublicacion'] = int(data['idPublicacion'])
        return PublicationRepository.crear_publicacion(data)

    @staticmethod
    def listar_publicaciones(filtros=None):
        return PublicationRepository.listar_publicaciones(filtros)

    @staticmethod
    def obtener_publicacion(idPublicacion):
        try:
            idPublicacion = int(idPublicacion)
        except ValueError:
            return {"error": "idPublicacion debe ser un entero"}
        return PublicationRepository.obtener_publicacion(idPublicacion)

    @staticmethod
    def actualizar_publicacion(idPublicacion, data):
        try:
            idPublicacion = int(idPublicacion)
        except ValueError:
            return {"error": "idPublicacion debe ser un entero"}
        return PublicationRepository.actualizar_publicacion(idPublicacion, data)

    @staticmethod
    def eliminar_publicacion(idPublicacion):
        return PublicationRepository.eliminar_publicacion(idPublicacion)

    @staticmethod
    def agregar_reaccion(idPublicacion, data):
        try:
            data['idPersona'] = int(data['idPersona'])  # Convertir a entero
        except ValueError:
            return {"error": "idPersona debe ser un entero"}
        return PublicationRepository.gestionar_reaccion(idPublicacion, data, accion="crear")

    @staticmethod
    def eliminar_reaccion(idPublicacion, data):
        try:
            resultado = PublicationRepository.gestionar_reaccion(idPublicacion, data, accion="eliminar")
            if "error" in resultado:
                return resultado
            if resultado.get("eliminado", 0) > 0:
                return {"mensaje": "Reacción eliminada exitosamente."}
            else:
                return {"error": "No se encontró la reacción para eliminar."}
        except Exception as e:
            return {"error": f"Excepción en eliminar_reaccion: {str(e)}"}
    
    @staticmethod
    def listar_reacciones(idPublicacion):
        try:
            return PublicationRepository.listar_reacciones(idPublicacion)
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def agregar_comentario(idPublicacion, data):
        try:
            # Convertir idPublicacion e idPersona a los tipos correctos
            idPublicacion = str(idPublicacion)  # Convertir idPublicacion a string si está almacenado como string
            data["idPersona"] = int(data["idPersona"])  # Convertir idPersona a entero
        except ValueError:
            return {"error": "El campo 'idPersona' debe ser un entero y 'idPublicacion' un string."}

        # Delegar la creación directamente al repositorio
        return PublicationRepository.agregar_comentario(idPublicacion, data)


    @staticmethod
    def eliminar_comentario(idComentario):
        try:
            idComentario = int(idComentario)
        except ValueError:
            return {"error": "idComentario debe ser un entero."}
        return PublicationRepository.eliminar_comentario(idComentario)

    @staticmethod
    def listar_comentarios(idPublicacion):
        try:
            idPublicacion = int(idPublicacion)
        except ValueError:
            return {"error": "idPublicacion debe ser un entero."}
        return PublicationRepository.listar_comentarios(idPublicacion)


    @staticmethod
    def listar_intereses(idPublicacion):
        return PublicationRepository.listar_intereses(idPublicacion)


