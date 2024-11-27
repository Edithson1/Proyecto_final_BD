from repositories.interes_repository import InteresRepository

class InteresService:

    @staticmethod
    def listar_intereses():
        return InteresRepository.listar_intereses()

    @staticmethod
    def asociar_interes_persona(idPersona, nombreInteres):
        try:
            idPersona = int(idPersona)
            if not nombreInteres:
                return {"error": "El nombre del interés es obligatorio."}
            return InteresRepository.gestionar_relacion_persona_interes(idPersona, nombreInteres, accion="crear")
        except ValueError:
            return {"error": "El ID de la persona debe ser un número entero."}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def eliminar_interes_persona(idPersona, nombreInteres):
        try:
            idPersona = int(idPersona)
            if not nombreInteres:
                return {"error": "El nombre del interés es obligatorio."}
            return InteresRepository.gestionar_relacion_persona_interes(idPersona, nombreInteres, accion="eliminar")
        except ValueError:
            return {"error": "El ID de la persona debe ser un número entero."}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def obtener_intereses_persona(idPersona):
        try:
            idPersona = int(idPersona)
            return InteresRepository.obtener_relaciones_persona_interes(idPersona)
        except ValueError:
            return {"error": "El ID de la persona debe ser un número entero."}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def asociar_interes_publicacion(idPublicacion, nombreInteres):
        try:
            idPublicacion = int(idPublicacion)
            if not nombreInteres:
                return {"error": "El nombre del interés es obligatorio."}
            return InteresRepository.gestionar_relacion_publicacion_interes(idPublicacion, nombreInteres, accion="crear")
        except ValueError:
            return {"error": "El ID de la publicación debe ser un número entero."}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def eliminar_interes_publicacion(idPublicacion, nombreInteres):
        """
        Eliminar la relación RELACIONADA_CON entre una publicación y un interés.

        Args:
            idPublicacion (int): ID de la publicación.
            nombreInteres (str): Nombre del interés.

        Returns:
            dict: Resultado de la operación o un mensaje de error.
        """
        try:
            idPublicacion = int(idPublicacion)
            if not nombreInteres:
                return {"error": "El nombre del interés es obligatorio."}
            return InteresRepository.gestionar_relacion_publicacion_interes(idPublicacion, nombreInteres, accion="eliminar")
        except ValueError:
            return {"error": "El ID de la publicación debe ser un número entero."}
        except Exception as e:
            return {"error": str(e)}
