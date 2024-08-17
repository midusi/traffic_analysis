from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired


class UpdateForm(FlaskForm):
    estado = SelectField("Estado de la solicitud", [InputRequired()])
    comentario = StringField("Observaciones sobre el cambio de estado")