from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

followers = db.Table ('followers',
	db.Column ('follower_id', db.Integer, db.ForeignKey ('user.id')),
	db.Column ('followed_id', db.Integer, db.ForeignKey ('user.id'))
	)

class User (UserMixin, db.Model):
	id = db.Column (db.Integer, primary_key=True)
	username = db.Column (db.String, index=True, unique=True)
	email = db.Column (db.String, index=True, unique=True)
	password_hash = db.Column (db.String (128))
	posts = db.relationship ('Post', backref='author', lazy='dynamic')
	about_me = db.Column (db.String (140))
	last_seen = db.Column (db.DateTime, default=datetime.utcnow)
	followed = db.relationship (
		'User', secondary=followers,
		primaryjoin=(followers.c.follower_id == id),
		secondaryjoin=(followers.c.followed_id == id),
		backref=db.backref ('followers', lazy='dynamic'), lazy='dynamic')

	def __repr__ (self):
		return "<User {}>".format (self.username)

	def set_password (self, password):
		self.password_hash = generate_password_hash (password)

	def check_password (self, password):
		return check_password_hash (self.password_hash, password)

	def avatar (self, size):
		digest = md5 (self.email.lower ().encode ('utf-8')).hexdigest ()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format (
			digest, size)

	def follow (self, user):
		if not self.is_following (user):
			self.followed.append (user)

	def unfollow (self, user):
		if self.is_following (user):
			self.followed.remove (user)

	def is_following (self, user):
		return self.followed.filter (
			followers.c.followed_id == user.id).count () > 0

	def followed_posts (self):
		followed_ids = [user.id for user in self.followed]
		followed_ids.append (self.id)
		return Post.query.filter (Post.user_id.in_ (followed_ids)).order_by (Post.timestamp.desc ())

class Post (db.Model):
	id = db.Column (db.Integer, primary_key=True)
	body = db.Column (db.String (140))
	timestamp = db.Column (db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column (db.Integer, db.ForeignKey ('user.id'))

	def __repr__ (self):
		return '<Post {}>'.format (self.body)