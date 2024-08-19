import unittest
from backend.models.database import db
from backend.app import app
from backend.models.usuario import crear_usuario, buscar_usuario_por_email
from backend.models.usuario.usuario import Usuario
from .. import BaseTestClass
from backend.models.usuario import update_usuario


class UsuarioTestCase(BaseTestClass):

    def test_crear_usuario(self):
        # Llama a la función para crear un usuario
        crear_usuario(
            nombre="Juan", apellido="Pérez", email="juan.perez@example.com", admin=True
        )

        # Verifica que el usuario fue creado en la base de datos
        usuario = Usuario.query.filter_by(email="juan.perez@example.com").first()
        self.assertIsNotNone(usuario)
        self.assertIsNotNone(usuario.password)
        self.assertEqual(usuario.nombre, "Juan")
        self.assertEqual(usuario.apellido, "Pérez")
        self.assertTrue(usuario.activo)
        self.assertTrue(usuario.admin)

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

    def test_modificar_usuario(self):
        crear_usuario(
            nombre="Juan", apellido="Pérez", email="juan.perez@gmail.com", admin=True
        )
        usuario = buscar_usuario_por_email("juan.perez@gmail.com")
        update_usuario(
            id=usuario.id,
            email=usuario.email,
            nombre="Pepito",
            apellido="Lopez",
            activo=False,
            admin=False,
        )
        usuario = buscar_usuario_por_email("juan.perez@gmail.com")
        self.assertEqual(usuario.nombre, "Pepito")
        self.assertEqual(usuario.apellido, "Lopez")
        self.assertEqual(usuario.email, "juan.perez@gmail.com")
        self.assertFalse(usuario.activo)
        self.assertFalse(usuario.admin)


if __name__ == "__main__":
    unittest.main()
