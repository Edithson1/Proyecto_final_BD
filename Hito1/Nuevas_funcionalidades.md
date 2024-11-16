<p align="center">
  <a href="https://github.com/DenverCoder1/readme-typing-svg">
    <img src="https://readme-typing-svg.herokuapp.com?font=Time+New+Roman&color=F1C40F&size=25&center=true&vCenter=true&width=600&height=100&lines=UNIVERSIDAD+PERUANA+CAYETANO+HEREDIA">
  </a>
</p>

## Integrantes de equipo:
+ Aybar Escobar Edithson Ricardo
+ Llanos Angeles Leily Marlith 
+ Luque Mamani Magno Ricardo 
+ Mendoza Villar Antony Iván 
+ Quezada Marceliano Gian Carlos 
## Docente: 
+ Montalvo Garcia Peter Jhonatan 

<div align="center">
  <h1> Informe de Presentación del Trabajo: Nuevas funcionalidades al Modelamiento de Red Social para Seguimiento de Influencers  </h1>
</div>

## 1. Introducción

La red de streaming “Ok” busca modelar el comportamiento de sus influencers y su interacción en una red social. Este trabajo detalla el diseño de una base de datos que respalda las funcionalidades requeridas para gestionar usuarios, seguidores, influencers y publicaciones, así como nuevas funcionalidades añadidas para comentarios, reacciones, mensajes privados, seguidores mutuos y comunidades.

## 2. Especificaciones del Sistema

El modelamiento de la red social se basa en los siguientes requisitos y características:

- Una persona en la red social debe tener al menos uno de los siguientes campos (correo electrónico o celular) y de manera obligatoria: nombre y fecha de nacimiento.
- Una persona en la red social puede seguir a cero, uno o varias personas. Esto se conoce como el número de seguidores.
- Una persona puede dejar de seguir a otra persona y su número de seguidores disminuirá.
- Una persona tiene un número de seguidores (personas que lo siguen) y número de seguidos (personas a las que sigue).
- Se considera un influencer si una persona tiene más de 1000 seguidores y la cantidad de seguidos es menor al 10% de su total de seguidores. Una persona puede perder su rango de influencer si deja de cumplirse esa condición.
- Una persona que es influencer tendrá habilitada la opción de realizar videos especiales o subir fotos especiales, que la red promocionará más.
- Una persona puede tener cero, uno o varias publicaciones. Estas pueden ser en formato de video o imagen. Se debe guardar el tipo de formato y la URL donde se guarda esta información.
- Se debe guardar un historial de cuándo fueron influencers, qué usuario y por cuánto tiempo.

## 3. Estructura de la Base de Datos

La base de datos incluye las tablas y relaciones principales que permiten cumplir con los requisitos establecidos:

- **Tabla Persona**: Representa a cada usuario de la red social, almacenando su nombre, fecha de nacimiento, correo electrónico y celular.
- **Tabla Seguimiento**: Define la relación de seguimiento entre los usuarios, permitiendo saber quién sigue a quién. Esta tabla incluye un campo `Activo` para indicar si la relación está vigente.
- **Tabla Publicación**: Contiene las publicaciones de los usuarios, almacenando el tipo de formato (video o imagen) y la URL del archivo.
- **Tabla Influencer**: Registra a los usuarios que cumplen con los criterios para ser influencers.
- **Tabla Historial**: Almacena el historial de los períodos en los que un usuario fue influencer.

Además, un `Trigger update_influencer_status` mantiene automáticamente el estatus de influencer de los usuarios al realizar cambios en las relaciones de seguimiento.

## 4. Nuevos Casos de Uso

Para expandir la funcionalidad del sistema, se han añadido nuevos casos de uso que introducen relaciones adicionales:

- **Fechas de creación, descripciones y foto de perfil**:
  - Se añade en la tabla Persona los campos `FechaCreacionCuenta` (fecha y hora de creación), `descripcion` (descripción opcional) y `FotoPerfil` (URL de la imagen).
  - Se añade en la tabla Publicacion los campos `fechaPublicacion` (fecha y hora) y `descripcion`.

- **Comentarios en Publicaciones**:
  - Permite a los usuarios comentar en las publicaciones de otros usuarios.
  - Se añade la tabla `Comentario` con los campos `idComentario`, `texto`, `fechaComentario`, `Persona_idPersona` (autor del comentario) y `Publicacion_idPublicacion`.

- **Reacciones o "Me Gusta" en Publicaciones**:
  - Implementa un sistema de reacciones.
  - La tabla `Reaccion` contiene `idReaccion`, `tipoReaccion`, `Persona_idPersona` (usuario que reaccionó) y `Publicacion_idPublicacion`.

- **Mensajes Privados entre Usuarios**:
  - Añade la capacidad de enviar mensajes privados.
  - La tabla `Mensaje` incluye los campos `idMensaje`, `texto`, `fechaEnvio`, `Persona_idEmisor` y `Persona_idReceptor`.

- **Seguidores Mutuos o "Amigos"**:
  - Identifica relaciones de amistad entre usuarios que se siguen mutuamente.
  - Se añade un campo `esAmigo` en la tabla Seguimiento o se crea una vista que muestra únicamente las relaciones de amistad.

- **Grupos o Comunidades**:
  - Permite a los usuarios unirse a grupos de intereses comunes.
  - La tabla `Grupo` incluye `idGrupo`, `nombreGrupo` y `descripcion`, mientras que `MiembroGrupo` vincula usuarios con grupos.

## 5. Modelo de Base de Datos

El esquema de la base de datos incluye las nuevas tablas y relaciones entre ellas, optimizando la consulta de datos sobre seguidores, influencers, publicaciones y sus interacciones.

![modelo](https://github.com/user-attachments/assets/9323d0aa-4cb5-4e56-aacf-f57f27c74b99)


## 6. Conclusión

Este modelo de base de datos para la red social “Ok” satisface los requerimientos de seguimiento de influencers, gestión de publicaciones e interacciones sociales, y proporciona una estructura flexible para futuras expansiones. Las nuevas tablas implementadas facilitan funcionalidades clave, haciendo que el sistema sea robusto y extensible.

