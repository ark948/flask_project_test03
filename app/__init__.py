from flask import Flask

from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # initialize extensions here

    # register blueprints here

    @app.route('/test/')
    def test_page():
        return '<h3>App factory test</h3>'
    
    return app