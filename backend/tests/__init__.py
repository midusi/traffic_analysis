import unittest
from backend.app import create_app
from backend.models.database import db


class BaseTestClass(unittest.TestCase):

    def setUp(self):
        app = create_app(env="testing")
        self.ctx = app.app_context()
        self.ctx.push()
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()
