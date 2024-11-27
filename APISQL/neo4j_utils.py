"""
Módulo de utilidades para operaciones CRUD y gestión de relaciones en Neo4j.
Proporciona funciones de alto nivel para interactuar con la base de datos.
"""



from utils.neo4j import neo4j_conn

def query(query, params=None):
    """
    Ejecuta una consulta Cypher y devuelve los resultados.
    """
    with neo4j_conn.session() as session:
        try:
            result = session.run(query, params)
            return [record.data() for record in result]
        except Exception as e:
            return {"error": str(e)}

def crear_nodo(etiqueta, propiedades):
    """
    Crea un nuevo nodo en Neo4j.
    
    Args:
        etiqueta (str): Etiqueta del nodo (ej: 'Persona')
        propiedades (dict): Propiedades del nodo
    
    Returns:
        dict: Datos del nodo creado
    """
    keys = ", ".join([f"{k}: ${k}" for k in propiedades.keys()])
    query = f"CREATE (n:{etiqueta} {{ {keys} }}) RETURN n"
    return neo4j_conn.execute_query(query, propiedades)

def obtener_nodo_por_id(etiqueta, id_propiedad, id_valor):
    """
    Obtener un nodo por su ID en Neo4j.
    """
    query = f"MATCH (n:{etiqueta} {{{id_propiedad}: $id_valor}}) RETURN n"
    result = neo4j_conn.execute_query(query, {"id_valor": id_valor})

    # Si no hay resultados, devolver None
    if not result:
        return None

    # El resultado ya está en formato lista de diccionarios, extraer propiedades del nodo
    return result

def actualizar_nodo(etiqueta, id_propiedad, id_valor, nuevas_propiedades):
    """
    Actualizar un nodo en Neo4j con nuevas propiedades.
    """
    # Validar que haya propiedades para actualizar
    if not nuevas_propiedades:
        return {"error": "No hay propiedades para actualizar"}

    # Construir la cláusula SET de manera segura
    set_items = []
    params = {"id_valor": id_valor}
    
    for k, v in nuevas_propiedades.items():
        param_key = f"param_{k}"
        set_items.append(f"n.{k} = ${param_key}")
        params[param_key] = v

    set_clause = ", ".join(set_items)
    
    query = f"""
    MATCH (n:{etiqueta} {{{id_propiedad}: $id_valor}}) 
    SET {set_clause} 
    RETURN n
    """
    return neo4j_conn.execute_query(query, params)

def eliminar_nodo(etiqueta, id_propiedad, id_valor):
    """
    Eliminar un nodo en Neo4j por su ID.
    """
    query = f"MATCH (n:{etiqueta} {{{id_propiedad}: $id_valor}}) DETACH DELETE n RETURN COUNT(n) AS eliminado"
    return neo4j_conn.execute_query(query, {"id_valor": id_valor})

def listar_relaciones(etiqueta1, id_propiedad1, id_valor1, tipo_relacion, etiqueta2, derecha=False):
    """
    Listar relaciones de un nodo hacia otros nodos.
    Para seguidores: derecha=True (quien me sigue)
    Para seguidos: derecha=False (a quién sigo)
    """
    if derecha:
        # Para seguidores: (b)-[:SIGUE]->(a)
        query = f"""
        MATCH (b:{etiqueta2})-[:{tipo_relacion}]->(a:{etiqueta1} {{{id_propiedad1}: $id_valor1}})
        RETURN b
        """
    else:
        # Para seguidos: (a)-[:SIGUE]->(b)
        query = f"""
        MATCH (a:{etiqueta1} {{{id_propiedad1}: $id_valor1}})-[:{tipo_relacion}]->(b:{etiqueta2})
        RETURN b
        """
    return neo4j_conn.query(query, {"id_valor1": id_valor1})

def gestionar_relacion_y_actualizar_amistad(etiqueta1, id_propiedad1, id_valor1, etiqueta2, id_propiedad2, id_valor2, tipo_relacion):
    """
    Crea una relación entre dos nodos y actualiza la propiedad `esAmigo` si ambos nodos se siguen mutuamente.
    """
    try:
        # Crear la relación SIGUE del usuario 1 al usuario 2
        query_crear = f"""
        MATCH (a:{etiqueta1} {{{id_propiedad1}: $id_valor1}}), (b:{etiqueta2} {{{id_propiedad2}: $id_valor2}})
        MERGE (a)-[r:{tipo_relacion}]->(b)
        RETURN r
        """
        neo4j_conn.execute_query(query_crear, {"id_valor1": id_valor1, "id_valor2": id_valor2})

        # Verificar si ambos usuarios se siguen mutuamente
        query_verificar = f"""
        MATCH (a:{etiqueta1} {{{id_propiedad1}: $id_valor1}})-[r1:{tipo_relacion}]->(b:{etiqueta2} {{{id_propiedad2}: $id_valor2}}),
              (b)-[r2:{tipo_relacion}]->(a)
        SET r1.esAmigo = True, r2.esAmigo = True
        RETURN r1, r2
        """
        result = neo4j_conn.execute_query(query_verificar, {"id_valor1": id_valor1, "id_valor2": id_valor2})
        return result  # Devolver el resultado actualizado

    except Exception as e:
        print("Error al gestionar la relación y actualizar la propiedad esAmigo:", e)
        raise
    
def listar_nodos(etiqueta, filtros=None):
    """
    Listar nodos de una etiqueta específica con filtros opcionales.
    
    Args:
        etiqueta (str): Etiqueta de los nodos a listar.
        filtros (dict): Diccionario con filtros opcionales.

    Returns:
        list: Lista de nodos que coinciden con los filtros.
    """
    # Construir filtros en la consulta si existen
    where_clause = ""
    params = {}
    if filtros:
        where_clauses = []
        for key, value in filtros.items():
            where_clauses.append(f"n.{key} = ${key}")
            params[key] = value
        where_clause = f"WHERE {' AND '.join(where_clauses)}"

    query = f"MATCH (n:{etiqueta}) {where_clause} RETURN n"
    return [record["n"] for record in neo4j_conn.query(query, params)]