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
    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form["image-url"]
    
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
# TODO route for user new post ** method GET 
# *The route should follow the user id to keep that relationship
@app.route('/users/<int:user_id>/posts/new')
def get_new_post_page(user_id):
    """Takes user to the new post page for creating a new post and submit it to the database"""
    user = User.query.get_or_404(user_id)
    
    return render_template("users/posts/new.html", user=user) #*working
    
# TODO route for user post ** method POST*
# *Get values from the page and save them to the database to create a new post
@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    """Creates a new post and saves to the database"""
    return redirect ('/users/posts/detail') 

# TODO route for post detail page
@app.route('/users/posts/<int:post_id>')
def show_post(post_id):
    """Shows user post and allows for them to edit a post"""
    post = Post.query.get_or_404(post_id)
    return render_template("users/posts/detail.html", post=post) #*working

# TODO route for user to edit post ** method GET
@app.route('/users/posts/<int:post_id>/edit')
def create_post(post_id):
    """Takes user to the post editing page"""
    
    post = Post.query.get_or_404(post_id)
    return render_template("users/posts/edit.html", post=post) #*working

# TODO route for user edit ** method POST
# ***get the values from the page for editing and post
@app.route('/users/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Allows user to edit a post and saves edit to the database"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"] or None
    post.content = request.form["content"] or None
    
    db.session.add(post)
    db.session.commit()
    return redirect(f'"/users/posts/{post.user_id}')

# TODO route for user delete ** method POST
@app.route('/users/posts/<int:post_id>', methods=["POST"])
def delete_post(post_id):
    """Allow for user to delete a post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    
    return redirect (f"/users/{post.user_id}")
    
