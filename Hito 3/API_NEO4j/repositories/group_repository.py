from utils.neo4j_utils import (
    crear_nodo, obtener_nodo_por_id, 
    actualizar_nodo, eliminar_nodo, 
    gestionar_relacion, listar_relaciones, 
    listar_nodos)

class GroupRepository:

    @staticmethod
    def crear_grupo(data):
        return crear_nodo('Grupo', data)

    @staticmethod
    def listar_grupos(filtros=None):
        return listar_nodos('Grupo', filtros)

    @staticmethod
    def obtener_grupo(idGrupo):
        return obtener_nodo_por_id('Grupo', 'idGrupo', idGrupo)

    @staticmethod
    def actualizar_grupo(idGrupo, nuevas_propiedades):
        return actualizar_nodo('Grupo', 'idGrupo', idGrupo, nuevas_propiedades)

    @staticmethod
    def eliminar_grupo(idGrupo):
        return eliminar_nodo('Grupo', 'idGrupo', idGrupo)

    @staticmethod
    def gestionar_relacion_grupo_miembro(idGrupo, idUsuario, accion):
        return gestionar_relacion('Grupo', 'idGrupo', idGrupo, 'Persona', 'idPersona', idUsuario, 'ES_MIEMBRO_DE', accion)

    @staticmethod
    def listar_miembros(idGrupo):
        return listar_relaciones('Grupo', 'idGrupo', idGrupo, 'ES_MIEMBRO_DE', 'Persona')

    @staticmethod
    def establecer_creador(idGrupo, idUsuario):
        return gestionar_relacion('Persona', 'idPersona', idUsuario, 'Grupo', 'idGrupo', idGrupo, 'CREADOR_DE', accion="crear")
