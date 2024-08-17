from flask_wtf import FlaskForm
from wtforms import SelectField, EmailField
from wtforms.validators import InputRequired, Length


class CreateForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(), Length(max=50)])
    rol = SelectField("Rol", choices=["Operador", "Administrador"])
