import unittest
from backend.models.database import db
from backend.app import app
from backend.models.usuario import crear_usuario
from backend.models.usuario.usuario import Usuario
from backend.models.bcrypt import bcrypt


class UsuarioTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        # Crear contexto de la aplicación
        self.ctx = app.app_context()
        self.ctx.push()
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_crear_usuario(self):
        # Llama a la función para crear un usuario
        crear_usuario(nombre="Juan", apellido="Pérez", email="juan.perez@example.com")

        # Verifica que el usuario fue creado en la base de datos
        usuario = Usuario.query.filter_by(email="juan.perez@example.com").first()
        self.assertIsNotNone(usuario)
        self.assertIsNotNone(usuario.password)
        self.assertEqual(usuario.nombre, "Juan")
        self.assertEqual(usuario.apellido, "Pérez")
        self.assertTrue(usuario.activo)

    def test_nombre_demasiado_largo(self):
        nombre_largo = "a" * 26  # 26 caracteres, excede el límite de 25
        with self.assertRaises(Exception):
            usuario = Usuario(nombre=nombre_largo, email="test@example.com")
            db.session.add(usuario)
            db.session.commit()

    def test_email_demasiado_largo(self):
        email_largo = "a" * 51 + "@example.com"  # Excede el límite de 50 caracteres
        with self.assertRaises(Exception):
            usuario = Usuario(nombre="Juan", email=email_largo)
            db.session.add(usuario)
            db.session.commit()


if __name__ == "__main__":
    unittest.main()
