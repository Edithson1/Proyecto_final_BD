from repositories.group_repository import GroupRepository

class GroupService:

    @staticmethod
    def crear_grupo(data):
        return GroupRepository.crear_grupo(data)

    @staticmethod
    def listar_grupos(filtros=None):
        return GroupRepository.listar_grupos(filtros)

    @staticmethod
    def obtener_grupo(idGrupo):
        return GroupRepository.obtener_grupo(idGrupo)

    @staticmethod
    def actualizar_grupo(idGrupo, data):
        return GroupRepository.actualizar_grupo(idGrupo, data)

    @staticmethod
    def eliminar_grupo(idGrupo):
        return GroupRepository.eliminar_grupo(idGrupo)

    @staticmethod
    def agregar_miembro(idGrupo, idUsuario):
        return GroupRepository.gestionar_relacion_grupo_miembro(idGrupo, idUsuario, accion="crear")

    @staticmethod
    def eliminar_miembro(idGrupo, idUsuario):
        return GroupRepository.gestionar_relacion_grupo_miembro(idGrupo, idUsuario, accion="eliminar")

    @staticmethod
    def listar_miembros(idGrupo):
        return GroupRepository.listar_miembros(idGrupo)

    @staticmethod
    def establecer_creador(idGrupo, idUsuario):
        return GroupRepository.establecer_creador(idGrupo, idUsuario)
