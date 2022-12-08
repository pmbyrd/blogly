"""Seed file to make sample data for blogly db."""

from models import User, db
from app import app

# Create all tables
app.app_context().push()

db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add Users

user1 = User(first_name = "Jon", last_name="Snow", image_url="https://randomuser.me/api/portraits/men/17.jpg")
user2 = User(first_name = "Ned", last_name= "Stark", image_url="https://randomuser.me/api/portraits/men/7.jpg")
user3 = User(first_name = "Arya", last_name="Stark", image_url= "https://randomuser.me/api/portraits/women/76.jpg")

# Add new objects to session, so they'll persist
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

# Commit--otherwise, this never gets saved!
db.session.commit()


