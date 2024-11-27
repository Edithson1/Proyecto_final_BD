# services/influencer_service.py

from repositories.influencer_repository import InfluencerRepository
from services.usuario_service import UsuarioService

class InfluencerService:

    @staticmethod
    def convertir_en_influencer(idPersona):
        """
        Verificar si una persona tiene más de 1000 seguidores y convertirla en influencer.
        
        Args:
            idPersona (int): ID de la persona.
        
        Returns:
            dict: Resultado de la operación.
        """
        try:
            # Primero, obtenemos la lista de seguidores de la persona
            seguidores = UsuarioService.listar_seguidores(idPersona)
            seguidos = UsuarioService.listar_seguidos(idPersona)
            
            # Sacamos el 10% de los seguidores
            porcentaje_seguidores = len(seguidores) * 10 // 100
            # Verificamos si la persona tiene más de 1000 seguidores
            if len(seguidores) >= 1000 and len(seguidos) < porcentaje_seguidores:
                # Si tiene más de 1000 seguidores, la convertimos en influencer
                return InfluencerRepository.convertir_en_influencer(idPersona)
            else:
                return {"error": "La persona no tiene suficientes seguidores para ser un influencer."}
        except ValueError:
            return {"error": "El ID de la persona debe ser un número entero."}
        except Exception as e:
            return {"error": str(e)}
