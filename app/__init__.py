from flask import Flask
from config import Config
import os
# from app.extensions import login_manager

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask_login import LoginManager
login_manager = LoginManager()
from flask_migrate import Migrate
migrate = Migrate()
from flask_mail import Mail
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # initialize extensions here
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    login_manager.init_app(app)
    mail.init_app(app)

    # register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.contact import bp as contact_bp
    app.register_blueprint(contact_bp, url_prefix='/contact')

    # shell context moved

    @app.route('/test/')
    def test_page():
        return '<h3>App factory test</h3>'
    
    import logging
    from logging.handlers import SMTPHandler, RotatingFileHandler

    if not app.debug: 
        # if app is running without debug mode
        # email-based error logger
        if app.config['MAIL_SERVER']: 
            # and if mail server exists in config
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Application Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            # only report errors and not warnings, informational or debugging messages
            app.logger.addHandler(mail_handler)
            # attach it to the app.logger object from flask

            # file-based error logger
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240,
                                               backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info('Application startup')
    
    return app