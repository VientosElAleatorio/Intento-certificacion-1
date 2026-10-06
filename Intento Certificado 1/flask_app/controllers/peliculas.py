from flask import flash, redirect, render_template, request, session
from flask_app import app
from flask_app.models.pelicula import Pelicula
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt


@app.route("/cine/nueva")
def nueva_pelicula():
    if "usuario_id" not in session:
        return redirect("/")
    usuario = Usuario.buscar_por_id({"id": session["usuario_id"]})
    if not usuario:
        return redirect("/")

    return render_template("nueva_peli.html")


@app.route("/cine/crear", methods=["POST"])
def crear_pelicula():
    if "usuario_id" not in session:
        return redirect("/")
    usuario = Usuario.buscar_por_id({"id": session["usuario_id"]})
    if not usuario:
        return redirect("/")
    datos = {**request.form, "usuario_id": session["usuario_id"]}
    Pelicula.guardar(datos)
    return redirect("/cine")
