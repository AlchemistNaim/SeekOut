import os
basedir = os.path.abspath (os.path.dirname (__file__))

class Config:
	SECRET_KEY = os.environ.get ('SECRET_KEY') or 'only-naim-will-guess'
	uri = os.getenv("DATABASE_URL", "sqlite:///app.db")
	if uri.startswith("postgres://"):
	    uri = uri.replace("postgres://", "postgresql://", 1)
	if 'render.com' in uri:
    uri += '?sslmode=require'
	SQLALCHEMY_DATABASE_URI = uri
	SQLALCHEMY_TRACK_MOODIFICATIONS = False

	MAIL_SERVER = os.environ.get ('MAIL_SERVER')
	MAIL_PORT = os.environ.get ('MAIL_PORT') or 25
	MAIL_USE_TLS = os.environ.get ('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get ('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get ('MAIL_PASSWORD')
	ADMINS = ['solve.naim@gmail.com']

	POST_PER_PAGE = 5