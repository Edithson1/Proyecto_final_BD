from repositories.evento_repository import EventoRepository
import datetime

class EventoService:

    @staticmethod
    def crear_evento(datos):
        return EventoRepository.crear_evento(datos)

    @staticmethod
    def listar_eventos():
        return EventoRepository.listar_eventos()

    @staticmethod
    def obtener_evento_por_id(idEvento):
        """
        Servicio para obtener un evento por su ID.
        """
        resultado = EventoRepository.obtener_evento_por_id(idEvento)
        if not resultado:
            return {"error": "No se encontró el evento con el ID proporcionado."}
        return resultado  # Devolver el primer elemento (ya es un diccionario)

    def actualizar_evento(idEvento, nuevas_propiedades):
        """
        Servicio para actualizar un evento.
        """
        idEvento = int(idEvento)  # Convertir a entero
        # Verificar si 'fecha' está en las propiedades y convertirla a formato datetime para Neo4j
        if "fecha" in nuevas_propiedades:
            # Convertir la fecha a formato Neo4j `datetime()`
            nuevas_propiedades["fecha"] = f"datetime('{nuevas_propiedades['fecha']}')"

        # Llamar al repositorio para actualizar el evento
        resultado = EventoRepository.actualizar_evento(idEvento, nuevas_propiedades)

        # Verificar si la actualización fue exitosa
        if not resultado or "error" in resultado:
            return {"error": "No se pudo actualizar el evento."}

        return {"mensaje": "Evento actualizado correctamente."}

    @staticmethod
    def eliminar_evento(idEvento):
        idEvento = int(idEvento)  # Convertir a entero
        return EventoRepository.eliminar_evento(idEvento)

    @staticmethod
    def registrar_asistente(idEvento, idPersona):
        try:
            idEvento = int(idEvento)
            idPersona = int(idPersona)
            return EventoRepository.gestionar_relacion_evento_persona(
                idPersona=idPersona, 
                idEvento=idEvento,
                tipo_relacion="ASISTE_A",
                accion="crear"
            )
        except ValueError:
            return {"error": "IDs inválidos"}
        except Exception as e:
            return {"error": str(e)}
 
    @staticmethod
    def eliminar_asistente(idEvento, idPersona):
        try:
            idEvento = int(idEvento)
            idPersona = int(idPersona)

            return EventoRepository.eliminar_persona_evento(idEvento,idPersona)
        except ValueError:
            return {"error": "IDs inválidos"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def listar_asistentes(idEvento):
        try:
            idEvento = int(idEvento)
            resultado = EventoRepository.listar_relaciones_evento_persona(idEvento, "ASISTE_A")
            if not resultado:
                return []
            return resultado
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def asociar_interes_evento(idEvento, nombreInteres):
        try:
            # Validar que los parámetros no sean nulos
            if idEvento is None or nombreInteres is None:
                return {"error": "El ID del evento y el nombre del interés son requeridos"}

            # Convertir idEvento a entero si es necesario
            try:
                idEvento = int(idEvento)
            except (ValueError, TypeError):
                return {"error": "El ID del evento debe ser un número válido"}

            # Validar que el nombreInteres sea una cadena no vacía
            if not isinstance(nombreInteres, str) or not nombreInteres.strip():
                return {"error": "El nombre del interés debe ser una cadena válida"}

            # Llamar al repositorio para gestionar la relación
            resultado = EventoRepository.gestionar_relacion_evento_interes(
                idEvento,
                nombreInteres.strip(),
                accion="crear"
            )
            
            if "error" in resultado:
                return resultado

            return {"mensaje": "Interés asociado correctamente al evento"}
            
        except Exception as e:
            return {"error": f"Error al asociar el interés: {str(e)}"}