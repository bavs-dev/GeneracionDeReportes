from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from app.config import Config
from dotenv import load_dotenv
from sqlalchemy import text  # <--- AÑADE ESTO AL INICIO

import os

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()

load_dotenv()

def create_app():
    app = Flask(__name__, static_folder="../static")
    app.config.from_object(Config)


    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from app.models.usuario import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."

    # Registrar blueprints
    from app.controllers.auth_controller import auth
    from app.controllers.dashboard import main
    from app.controllers.usuario_controller import usuario_bp  # Importa el Blueprint
    from app.controllers.generacion_ticket_controller import  generacionTicket_bp # importamos el Blueprint
    from app.controllers.generacionDeTicketVistaController import generacionTicketVista_bp
    from flask_login import current_user

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(usuario_bp)  # REGISTRO DEL CRUD DE USUARIOS
    app.register_blueprint(generacionTicket_bp) #
    app.register_blueprint(generacionTicketVista_bp)
    # Inyectar automáticamente 'usuario' en todas las plantillas
    @app.context_processor
    def inyectar_usuario():
        return dict(usuario=current_user)


    # Ruta de inicio con verificación de base de datos
    @app.route('/')
    def index():
        try:
            db.session.execute(text('SELECT 1'))  # <--- ENVUELTO EN text()
            print("✅ Conexión exitosa a la base de datos.")
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(f"❌ Error de conexión a la base de datos: {e}")
            return "<h3>Error al conectar con la base de datos.</h3>"

    return app
