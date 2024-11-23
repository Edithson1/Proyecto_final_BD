
# Creación de una Red Social en Neo4j

Este documento detalla las consultas utilizadas para construir y estructurar una red social en Neo4j. Cada sección incluye una explicación de las operaciones realizadas.

## Creación de Nodos

### Nodos de Persona
Se crean nodos para representar a las personas que forman parte de la red social:

```cypher
CREATE (:Persona {idPersona: 1});
CREATE (:Persona {idPersona: 2});
CREATE (:Persona {idPersona: 3});
CREATE (:Persona {idPersona: 4});
CREATE (:Persona {idPersona: 5});
CREATE (:Persona {idPersona: 6});
```

### Nodo de Grupo
Se define un nodo para representar un grupo temático en la red social:

```cypher
CREATE (:Grupo {idGrupo: 1, nombreGrupo: 'Grupo de Tecnología', descripcion: 'Intercambio de ideas sobre tecnología'});
```

### Nodo de Publicación
Se crean nodos para publicaciones dentro de la red social:

```cypher
CREATE (:Publicacion {idPublicacion: 1});
```

## Creación de Relaciones

### Relación de Seguimiento entre Personas
Se modela la relación de seguimiento donde una persona sigue a otra:

```cypher
MATCH (p1:Persona {idPersona: 1}), (p2:Persona {idPersona: 2})
CREATE (p1)-[:SIGUE {esAmigo: False}]->(p2);
```

### Relación de Pertenencia a Grupo
Se establece que una persona pertenece a un grupo:

```cypher
MATCH (p:Persona {idPersona: 1}), (g:Grupo {idGrupo: 1})
CREATE (p)-[:ES_MIEMBRO_DE]->(g);
```

### Relación de Reacción a Publicación
Se define una reacción que una persona realiza sobre una publicación:

```cypher
MATCH (p:Persona {idPersona: 1}), (pub:Publicacion {idPublicacion: 1})
CREATE (p)-[:REACCIONA {tipoReaccion: 'No me Gusta', idReaccion: 1, nombreReaccion: 'dislike'}]->(pub);
```

### Relación de Comentario en Publicación
Se añade un comentario realizado por una persona sobre una publicación:

```cypher
MATCH (p:Persona {idPersona: 1}), (pub:Publicacion {idPublicacion: 1})
CREATE (p)-[:COMENTA {texto: '¡Gran publicación!', fechaComentario: datetime()}]->(pub);
```

### Relación de Influencer
Un nodo de **Influencer** se conecta con una persona para indicar que esta tiene cierta influencia:

```cypher
MATCH (p:Persona {idPersona: 1})
CREATE (p)-[:ES_INFLUENCER]->(:Influencer {idInfluencer: 1});
```

## Organización de Intereses

### Creación de Tipos de Intereses
Se crean nodos que agrupan diferentes tipos de intereses:

```cypher
CREATE (:TipoInteres {nombre: 'Generales'});
CREATE (:TipoInteres {nombre: 'Tecnológicos'});
CREATE (:TipoInteres {nombre: 'Entretenimiento'});
CREATE (:TipoInteres {nombre: 'Deportivos'});
CREATE (:TipoInteres {nombre: 'Estilo de Vida'});
CREATE (:TipoInteres {nombre: 'Cocina y Gastronomía'});
CREATE (:TipoInteres {nombre: 'Especializados'});
CREATE (:TipoInteres {nombre: 'Creativos'});
CREATE (:TipoInteres {nombre: 'En Tendencia'});
```

### Relación entre Intereses y Tipos de Intereses
Se conecta cada interés con su categoría correspondiente:

```cypher
MATCH (a:TipoInteres {nombre: 'Generales'})
CREATE (:Interes {nombre: 'Tecnología'})-[:PERTENECE_A]->(a),
       (:Interes {nombre: 'Arte'})-[:PERTENECE_A]->(a),
       (:Interes {nombre: 'Música'})-[:PERTENECE_A]->(a);
```

## Eventos

### Creación de Nodos de Evento
Se definen eventos dentro de la red social:

```cypher
CREATE (:Evento {idEvento: 1, nombre: 'Conferencia de Tecnología', descripcion: 'Un evento para discutir las últimas tendencias en tecnología', fecha: date('2024-12-10')});
CREATE (:Evento {idEvento: 2, nombre: 'Hackathon', descripcion: 'Competencia de programación intensiva', fecha: date('2024-12-15')});
```

### Relación de Participación en Eventos
Se conecta a las personas que asisten a los eventos:

```cypher
MATCH (p1:Persona {idPersona: 3}), (e:Evento {idEvento: 1})
CREATE (p1)-[:ASISTE_A]->(e);
```

### Relación entre Eventos e Intereses
Los eventos se relacionan con intereses relevantes:

```cypher
MATCH (e:Evento {idEvento: 1}), (i:Interes {nombre: 'Inteligencia Artificial'})
CREATE (e)-[:RELACIONADO_CON]->(i);
```

## Búsquedas y Visualizaciones

### Registro de Búsquedas
Se crean nodos para almacenar búsquedas realizadas por las personas:

```cypher
CREATE (b:Busqueda {idBusqueda: 1, termino: 'Blockchain', fechaBusqueda: datetime('2024-11-22T10:00:00')});
MATCH (p:Persona {idPersona: 1}), (b:Busqueda {idBusqueda: 1})
CREATE (p)-[:REALIZA_BUSQUEDA]->(b);
```

### Registro de Visualizaciones
Se modelan las visualizaciones de contenido por parte de las personas:

```cypher
CREATE (v:Visualizacion {idVisualizacion: 1, tipoContenido: 'Publicación', idContenido: 1, fechaVisualizacion: datetime('2024-11-22T14:00:00')});
MATCH (p:Persona {idPersona: 1}), (v:Visualizacion {idVisualizacion: 1})
CREATE (p)-[:MIRA_CONTENIDO]->(v);
```
