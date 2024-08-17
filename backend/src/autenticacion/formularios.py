from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, validators, SelectField
from wtforms.validators import InputRequired, Length


class RegistroSimpleForm(FlaskForm):
    nombre = StringField("Nombre", [InputRequired(), validators.Length(min=3, max=25)])
    apellido = StringField(
        "Apellido", [InputRequired(), validators.Length(min=3, max=25)]
    )
    email = EmailField("Email", validators=[InputRequired(), Length(max=50)])


class ConfirmarRegistroForm(FlaskForm):
    username = StringField(
        "Usuario", validators=[InputRequired(), Length(min=3, max=50)]
    )

    password = PasswordField(
        "Contraseña",
        [
            InputRequired(),
            Length(min=3, max=255),
            validators.EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Repetir contraseña")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(), Length(max=50)])

    password = PasswordField("Contraseña", [InputRequired(), Length(min=3, max=255)])


class CreateForm(FlaskForm):
    username = StringField(
        "Nombre de usuario", [InputRequired(), validators.Length(min=3, max=25)]
    )
    password = PasswordField(
        "Contraseña", [InputRequired(), validators.Length(min=3, max=250)]
    )
    email = EmailField("Email", validators=[InputRequired(), Length(max=50)])
    nombre = StringField("Nombre", [InputRequired(), validators.Length(min=3, max=25)])
    apellido = StringField(
        "Apellido", [InputRequired(), validators.Length(min=3, max=25)]
    )
    rol = SelectField(
        "Rol",
        validators=[InputRequired()],
        choices=["Superadmin", "Dueño", "Operador", "Administrador"],
    )
    institucion = SelectField(
        "Institución",
        validators=[InputRequired()],
    )


class UpdateForm(FlaskForm):
    username = StringField(
        "Nombre de usuario", [InputRequired(), validators.Length(min=3, max=25)]
    )
    email = EmailField("Email", validators=[InputRequired(), Length(max=50)])
    nombre = StringField("Nombre", [InputRequired(), validators.Length(min=3, max=25)])
    apellido = StringField(
        "Apellido", [InputRequired(), validators.Length(min=3, max=25)]
    )

class AgregarInstitucionForm(FlaskForm):
    rol = SelectField(
        "Rol",
        validators=[InputRequired()],
        choices=["Dueño", "Operador", "Administrador"],
    )
    institucion = SelectField(
        "Institución",
        validators=[InputRequired()],
    )
