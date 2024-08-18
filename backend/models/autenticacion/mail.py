from flask import Flask
from flask_mail import Mail
from flask_mail import Message
from src.web.helpers.produccion import es_produccion

mail = Mail()


def init_app(app):
    """Inicializa la aplicacion con flask mail"""
    mail.init_app(app)


def enviar_mail(asunto, destinatario, html="", mensaje=""):
    """
    Envía un mail real si está en produccion,
    sino se imprime en consola.
    """

    if es_produccion:
        msg = Message(asunto, recipients=[destinatario], html=html, body=mensaje)
        mail.send(msg)
    else:
        print(
            "Correo enviado a: "
            + destinatario
            + " asunto: "
            + asunto
            + " mensaje: "
            + mensaje
            + " html: "
            + html
        )
