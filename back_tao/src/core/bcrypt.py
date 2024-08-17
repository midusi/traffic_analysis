from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


# es como un inicializador, ahora la variable bcrypt de aca arriba puedo importarla para usarla en otros archivos(con la db hicimos lo mismo)
def init_app():
    bcrypt.init_app(app)
