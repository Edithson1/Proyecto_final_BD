# repositories/influencer_repository.py

from utils.neo4j_utils import gestionar_relacion
from config.neo4j_driver import neo4j_driver

class InfluencerRepository:

    @staticmethod
    def convertir_en_influencer(idPersona):
        """
        Convertir una persona en influencer creando la relación con el nodo Influencer.
        
        Args:
            idPersona (int): ID de la persona que se va a convertir en influencer.
        
        Returns:
            dict: Resultado de la operación.
        """
        try:
            # Creamos el nodo influencer y la relación con la persona
            query = """
            MATCH (p:Persona {idPersona: $idPersona})
            CREATE (i:Influencer {idInfluencer: apoc.create.uuid()})
            CREATE (p)-[:ES_INFLUENCER]->(i)
            RETURN i
            """
            result = neo4j_driver.query(query, {"idPersona": idPersona})
            if result:
                return {"mensaje": "La persona se ha convertido en influencer."}
            return {"error": "No se pudo convertir a la persona en influencer."}
        except Exception as e:
            return {"error": str(e)}
