"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User
# import seed

# User = User()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()
connect_db(app)

# db.create_all()

app.config['SECRET_KEY'] = 'secret_key'

@app.route('/')
def show_users_home():
    """Shows all users"""
    # must get the db to display the users
    users = User.query.all()
    return render_template("home.html", users=users)

@app.route('/new-user')
def create_new_user():
    """Shows new user form and creates a new user from the inputs"""
    # get the input fields from the page
    
    
    return render_template("new-user.html")

# the user detail route must follow that user.id
@app.route('/user-detail/<int:user_id>')
def show_user_details(user_id):
    """Shows the details of the user"""
    user = User.query.get_or_404(user_id)
    return render_template("user-detail.html", user=user)

@app.route('/edit-user')
def show_edit_page():
    """Takes user to the edit page and makes any changes to the db"""
    
    return render_template("edit-user.html")