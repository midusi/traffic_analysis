import unittest
from backend.models.usuario import buscar_usuario_por_email
from .. import BaseTestClass


class RegistroTestCase(BaseTestClass):

    def setUp(self):
        super().setUp()

        self.response = self.app.post(
            "/api/registro/",
            json={
                "nombre": "Juan",
                "apellido": "Pérez",
                "email": "juan.perez@example.com",
                "admin": False,
            },
        )

    def test_registro_exitoso(self):
        """Test para un registro exitoso."""

        self.assertEqual(self.response.status_code, 200)
        self.assertIn("message", self.response.get_json())

    def test_registro_email_ya_registrado(self):
        """Test para el caso en que el email ya está registrado."""

        # Se intenta registrar de nuevo con el mismo email
        response = self.app.post(
            "/api/registro/",
            json={
                "nombre": "Juan",
                "apellido": "Pérez",
                "email": "juan.perez@example.com",
                "admin": False,
            },
        )
        self.assertEqual(response.status_code, 422)
        self.assertIn("error", response.get_json())

    def test_registro_falta_json(self):
        """Test para el caso en que falta el contenido JSON."""

        response = self.app.post("/api/registro/")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_registro_json_invalido(self):
        """Test para el caso en que el JSON es inválido."""

        response = self.app.post(
            "/api/registro/", data="Invalid JSON"  # Envía datos no JSON
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_registro_validacion_fallida(self):
        """Test para el caso en que la validación del JSON falla."""

        response = self.app.post(
            "/api/registro/",
            json={
                "nombre": "",  # Nombre vacío que debería fallar la validación
                "apellido": "Pérez",
                "email": "juan.perez@example.com",
                "admin": False,
            },
        )
        self.assertEqual(response.status_code, 422)
        self.assertIn("errors", response.get_json())

    def test_confirmar_registro_exitoso(self):
        """Test para confirmar el registro exitosamente."""

        usuario = buscar_usuario_por_email("juan.perez@example.com")
        token = usuario.token

        # Luego se confirma el registro usando el token
        response = self.app.post(
            "/api/registro/confirmar",
            json={"token": token, "password": "nueva_password"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.get_json())

    def test_confirmar_registro_token_invalido(self):
        """Test para confirmar el registro con un token inválido."""

        response = self.app.post(
            "/api/registro/confirmar",
            json={"token": "token_invalido", "password": "nueva_password"},
        )
        self.assertEqual(response.status_code, 422)
        self.assertIn("error", response.get_json())

    def test_confirmar_registro_falta_json(self):
        """Test para el caso en que falta el contenido JSON."""

        response = self.app.post("/api/registro/confirmar")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_confirmar_registro_json_invalido(self):
        """Test para el caso en que el JSON es inválido."""

        response = self.app.post(
            "/api/registro/confirmar", data="Invalid JSON"  # Envía datos no JSON
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_confirmar_registro_validacion_fallida(self):
        """Test para el caso en que la validación del JSON falla."""

        response = self.app.post(
            "/api/registro/confirmar",
            json={"token": "", "password": "nueva_password"},  # Token vacío
        )
        self.assertEqual(response.status_code, 422)
        self.assertIn("error", response.get_json())


if __name__ == "__main__":
    unittest.main()
