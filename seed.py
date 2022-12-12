"""Seed file to make sample data for blogly db."""

from models import User,Post, Tag, PostTag, db
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

p1 = Post(title="Test 1", content="Hello, hello", user_id=1)
p2 = Post(title="Test 2", content="Hey, hey", user_id=1)
p3 = Post(title="Test 3", content="Hello, hello", user_id=2)
p4 = Post(title="Test 4", content="Hey, hey", user_id=2)
p5 = Post(title="Test 5", content="Hello, hello", user_id=3)
p6 = Post(title="Test 6", content="Hey, hey", user_id=3)

t1 = Tag(name="tech")
t2 = Tag(name="food")
t3 = Tag(name="cool")
t4 = Tag(name="random")
# Add new objects to session, so they'll persist
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.commit()

db.session.add_all([t1,t2,t3,t4])
db.session.commit()

db.session.add_all([p1,p2,p3,p4, p5,p6])
db.session.commit()

# Commit--otherwise, this never gets saved!


