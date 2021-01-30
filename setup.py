# Purpose: Using the context of the app, initialize the database tables

from app import app
from models import db

with app.app_context():
    db.create_all()
