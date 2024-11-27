from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()
    
    def execute_query(self, query, parameters=None):
        try:
            print("Ejecutando consulta en Neo4j:", query)
            print("Parámetros enviados:", parameters)
            with self.driver.session() as session:
                result = session.run(query, parameters)
                print("Consulta ejecutada con éxito")

                # Convertir el resultado a una lista de diccionarios
                records = [record.data() for record in result]
                print("Registros obtenidos:", records)
                return records
        except Exception as e:
            print("Error ejecutando consulta en Neo4j:", e)
            raise


neo4j_conn = Neo4jConnection(
    uri="bolt://44.204.108.39:7687",
    user="neo4j",
    password="stoppering-dates-electrolyte"
)

