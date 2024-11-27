from werkzeug.security import generate_password_hash, check_password_hash
import requests
import re
from utils.db import get_connection
from utils.neo4j import neo4j_conn
from flask import session

def save_user(username, password, mail, name, bio, dob, gender):

    """
    guarda un nuevo usuario en la base de datos SQL y registra su ID en NEO4J-

    Parametros:
       - username (str): Nombre de usuario único.
       - password (str): Contraseña del usuario en texto plano.
       - mail (str): Correo electirnico o numeor de telefono.
       - bio (str): Biografia del usuario.
       - dob(str): Fecha de nacimiento
       - gender (str): Genero


    Flujo: 

      1. ** Encriptar la contraseña**:
         Utilizamos 'generate_password_hash' para guardar la contraseña de forma segura. 

      2. ** Validar el campo mail **:
        Determina si mail es un correo electrónico o un numero de telefono:
        - Si es un correo electronico valido, lo guarda en 'email'
        - Si es un numero de telefono valido, lo guarda en phone.
        - Lanza un ValueError si no es valido

      3. ** Descarga una imagen de foto de perfil predeterminada **
        Descarga la imagen desde una URL y lo convierte en binario.
        - Lanza un ValueError si no se pudo descargar.

      4. ** INSERTAR  datos en la base de datos SQL**
         - Inserta los datos del usuario en la tabla Persona
         - Confirma la inserción con 'connection.commit'
         - Obtenemos el ultimo ID registrado.

      5. **Registrar el usuario en NEO4J**:
         - Utiliza el 'idPersona' para crear o actualizar un nodo en la base de datos Neo4j.
         - Lanza la excepcion en caso de errores.

    Manejo de Errores:
        - **ValueError**: Si la validación de correo o teléfono falla o si la imagen no se puede descargar.
        - **Excepciones generales**: Captura errores durante la inserción en SQL o Neo4j y realiza un rollback en SQL si es necesario.

    Excepciones:
        - Propaga excepciones si hay errores durante la conexión o consultas en Neo4j.

    Returns:
        None. Los errores se imprimen o se lanzan como excepciones.

    """
    # Encriptar la contraseña
    hashed_password = generate_password_hash(password)

    # Validar si el dato es correo electrónico o número de teléfono
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', mail):
        email = mail
        phone = None
    elif re.match(r'^\d{9,15}$', mail):
        email = None
        phone = mail
    else:
        raise ValueError("El dato proporcionado para 'mail' no es válido como correo electrónico ni como número de teléfono.")

    # Descargar y convertir la imagen a binario
    response = requests.get("https://i.ibb.co/FYb5zQx/a80e3690318c08114011145fdcfa3ddb.jpg")

    if response.status_code == 200:
        profile_picture = response.content
        print("Imagen descargada correctamente")
    else:
        print("Error al descargar la imagen:", response.status_code)
        raise ValueError("No se pudo descargar la imagen de perfil.")

    # Insertar los datos en la base de datos y obtener el ID del usuario insertado
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Inserción de datos
            sql = """
                INSERT INTO Persona 
                (Nombre, UserName, FechaNacimiento, CorreoElectronico, Celular, contraseña, FechaCreacionCuenta, FotoPerfil, Genero, descripcion) 
                VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s)
            """
            print("Datos que se insertarán en la base de datos:", (name, username, dob, email, phone, hashed_password, gender, bio))
            cursor.execute(sql, (name, username, dob, email, phone, hashed_password, profile_picture, gender, bio))

            # Obtener el ID del último registro insertado
            cursor.execute("SELECT LAST_INSERT_ID() AS idPersona")
            result = cursor.fetchone()
            id_persona = result['idPersona'] if result else None
        
        if not id_persona:
            raise Exception("No se pudo obtener el ID del usuario insertado en SQL.")
        
        # Registrar el ID del usuario en Neo4j
        try:
            query = """
            MERGE (p:Persona {idPersona: $idPersona})
            RETURN p
            """
            print("Consulta que se enviará a Neo4j:", query)
            print("Datos que se enviarán a Neo4j:", {"idPersona": id_persona})

            neo4j_conn.execute_query(query, {"idPersona": id_persona})
        except Exception as e:
            raise Exception(f"Error al registrar en Neo4j: {str(e)}")

        # Si todo es exitoso, confirmar la transacción en SQL
        connection.commit()
        print("Registro exitoso en ambas bases de datos.")
    except Exception as e:
        # Revertir la transacción en caso de cualquier error
        connection.rollback()
        print("Error durante el registro:", e)
        raise e
    finally:
        connection.close()



def get_users():
    connection = get_connection()
    users = []
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT UserName, contraseña, 
                       COALESCE(CorreoElectronico, Celular) AS mail, 
                       Nombre, descripcion 
                FROM Persona
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                users.append((row['UserName'], row['contraseña'], row['mail'], row['Nombre'], row['descripcion']))
    except Exception as e:
        print("Error al obtener los usuarios:", e)
    finally:
        connection.close()  # Cierra la conexión
    return users


def update_user_data(username, password, mail, name, bio):
    hashed_password = generate_password_hash(password)
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """-
                UPDATE Persona
                SET contraseña = %s, CorreoElectronico = %s, Nombre = %s, descripcion = %s
                WHERE UserName = %s
            """
            cursor.execute(sql, (hashed_password, mail, name, bio, username))
            connection.commit()

            # Verifica si se actualizó alguna fila
            if cursor.rowcount == 0:
                raise ValueError(f"No se encontró el usuario con username '{username}'")
    except Exception as e:
        connection.rollback()
        print("Error al actualizar el usuario:", e)
        raise  # Relanza la excepción para manejarla en la capa superior
    finally:
        connection.close()



def login_user(username, password):
    """
    Autentica a un usuario validando sus credenciales con la base de datos.

    Parámetros:
       username (str): Nombre de usuario proporcionado por el cliente.
       password (str): Contraseña proporcionada por el cliente.

    Flujo: 
       1. Establece una conexión a la base de datos usando get_connection().
       2. Realiza una consulta SQL para obtener los datos del usuario.
       3. Verifica si la contraseña proporcionada coincide con la contraseña almacenada (hashed).
       4. Si las credenciales son válidas, devuelve los datos del usuario.
       5. Si las credenciales son incorrectas, devuelve None.
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Consulta SQL para obtener el usuario por su nombre de usuario
            sql = "SELECT idPersona, username, contraseña FROM Persona WHERE username = %s"
            cursor.execute(sql, (username,))
            user = cursor.fetchone()  # Obtenemos el primer (y único) resultado

        if user:  # Si el usuario existe
            stored_password = user['contraseña']  # Contraseña almacenada en la base de datos
            if check_password_hash(stored_password, password):  # Verifica si la contraseña es correcta
                return user  # Si la contraseña es correcta, retorna los datos del usuario
            else:
                return None  # Si la contraseña es incorrecta
        else:
            return None  # Si el usuario no existe

    except Exception as e:
        print(f"Error al intentar autenticar al usuario: {e}")
        return None