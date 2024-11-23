
# Creación de una Red Social en Neo4j

Se detalla las consultas utilizadas para construir y estructurar nuestra red social en Neo4j. Cada sección incluye una explicación de las operaciones realizadas.

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
CREATE (:Persona {idPersona: 7});
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
MATCH (p1:Persona {idPersona: 1}), (p2:Persona {idPersona: 2}) CREATE (p1)-[:SIGUE {esAmigo: False}]->(p2);
MATCH (p3:Persona {idPersona: 1}), (p4:Persona {idPersona: 3}) CREATE (p3)-[:SIGUE {esAmigo: False}]->(p4);
MATCH (p5:Persona {idPersona: 2}), (p6:Persona {idPersona: 4}) CREATE (p5)-[:SIGUE {esAmigo: False}]->(p6);
MATCH (p7:Persona {idPersona: 3}), (p8:Persona {idPersona: 5}) CREATE (p7)-[:SIGUE {esAmigo: False}]->(p8);
```

### Relación de Pertenencia a Grupo
Se establece que una persona pertenece a un grupo:

```cypher
MATCH (p:Persona {idPersona: 1}), (g:Grupo {idGrupo: 1}) CREATE (p)-[:ES_MIEMBRO_DE]->(g);
MATCH (p:Persona {idPersona: 7}), (g:Grupo {idGrupo: 1}) CREATE (p)-[:ES_MIEMBRO_DE]->(g);
```

### Relación de creador del Grupo
Se establece que una persona creo un grupo:
```cypher
MATCH (p:Persona {idPersona: 1}), (g:Grupo {idGrupo: 1}) CREATE (p)-[:CREADOR_DE]->(g);
```

### Relación de Reacción a Publicación
Se define una reacción que una persona realiza sobre una publicación:

```cypher
MATCH (p:Persona {idPersona: 1}), (pub:Publicacion {idPublicacion: 1}) CREATE (p)-[:REACCIONA {tipoReaccion: 'No me Gusta', idReaccion: 1, nombreReaccion: 'dislike'}]->(pub);
MATCH (p:Persona {idPersona: 2}), (pub:Publicacion {idPublicacion: 1}) CREATE (p)-[:REACCIONA {tipoReaccion: 'Me Gusta', idReaccion: 2, nombreReaccion: 'Like'}]->(pub);
MATCH (p:Persona {idPersona: 3}), (pub:Publicacion {idPublicacion: 1}) CREATE (p)-[:REACCIONA {tipoReaccion: 'Me Encanta', idReaccion: 3, nombreReaccion: 'Love'}]->(pub);
```

### Relación de Comentario en Publicación
Se añade un comentario realizado por una persona sobre una publicación:

```cypher
MATCH (p:Persona {idPersona: 1}), (pub:Publicacion {idPublicacion: 1}) CREATE (p)-[:COMENTA {texto: '¡Gran publicación!', fechaComentario: datetime()}]->(pub);
MATCH (p:Persona {idPersona: 1}), (pub:Publicacion {idPublicacion: 1}) CREATE (p)-[:COMENTA {texto: '¡Me encanta este tema!', fechaComentario: datetime('2024-11-22T15:30:00')}]->(pub);
MATCH (p:Persona {idPersona: 2}), (pub:Publicacion {idPublicacion: 1}) CREATE (p)-[:COMENTA {texto: 'Muy interesante.', fechaComentario: datetime('2024-11-22T16:00:00')}]->(pub);
```

### Relación de Influencer
Un nodo de **Influencer** se conecta con una persona para indicar que esta tiene cierta influencia:

```cypher
MATCH (p:Persona {idPersona: 1}) CREATE (p)-[:ES_INFLUENCER]->(:Influencer {idInfluencer: 1});
MATCH (i:Influencer {idInfluencer: 1}), (pub:Publicacion {idPublicacion: 1}) CREATE (i)-[:PUBLICA]->(pub);
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
MATCH (a:TipoInteres {nombre: 'Generales'}) CREATE (:Interes {nombre: 'Tecnología'})-[:PERTENECE_A]->(a), (:Interes {nombre: 'Arte'})-[:PERTENECE_A]->(a), (:Interes {nombre: 'Música'})-[:PERTENECE_A]->(a);
MATCH (b:TipoInteres {nombre: 'Tecnológicos'}) CREATE (:Interes {nombre: 'Inteligencia Artificial'})-[:PERTENECE_A]->(b), (:Interes {nombre: 'Desarrollo Web'})-[:PERTENECE_A]->(b), (:Interes {nombre: 'Blockchain'})-[:PERTENECE_A]->(b);
MATCH (c:TipoInteres {nombre: 'Entretenimiento'}) CREATE (:Interes {nombre: 'Anime'})-[:PERTENECE_A]->(c), (:Interes {nombre: 'Cine'})-[:PERTENECE_A]->(c), (:Interes {nombre: 'Videojuegos'})-[:PERTENECE_A]->(c);
MATCH (d:TipoInteres {nombre: 'Deportivos'}) CREATE (:Interes {nombre: 'Fútbol'})-[:PERTENECE_A]->(d), (:Interes {nombre: 'Baloncesto'})-[:PERTENECE_A]->(d), (:Interes {nombre: 'Yoga'})-[:PERTENECE_A]->(d);
MATCH (e:TipoInteres {nombre: 'Estilo de Vida'}) CREATE (:Interes {nombre: 'Salud y bienestar'})-[:PERTENECE_A]->(e), (:Interes {nombre: 'Minimalismo'})-[:PERTENECE_A]->(e);
MATCH (f:TipoInteres {nombre: 'Cocina y Gastronomía'}) CREATE (:Interes {nombre: 'Comida vegana'})-[:PERTENECE_A]->(f), (:Interes {nombre: 'Repostería'})-[:PERTENECE_A]->(f);
MATCH (g:TipoInteres {nombre: 'Especializados'}) CREATE (:Interes {nombre: 'Astronomía'})-[:PERTENECE_A]->(g), (:Interes {nombre: 'Filosofía'})-[:PERTENECE_A]->(g);
MATCH (h:TipoInteres {nombre: 'Creativos'}) CREATE (:Interes {nombre: 'Pintura'})-[:PERTENECE_A]->(h), (:Interes {nombre: 'Diseño gráfico'})-[:PERTENECE_A]->(h);
MATCH (i:TipoInteres {nombre: 'En Tendencia'}) CREATE (:Interes {nombre: 'NFTs'})-[:PERTENECE_A]->(i), (:Interes {nombre: 'Criptomonedas'})-[:PERTENECE_A]->(i);
```
### Relacionar personas con intereses
Se conecta a las personas con los temas que le interesan:
```cypher
MATCH (p:Persona {idPersona: 1}), (i:Interes {nombre: 'Inteligencia Artificial'}) CREATE (p)-[:INTERESADO_EN]->(i);
MATCH (p:Persona {idPersona: 1}), (i:Interes {nombre: 'Tecnología'}) CREATE (p)-[:INTERESADO_EN]->(i);
MATCH (p:Persona {idPersona: 2}), (i:Interes {nombre: 'Fútbol'}) CREATE (p)-[:INTERESADO_EN]->(i);
MATCH (p:Persona {idPersona: 2}), (i:Interes {nombre: 'Videojuegos'}) CREATE (p)-[:INTERESADO_EN]->(i);
MATCH (p:Persona {idPersona: 3}), (i:Interes {nombre: 'Cine'}) CREATE (p)-[:INTERESADO_EN]->(i);
MATCH (p:Persona {idPersona: 4}), (i:Interes {nombre: 'Repostería'}) CREATE (p)-[:INTERESADO_EN]->(i);
MATCH (p:Persona {idPersona: 5}), (i:Interes {nombre: 'Yoga'}) CREATE (p)-[:INTERESADO_EN]->(i);
MATCH (p:Persona {idPersona: 6}), (i:Interes {nombre: 'Criptomonedas'}) CREATE (p)-[:INTERESADO_EN]->(i);
MATCH (p:Persona {idPersona: 7}), (i:Interes {nombre: 'Arte'}) CREATE (p)-[:INTERESADO_EN]->(i);
```


### Relación Publicación-Interes
Se conecta una publicacion con un interes:
```cypher
MATCH (p:Publicacion {idPublicacion: 1}), (i:Interes {nombre: 'Tecnología'}) CREATE (p)-[:RELACIONADA_CON]->(i);
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
MATCH (p:Persona {idPersona: 1}), (e:Evento {idEvento: 1}) CREATE (p)-[:CREADOR_DE]->(e);
MATCH (p:Persona {idPersona: 2}), (e:Evento {idEvento: 2}) CREATE (p)-[:CREADOR_DE]->(e);
MATCH (p:Persona {idPersona: 3}), (e:Evento {idEvento: 1}) CREATE (p)-[:ASISTE_A]->(e);
MATCH (p:Persona {idPersona: 4}), (e:Evento {idEvento: 1}) CREATE (p)-[:ASISTE_A]->(e);
MATCH (p:Persona {idPersona: 5}), (e:Evento {idEvento: 2}) CREATE (p)-[:ASISTE_A]->(e);
MATCH (p:Persona {idPersona: 6}), (e:Evento {idEvento: 2}) CREATE (p)-[:ASISTE_A]->(e);
```

### Relación entre Eventos e Intereses
Los eventos se relacionan con intereses relevantes:

```cypher
MATCH (e:Evento {idEvento: 1}), (i:Interes {nombre: 'Inteligencia Artificial'}) CREATE (e)-[:RELACIONADO_CON]->(i);
MATCH (e:Evento {idEvento: 2}), (i:Interes {nombre: 'Desarrollo Web'}) CREATE (e)-[:RELACIONADO_CON]->(i);
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

## Vista del avance la base de datos no relacional Neo4j:
![image](https://github.com/user-attachments/assets/c7447c7a-cd4d-465a-b2de-1104eea2e892)

