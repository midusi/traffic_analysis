from src.web.helpers.autenticacion import check_mantenimiento, necesita_institucion_activa
from src.web.controllers.autenticacion.registro import registro_bp
from src.web.controllers.autenticacion.acceso import acceso_bp
from src.web.controllers.configuracion import configuracion_bp
from src.web.api.autenticacion import api_autenticacion_bp
from src.web.api.perfil import api_perfil_bp
from src.web.api.institucion import api_instituciones_bp
from src.web.api.servicio import api_servicios_bp
from src.web.api.solicitud import api_solicitudes_bp
from src.web.api.stats import api_stats_bp

from src.web.controllers.usuarios_institucion import usuarios_institucion_bp
from src.web.controllers.instituciones import instituciones_bp
from src.web.controllers.usuarios import usuarios_bp
from src.web.controllers.servicios import servicios_bp
from src.web.controllers.solicitudes import solicitudes_bp
from src.web.controllers.oauth import oauth_bp

def registrar_bps(app):
    """
    Registra los blueprints que se levantan al incio
    """
    @usuarios_institucion_bp.before_request
    @servicios_bp.before_request
    @solicitudes_bp.before_request
    @check_mantenimiento()
    @necesita_institucion_activa
    def before_request():
        pass

    @registro_bp.before_request
    @api_autenticacion_bp.before_request
    @api_perfil_bp.before_request
    @api_instituciones_bp.before_request
    @api_servicios_bp.before_request
    @api_solicitudes_bp.before_request
    @check_mantenimiento()
    def before_request():
        pass

    app.register_blueprint(registro_bp)
    app.register_blueprint(acceso_bp)
    app.register_blueprint(usuarios_institucion_bp)
    app.register_blueprint(instituciones_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(configuracion_bp)
    app.register_blueprint(api_autenticacion_bp)
    app.register_blueprint(api_perfil_bp)
    app.register_blueprint(api_instituciones_bp)
    app.register_blueprint(api_servicios_bp)
    app.register_blueprint(servicios_bp)
    app.register_blueprint(solicitudes_bp)
    app.register_blueprint(api_solicitudes_bp)
    app.register_blueprint(oauth_bp)
    app.register_blueprint(api_stats_bp)
