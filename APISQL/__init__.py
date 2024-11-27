from flask import Flask
from routes.auth_routes import auth_bp
#from api.routes.user_routes import user_bp
#from api.routes.file_routes import file_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Registrar Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    #app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(file_bp, url_prefix='/files')

    return app
