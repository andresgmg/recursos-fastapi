from model.handle_db import Handle_DB
from werkzeug.security import generate_password_hash

"""
En resumen, esta clase define un usuario con sus atributos y tiene métodos para agregar un ID único al usuario,
cifrar su contraseña, e insertarlo en la base de datos.
"""

class User():
    # Define un diccionario vacío llamado data_user que almacena los datos de usuario
    data_user = {}

    # Define el constructor de la clase, recibe el parámetro data_user y crea una instancia de Handle_DB()
    def __init__(self, data_user):
        self.db = Handle_DB()
        self.data_user = data_user

    # Define el método create_user() que cifra la contraseña del usuario y luego inserta los datos en la base de datos
    def create_user(self):
        # Agrega un ID único al diccionario data_user
        self._add_id()

        # Cifra la contraseña del usuario usando la función generate_password_hash() de werkzeug.security
        self._psw_encrypt()

        # Inserta los datos de usuario cifrados en la base de datos utilizando el método insert() de Handle_DB()
        self.db.insert(self.data_user)

    # Define el método _add_id() para agregar un ID único al diccionario data_user
    def _add_id(self):
        # Recupera todos los usuarios de la base de datos
        user = self.db.get_all()

        # Obtiene el último usuario registrado
        one_user = user[-1]

        # Genera un nuevo ID único para el usuario basado en el número de ID del último usuario registrado
        id_user = int(one_user[0])
        self.data_user["id"] = str(id_user+1)

    # Define el método _psw_encrypt() para cifrar la contraseña del usuario
    def _psw_encrypt(self):
        # Cifra la contraseña del usuario utilizando la función generate_password_hash() de werkzeug.security
        self.data_user["password_user"] = generate_password_hash(self.data_user["password_user"], "pbkdf2:sha256:30", 30)