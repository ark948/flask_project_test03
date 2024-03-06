from flask import Flask
from config import Config
# from app.extensions import login_manager

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask_login import LoginManager
login_manager = LoginManager()
from flask_migrate import Migrate
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # initialize extensions here
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    login_manager.init_app(app)

    # register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    errors_bp.template_folder='errors'

    # shell context moved

    @app.route('/test/')
    def test_page():
        return '<h3>App factory test</h3>'
    
    return app