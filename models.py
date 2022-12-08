"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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

    
    def display_details(self):
        """Shows the user details"""
        return self.first_name, self.last_name, self.image_url
        
   
    

