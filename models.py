"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
DEFAULT_IMAGE_URL = "https://images.unsplash.com/photo-1511367461989-f85a21fda167?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1031&q=80"
 
def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Creates a db for users"""
    __tablename__ = "users"
    """Generates a user table in the database"""
    def __repr__(self):
        """Show infor about user"""
        u= self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url} >"
    
    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True) 
    
    first_name = db.Column(db.Text,
                           nullable = False)
    
    last_name = db.Column(db.Text,
                           nullable = False)
    
    image_url = db.Column(db.Text,
                          nullable=False,
                          default=DEFAULT_IMAGE_URL)
    posts = db.relationship("Post")

    
class Post(db.Model):
    """Generates a table for Post in the database"""
    __tablename__ = "posts"
    
    
    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True) 
    
    title = db.Column(db.String(80),
                      nullable = False)

    content = db.Column(db.Text,
                         nullable=False)

    create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) 
    
    user = db.relationship("User", backref="users")
    
    post_tags = db.relationship('Post'
                                ,secondary='post_tags'
                                ,backref='tags')
    
    def __repr__(self):
        return f"<Post {self.title} {self.content} {self.user_id}>"
    
class PostTag(db.Model):
    """Generates a table for many-to-many relationships"""
    __tablename__ = "post_tags"
    
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    
class Tag(db.Model):
    """Generates a table for post tags"""
    __tablename__ = "tags"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), unique=True)
    
   
def get_user(user_id):
    """Queries the database to retrieve a user by their id"""
    user = User.query.get_or_404(user_id)

    return user

def get_post(post_id):
    """Queries the database to retrieve a post based of of the post id"""
    post = Post.query.get_or_404(post_id)
    
    return post

