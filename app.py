"""Blogly application."""

from flask import Flask, render_template, redirect, request, debughelpers
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Post
# import seed


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()
connect_db(app)

# db.create_all()
app.config['USE_DEBUGGER'] = True
app.config['SECRET_KEY'] = 'secret_key'

@app.route('/')
def root():
    """Homepage that redirects to all users"""
    return redirect("/users")

@app.route('/users')
def show_users_home():
    """Shows all users"""
    # must get the db to display the users
    users = User.query.all()
    return render_template("users/home.html", users=users)

@app.route('/users/new', methods=["GET"])
def create_new_user():
    """Shows new user form and creates a new user from the inputs"""
    
    return render_template("users/new.html")



# the user detail route must follow that user.id
@app.route('/users/<int:user_id>/detail')
def show_user_details(user_id):
    """Shows the details of the user"""
    user = User.query.get_or_404(user_id)
    # todo add the post to the page
    posts = Post.query.filter_by(user_id=user_id)
    return render_template("users/detail.html", user=user, posts=posts)

@app.route('/users/new', methods=["POST"])
def create_user():
    """Gets the new user details from the page and post them to the db"""
    # get the user inputs from the form if user input are vaild show that new user
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]
    user = User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(user)
    db.session.commit()
    # import pdb; pdb.set_trace()
    return redirect("/users")

@app.route('/users/<int:user_id>/edit')
def get_edit_page(user_id):
    """Takes the user to the edit page"""
    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Edits user and updates database"""
    user = User.query.get_or_404(user_id)
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]
    
    db.session.add(user)
    db.session.commit()
    
    return redirect("/users")
    
    
@app.route('/users/<int:user_id>/delete')
def get_delete_page(user_id):
    """Takes user to the delete page"""
    user = User.query.get_or_404(user_id)
    return render_template("users/delete.html", user=user)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')


# **Establish the post routes **

# the route need the user so the relationship stays connected
@app.route('/users/posts/new')
def show_post_page():
    """Shows the post page and form for making a new post"""
    
    return render_template("users/posts/new.html")


# @app.route('/posts/<int:post_id>')
# def show_user_post():
#     """A Page that shows the users post and buttons to edit or delete a post"""
#     return render_template("posts/detail.html")

# @app.route('/posts/<int:post_id>/detail', methods=["POST"])
# def edit_post():
#     """Allows user to edit post"""
#     return redirect('/posts/detail')

# @app.route('/posts/<int:post_id>')
# def edit_post(post_id):
#     """Allows user to edit post"""
#     return render_template("usess/posts/edit.html")
    