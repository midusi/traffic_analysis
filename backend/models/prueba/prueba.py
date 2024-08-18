from backend.models.database import db

class Prueba(db.Model):
    __tablename__="prueba"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f"id: {self.id}, Nombre: {self.name}"