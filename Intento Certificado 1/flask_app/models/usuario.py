import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

# Configuración de constantes y expresiones regulares
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
BD = "esquema_cinepedia"


class Usuario:

    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"] 
        self.email = data["email"]
        self.password = data["password"]

    @classmethod
    def guardar(cls, datos):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, password)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);
        """
        return connectToMySQL(BD).query_db(query, datos)

    @classmethod
    def buscar_por_email(cls, datos):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultados = connectToMySQL(BD).query_db(query, datos)
        return cls(resultados[0]) if resultados else False

    @staticmethod
    def validar_registro(form):
        es_valido = True

        # Validación del Nombre
        if len(form["nombre"]) < 2:
            flash("El nombre debe tener al menos 2 letras", "registro")
            es_valido = False

        # Validación del Apellido (Evita fallos al intentar insertar un campo vacío)
        if len(form["apellido"]) < 2:
            flash("El apellido debe tener al menos 2 letras", "registro")
            es_valido = False

        # Validación del Correo Electrónico
        if not EMAIL_REGEX.match(form["email"]):
            flash("E-mail inválido", "registro")
            es_valido = False

        # Validación de Contraseñas
        if form["password"] != form["confirmar"]:
            flash("Las contraseñas no coinciden", "registro")
            es_valido = False

        return es_valido
    @classmethod
    def buscar_por_id(cls, datos):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        resultados = connectToMySQL(BD).query_db(query, datos)
        return cls(resultados[0]) if resultados else None
    @classmethod
    def buscar_todos(cls):
        query = "SELECT * FROM usuarios;"
        resultados = connectToMySQL(BD).query_db(query)
        return [cls(resultado) for resultado in resultados] if resultados else []