from flask import Flask
from flask_migrate import Migrate

from config import Config
from app.db import db
from app.extensions import login_manager
from app.models.user import User


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # initialize extensions here
    db.init_app(app=app)
    migrate = Migrate(app=app, db=db)
    migrate.init_app(app=app, db=db)
    login_manager.init_app(app)

    # register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.shell_context_processor
    def shell():
        return {
            "db": db,
            "User": User,
        }

    @app.route('/test/')
    def test_page():
        return '<h3>App factory test</h3>'
    
    return app