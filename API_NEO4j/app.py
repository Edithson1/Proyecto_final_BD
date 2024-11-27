from flask import Flask
from controllers.usuario_controller import usuario_bp
from controllers.group_controller import group_controller
from controllers.publication_controller import publication_controller
from controllers.interes_controller import interes_controller
from controllers.evento_controller import evento_controller 
from controllers.influencer_controller import influencer_controller
app = Flask(__name__)

# Registrar Blueprints
app.register_blueprint(usuario_bp, url_prefix='/api')
app.register_blueprint(group_controller, url_prefix='/api')
app.register_blueprint(publication_controller, url_prefix='/api')
app.register_blueprint(interes_controller, url_prefix='/api')
app.register_blueprint(evento_controller, url_prefix='/api')
app.register_blueprint(influencer_controller, url_prefix='/api')

@app.route('/')
def index():
    return "Consulte la documentación de la API en /api/docs"

if __name__ == "__main__":
    app.run(debug=True)