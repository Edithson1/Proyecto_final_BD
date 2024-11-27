from neo4j import GraphDatabase

class Neo4jDriver:
    """
    Clase para gestionar la conexión con Neo4j.
    Maneja la conexión y ejecución de consultas a la base de datos.
    """
    
    def __init__(self, uri, user, password):
        """
        Inicializa la conexión con Neo4j.
        
        Args:
            uri (str): URI del servidor Neo4j
            user (str): Nombre de usuario
            password (str): Contraseña
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query(self, query, parameters=None):
        """
        Ejecuta una consulta en Neo4j.
        
        Args:
            query (str): Consulta Cypher a ejecutar
            parameters (dict, opcional): Parámetros para la consulta
        
        Returns:
            list: Lista de registros resultantes
        """
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]

# Configuración del cliente Neo4j
NEO4J_URI = "bolt://100.29.191.87:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "eraser-desert-benches"
neo4j_driver = Neo4jDriver(uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)