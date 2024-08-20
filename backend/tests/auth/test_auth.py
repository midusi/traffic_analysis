import unittest
from flask_jwt_extended import create_access_token
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


if __name__ == "__main__":
    unittest.main()
