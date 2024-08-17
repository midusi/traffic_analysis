from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, validators,SelectField
from wtforms.validators import InputRequired, Length


class CreateForm(FlaskForm):
    nombre = StringField("Nombre del servicio", [InputRequired(), validators.Length(min=3, max=25)])

    descripcion = StringField("Descripción", [InputRequired(), validators.Length(min=3, max=250)])

    palabras_claves = StringField("Palabras clave (separar por comas)", [InputRequired(), validators.Length(min=3, max=210)])

    tipo = SelectField("Tipo de servicio", validators=[InputRequired()])


