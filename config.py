import os
basedir = os.path.abspath (os.path.dirname (__file__))

class Config:
	SECRET_KEY = os.environ.get ('SECRET_KEY') or 'only-naim-will-guess'
	SQLALCHEMY_DATABASE_URI = os.environ.get ('DATABASE_URI') or \
		'sqlite:///' + os.path.join (basedir, 'app.db')
	SQLALCHEMY_TRACK_MOODIFICATIONS = False

	MAIL_SERVER = os.environ.get ('MAIL_SERVER')
	MAIL_PORT = os.environ.get ('MAIL_PORT') or 25
	MAIL_USE_TLS = os.environ.get ('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get ('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get ('MAIL_PASSWORD')
	ADMINS = ['solve.naim@gmail.com']

	POST_PER_PAGE = 5