import os
from app import create_app, db
import unittest
import tempfile
# babel skipped

# all test cases need to subclass from unittest.TestCase

class appTestCase(unittest.TestCase):

    def setUp(self):
        test_config = {}
        self.test_db_file = tempfile.mkstemp()[1] # returns a pair, [1] is probably the filename
        test_config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.test_db_file
        test_config['TESTING'] = True

        self.app = create_app(test_config)
        db.init_app(self.app)
        # babel init skipped
        
        with self.app.app_context():
            db.create_all()

        # register blueprints
        # maybe its only the main blueprint
        from app.main import bp as main_bp
        self.app.register_blueprint(main_bp)

        self.client = self.app.test_client()

    def tearDown(self):
        os.remove(self.test_db_file)

    def test_home(self):
        rv = self.client.get('/')
        self.assertEqual(rv.status_code, 200)