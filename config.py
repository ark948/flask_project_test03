import os
from dotenv import load_dotenv
from logging.config import dictConfig

basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, '.env'))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-random-secret-key' # change this later
    SECRET_CAPTCHA_KEY = 'some-random-key-for-captcha-dev'
    EXPIRE_SECONDS = 60 * 10 # 10 minutes
    CAPTCHA_IMG_FORMAT = 'JPEG' # JPEG is 3x fatser than png
    CAPTCHA_LENGTH = 6,
    CAPTCHA_DIGITS = False,
    EXCLUDE_VISUALLY_SIMILAR = True,
    BACKGROUND_COLOR = (0, 0, 0),  # RGB(A?) background color (default black)
    TEXT_COLOR = (255, 255, 255), # default white
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 8025)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
    LANGUAGES = ['en', 'fa']
