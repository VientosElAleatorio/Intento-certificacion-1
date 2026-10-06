from flask import flash, redirect, render_template, request, session
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/registrar", methods=["POST"])
def registrar():
    if not Usuario.validar_registro(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form["password"]).decode(
        "utf-8"
    )
    datos = {**request.form, "password": pw_hash}

    session["usuario_id"] = Usuario.guardar(datos)
    return redirect("/cine")


@app.route("/login", methods=["POST"])
def login():
    usuario = Usuario.buscar_por_email(request.form)
    if not usuario:
        return redirect("/")
    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        return redirect("/")
    session["usuario_id"] = usuario.id
    return redirect("/cine")


@app.route("/cine")
def cine():
    if "usuario_id" not in session:
        return redirect("/")
    usuario = Usuario.buscar_por_id({"id": session["usuario_id"]})
    if not usuario:
        return redirect("/")
    return render_template("cine.html", usuario=usuario, usuarios=Usuario.buscar_todos())


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")