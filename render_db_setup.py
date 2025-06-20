from microblog import app, db
from app.models import User, Post  # add more if you have them

with app.app_context():
    db.create_all()

