import unittest
from backend.models.database import db
from backend.models.usuario import (
    Usuario,
    crear_usuario,
    buscar_usuario_por_email,
    buscar_usuario_por_id,
    chequear_usuario,
    renovar_token,
    renovar_password,
    update_usuario,
)
from .. import BaseTestClass
from datetime import datetime, timedelta


class UsuarioTestCase(BaseTestClass):
    def setUp(self):
        super().setUp()
        self.usr = crear_usuario(
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@example.com",
            admin=True,
            password="password",
        )

    def test_crear_usuario(self):
        usuario = Usuario.query.filter_by(email="juan.perez@example.com").first()
        self.assertIsNotNone(usuario)
        self.assertIsNotNone(usuario.password)
        self.assertEqual(usuario.nombre, "Juan")
        self.assertEqual(usuario.apellido, "Pérez")
        self.assertTrue(usuario.activo)
        self.assertTrue(usuario.admin)
        self.assertIsNotNone(usuario.token)
        self.assertIsNotNone(usuario.token_expiracion)
        self.assertTrue(usuario.token_expiracion > datetime.now())

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
        usuario = self.usr
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

    def test_renovar_password_con_token_valido(self):
        # Generar un nuevo token para el usuario
        token = renovar_token(self.usr.id)

        # Intentar renovar la contraseña usando el token válido
        result = renovar_password("nueva_password", token)
        self.assertTrue(result)

        # Verificar que la contraseña se haya actualizado y que el token se haya invalidado
        usuario = buscar_usuario_por_id(self.usr.id)
        self.assertTrue(chequear_usuario(usuario.email, "nueva_password"))
        self.assertIsNone(usuario.token_expiracion)

    def test_renovar_password_con_token_invalido(self):
        # Intentar renovar la contraseña usando un token inválido
        result = renovar_password("nueva_password", "token_invalido")
        self.assertFalse(result)

        # Verificar que la contraseña no se haya actualizado
        usuario = buscar_usuario_por_id(self.usr.id)
        self.assertFalse(chequear_usuario(usuario.email, "nueva_password"))

    def test_renovar_token(self):
        # Generar un nuevo token para el usuario
        nuevo_token = renovar_token(self.usr.id)

        # Verificar que el token haya cambiado y que la fecha de expiración se haya actualizado
        usuario = buscar_usuario_por_id(self.usr.id)
        self.assertEqual(usuario.token, nuevo_token)
        self.assertGreater(usuario.token_expiracion, datetime.now())

    def test_renovar_password_con_token_expirado(self):
        # Generar un nuevo token y forzar su expiración
        token = renovar_token(self.usr.id)
        usuario = buscar_usuario_por_id(self.usr.id)
        usuario.token_expiracion = datetime.now() - timedelta(minutes=1)
        db.session.commit()

        # Intentar renovar la contraseña usando el token expirado
        result = renovar_password("nueva_password", token)
        self.assertFalse(result)

        # Verificar que la contraseña no se haya actualizado
        usuario = buscar_usuario_por_id(self.usr.id)
        self.assertFalse(chequear_usuario(usuario.email, "nueva_password"))


if __name__ == "__main__":
    unittest.main()
