import unittest
from backend.models.database import db
from backend.models.usuario import (
    Usuario,
    crear_usuario,
    crear_usuario_password,
    buscar_usuario_por_email,
    chequear_usuario,
)
from .. import BaseTestClass
from backend.models.usuario import update_usuario


class UsuarioTestCase(BaseTestClass):
    def setUp(self):
        super().setUp()
        crear_usuario_password(
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            admin=True,
            password="password",
        )

    def test_crear_usuario(self):
        crear_usuario(
            nombre="Admin", apellido="Messi", email="admin@example.com", admin=True
        )
        # Verifica que el usuario fue creado en la base de datos
        usuario = Usuario.query.filter_by(email="admin@example.com").first()
        self.assertIsNotNone(usuario)
        self.assertIsNotNone(usuario.password)
        self.assertEqual(usuario.nombre, "Admin")
        self.assertEqual(usuario.apellido, "Messi")
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
        usuario = buscar_usuario_por_email("juan.perez@example.com")
        update_usuario(
            id=usuario.id,
            email=usuario.email,
            nombre="Pepito",
            apellido="Lopez",
            activo=False,
            admin=False,
        )
        usuario = buscar_usuario_por_email("juan.perez@example.com")
        self.assertEqual(usuario.nombre, "Pepito")
        self.assertEqual(usuario.apellido, "Lopez")
        self.assertEqual(usuario.email, "juan.perez@example.com")
        self.assertFalse(usuario.activo)
        self.assertFalse(usuario.admin)

    def test_chequear_usuario(self):
        usuario = chequear_usuario("juan.perez@example.com", "password")
        self.assertIsNotNone(usuario)


if __name__ == "__main__":
    unittest.main()
