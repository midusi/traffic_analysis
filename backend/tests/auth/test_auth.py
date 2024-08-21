import unittest
from backend.models.usuario import crear_usuario
from .. import BaseTestClass


class AutenticacionTestCase(BaseTestClass):

    def setUp(self):
        super().setUp()
        self.usr = crear_usuario(
            email="test@example.com",
            nombre="Juan",
            apellido="Pérez",
            password="password",
            admin=True,
        )

        self.response = self.app.post(
            "/api/auth/",
            json={"email": "test@example.com", "password": "password"},
        )

    def test_auth_success(self):
        """Test para autenticación exitosa."""

        self.assertEqual(self.response.status_code, 200)
        self.assertIn("token", self.response.get_json())

    def test_logout(self):
        """Test para el endpoint de logout."""

        token = self.response.get_json().get("token")
        headers = {"Authorization": f"Bearer {token}"}

        response = self.app.get("/api/auth/logout", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_profile_success(self):
        """Test para obtener el perfil del usuario autenticado."""

        # Simula la autenticación
        token = self.response.get_json().get("token")
        headers = {"Authorization": f"Bearer {token}"}

        response = self.app.get("/api/auth/me", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("email", response.get_json())

    def test_auth_missing_json(self):
        """Test cuando falta el contenido JSON en la solicitud."""

        response = self.app.post("/api/auth/")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_auth_invalid_json(self):
        """Test cuando el JSON es inválido."""

        response = self.app.post(
            "/api/auth/", data="Invalid JSON"  # Envía datos no JSON
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_auth_invalid_credentials(self):
        """Test cuando se proveen credenciales inválidas."""

        response = self.app.post(
            "/api/auth/",
            json={"email": "wrong@example.com", "password": "wrong_password"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", response.get_json())

    def test_registro_exitoso(self):
        """Test para un registro exitoso."""

        response = self.app.post(
            "/api/registro/",
            json={
                "nombre": "Juan",
                "apellido": "Pérez",
                "email": "juan.perez@example.com",
                "admin": False,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.get_json())

    def test_registro_email_ya_registrado(self):
        """Test para el caso en que el email ya está registrado."""

        # Primero se registra el usuario
        self.app.post(
            "/api/registro/",
            json={
                "nombre": "Juan",
                "apellido": "Pérez",
                "email": "juan.perez@example.com",
                "admin": False,
            },
        )

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


if __name__ == "__main__":
    unittest.main()
