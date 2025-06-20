from flask import render_template, flash, redirect, url_for, request
from app import app, login, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm, PostForm
from app.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
from datetime import datetime

@login.user_loader
def load_user (id):
	return User.query.get (int (id))

@app.before_request
def before_request ():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow ()
		db.session.commit ()

@app.route ('/')
@app.route ('/index', methods=['GET', 'POST'])
@login_required
def index ():
	form = PostForm ()
	if form.validate_on_submit ():
		post = Post (body=form.post.data, author=current_user)
		db.session.add (post)
		db.session.commit ()
		flash ('Your post is now live!')
		return redirect (url_for ('index'))
	page = request.args.get ('page', 1, type=int)
	posts = db.paginate (
		current_user.followed_posts (), page=page,
		per_page=app.config['POST_PER_PAGE'])
	next_url = url_for ('index', page=posts.next_num) \
		if posts.has_next else None
	prev_url = url_for ('index', page=posts.prev_num) \
		if posts.has_prev else None
	return render_template ('index.html', title='Home', form=form,
		posts=posts.items, prev_url=prev_url, next_url=next_url)

@app.route ('/explore')
@login_required
def explore ():
	page = request.args.get ('page', 1, type=int)
	posts = db.paginate (
		Post.query.order_by (Post.timestamp.desc ()), page=page,
		per_page=app.config['POST_PER_PAGE'])
	next_url = url_for ('explore', page=posts.next_num) \
		if posts.has_next else None
	prev_url = url_for ('explore', page=posts.prev_num) \
		if posts.has_prev else None
	return render_template ('index.html', title='Explore', 
		posts=posts.items, prev_url=prev_url, next_url=next_url)

@app.route ('/login', methods=['GET', 'POST'])
def login ():
	if current_user.is_authenticated:
		return redirect (url_for ('index'))
	form = LoginForm ()
	if form.validate_on_submit ():
		user = User.query.filter_by (username=form.username.data).first ()
		if user is None or not user.check_password (form.password.data):
			flash ('Invalid username or password')
			return redirect (url_for ('login'))
		login_user (user, remember=form.remember_me.data)
		next_page = request.args.get ('next')
		if not next_page or urlparse (next_page).netloc != '':
			next_page = url_for ('index')
		return redirect (next_page)
	return render_template ('login.html', title='Login', form=form)

@app.route ('/logout')
def logout ():
	logout_user ()
	return redirect (url_for ('index'))

@app.route ('/register', methods=['GET', 'POST'])
def register ():
	if current_user.is_authenticated:
		return redirect (url_for ('index'))
	form = RegistrationForm ()
	if form.validate_on_submit ():
		user = User (username=form.username.data, email=form.email.data)
		user.set_password (form.password.data)
		db.session.add (user)
		db.session.commit ()
		flash ('Congratulations {}, you are now a registered user!'.format (form.username.data))
		return redirect (url_for ('login'))
	return render_template ('register.html', title='Register', form=form)

@app.route ('/user/<username>')
@login_required
def user (username):
	user = User.query.filter_by (username=username).first_or_404 ()
	form = EmptyForm ()
	page = request.args.get ('page', 1, type=int)
	posts = db.paginate (
		Post.query.filter_by (user_id=current_user.id).order_by (
		Post.timestamp.desc ()), page=page, per_page=app.config['POST_PER_PAGE'])
	next_url = url_for ('user', username=current_user.username, page=posts.next_num) \
		if posts.has_next else None
	prev_url = url_for ('user', username=current_user.username, page=posts.prev_num) \
		if posts.has_prev else None
	return render_template ('user.html', user=user, form=form, posts=posts.items,
		next_url=next_url, prev_url=prev_url)

@app.route ('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile ():
	form = EditProfileForm (current_user.username)
	if form.validate_on_submit ():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit ()
		flash ('Your changes have been saved.')
		return redirect (url_for ('edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template ('edit_profile.html', title='Edit Profile',
		form=form)

@app.route ('/follow/<username>', methods=['GET', 'POST'])
@login_required
def follow (username):
	form = EmptyForm ()
	if form.validate_on_submit ():
		user = User.query.filter_by (username=username).first ()
		if not user:
			flash ('User {} not found.'.format (username))
			return redirect (url_for ('index'))
		elif user == current_user:
			flash ('You cannot follow yourself.')
			return redirect (url_for ('index'))
		else:
			current_user.follow (user)
			db.session.commit ()
			flash ('You are now following {}'.format (username))
			return redirect (url_for ('user', username=username))
	else:
		return redirect (url_for ('index'))

@app.route ('/unfollow/<username>', methods=['GET', 'POST'])
@login_required
def unfollow (username):
	form = EmptyForm ()
	if form.validate_on_submit ():
		user = User.query.filter_by (username=username).first ()
		if not user:
			flash ('User {} not found.'.format (username))
			return redirect (url_for ('index'))
		elif user == current_user:
			flash ('You cannot unfollow yourself.')
			return redirect (url_for ('index'))
		else:
			current_user.unfollow (user)
			db.session.commit ()
			flash ('You unfollowed {}'.format (username))
			return redirect (url_for ('user', username=username))
	else:
		return redirect (url_for ('index'))