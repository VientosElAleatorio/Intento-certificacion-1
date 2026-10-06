import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Pelicula:
    def __init__(self, data):
        self.id = data["id"]
        self.titulo = data["titulo"]
        self.director = data["director"]
        self.fecha_estreno = data["fecha_estreno"]
        self.sinopsis = data["sinopsis"]
        self.usuario_id = data["usuario_id"]

    @classmethod
    def mostrar_todas(cls):
        query = "SELECT * FROM peliculas;"
        resultados = connectToMySQL("esquema_cinepedia").query_db(query)
        return [cls(resultado) for resultado in resultados] if resultados else []
    @classmethod
    def guardar(cls, datos):
        query = """
            INSERT INTO peliculas (titulo, director, fecha_estreno, sinopsis, usuario_id)
            VALUES (%(titulo)s, %(director)s, %(fecha_estreno)s, %(sinopsis)s, %(usuario_id)s);
        """
        return connectToMySQL("esquema_cinepedia").query_db(query, datos)
    @classmethod
    def buscar_por_id(cls, datos):
        query = "SELECT * FROM peliculas WHERE id = %(id)s;"
        resultados = connectToMySQL("esquema_cinepedia").query_db(query, datos)
        return cls(resultados[0]) if resultados else None
    @classmethod
    def actualizar(cls, datos):
        query = """
            UPDATE peliculas
            SET titulo = %(titulo)s, director = %(director)s, fecha_estreno = %(fecha_estreno)s, sinopsis = %(sinopsis)s
            WHERE id = %(id)s;
        """
        return connectToMySQL("esquema_cinepedia").query_db(query, datos)