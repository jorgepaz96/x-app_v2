# services/users/project/__init__.py


import os  
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # nuevo

# instanciando la db
db = SQLAlchemy() # nuevo

def create_app(script_info=None):
    # instanciado la app
    app = Flask(__name__)
    
    # establecer configuraicon
    app_settings = os.getenv('APP_SETTINGS')   # Nuevo
    app.config.from_object(app_settings)       # Nuevo

    # configuramos la extencion
    db.init_app(app)

    # registramos blueprints
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    # contecto shell para flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app,'db': db}

    return app
