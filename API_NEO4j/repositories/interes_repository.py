from utils.neo4j_utils import listar_nodos, gestionar_relacion, listar_relaciones

class InteresRepository:

    @staticmethod
    def listar_intereses():
        return listar_nodos("Interes")

    @staticmethod
    def gestionar_relacion_persona_interes(idPersona, nombreInteres, accion):
        return gestionar_relacion(
            etiqueta1="Persona",
            id_propiedad1="idPersona",
            id_valor1=idPersona,
            etiqueta2="Interes",
            id_propiedad2="nombre",
            id_valor2=nombreInteres,
            tipo_relacion="INTERESADO_EN",
            accion=accion
        )

    @staticmethod
    def obtener_relaciones_persona_interes(idPersona):
        return listar_relaciones(
            etiqueta1="Persona",
            id_propiedad1="idPersona",
            id_valor1=idPersona,
            tipo_relacion="INTERESADO_EN",
            etiqueta2="Interes",
            derecha=False
        )

    @staticmethod
    def gestionar_relacion_publicacion_interes(idPublicacion, nombreInteres, accion):
        return gestionar_relacion(
            etiqueta1="Publicacion",
            id_propiedad1="idPublicacion",
            id_valor1=idPublicacion,
            etiqueta2="Interes",
            id_propiedad2="nombre",
            id_valor2=nombreInteres,
            tipo_relacion="RELACIONADA_CON",
            accion=accion
        )

    @staticmethod
    def gestionar_relacion_publicacion_interes(idPublicacion, nombreInteres, accion):
        """
        Gestionar la relación RELACIONADA_CON entre una publicación y un interés.

        Args:
            idPublicacion (int): ID de la publicación.
            nombreInteres (str): Nombre del interés.
            accion (str): Acción a realizar ("crear" o "eliminar").

        Returns:
            dict: Resultado de la operación o un mensaje de error.
        """
        return gestionar_relacion(
            etiqueta1="Publicacion",
            id_propiedad1="idPublicacion",
            id_valor1=idPublicacion,
            etiqueta2="Interes",
            id_propiedad2="nombre",
            id_valor2=nombreInteres,
            tipo_relacion="RELACIONADA_CON",
            accion=accion
        )
