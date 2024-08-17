from src.core.autenticacion_oauth import google
from flask import Blueprint, redirect, url_for, session, jsonify, flash
from src.core.autenticacion import (
    buscar_usuario_por_email,
)
from src.web.controllers.autenticacion.registro import crear_usuario_mandar_mail

oauth_bp = Blueprint("oauth", __name__, url_prefix="/oauth")


@google.tokengetter
def get_google_oauth_token():
    return session.get("google_token")


@oauth_bp.route("/quiensoy")
def index():
    if "google_token" in session:
        me = google.get("userinfo")
        return jsonify({"data": me.data})

    return "Hay que loguearse con google para ver esto."


@oauth_bp.route("/autorizarLogin")
def autorizar_login():
    return google.authorize(callback=url_for("oauth.login", _external=True))


@oauth_bp.route("/login/callback")
def login():
    response = google.authorized_response()
    if response is None or response.get("access_token") is None:
        return "Falló el login."

    session["google_token"] = (response["access_token"], "")
    user = google.get("userinfo")

    mensaje = "La sesión se inició correctamente"
    if not buscar_usuario_por_email(user.data["email"]):
        crear_usuario_mandar_mail(
            user.data["email"], user.data["given_name"], user.data["family_name"]
        )
        session["usuario"] = user.data["email"]

        mensaje = (
            "Se ha registrado correctamente, se ha enviado un mail de confirmación."
        )

    session["usuario"] = user.data["email"]
    flash(mensaje, "success")
    return redirect(url_for("home"))
