"""Blogly application."""

from flask import Flask, render_template, redirect, request, debughelpers
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Post, PostTag, Tag, get_user, get_post
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
def show_all_users():
    """Shows all users"""
    users = User.query.all()
    return render_template('users/home.html', users=users)

@app.route('/users/new')
def show_new_user():
    """Shows form for creating a new user"""
    return render_template("users/new.html")

@app.route('/users/new', methods=["POST"])
def handle_new_user_form():
    """Handles the creaation of a new user an post to database and 
    redirects user back to home page"""
    # *Get the values from the page for submission
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users') #TODO fix redirect to go to user detail

@app.route('/users/<int:user_id>/detail')
def show_user(user_id):
    """Shows user details"""
    user = get_user(user_id)
 
    return render_template("users/detail.html", user=user)
 
    
@app.route('/users/<int:user_id>/edit')
def show_user_edit_page(user_id):
    """Shows the user edit page"""
    user = get_user(user_id)
    return render_template("users/edit.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def handle_user_edit(user_id):
    """Edits user information and updates the database"""
    user = get_user(user_id)
    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form["image-url"]
    
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete')
def show_delete_page(user_id):
    """Shows the deleted page"""
    user = get_user(user_id)
    return render_template("users/delete.html", user=user)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes a user from the database"""
    user = get_user(user_id)
    db.session.delete(user)
    db.session.commit()
    return render_template("users/delete.html")
  
# *******Implement routes for user posts
@app.route('/users/<int:user_id>/posts/new')
def show_new_post_page(user_id):
    """Shows page for creating a new post"""
    user = get_user(user_id)
    return render_template("posts/new.html", user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def handle_post(user_id):
    """Handles a new post, submits to the database and add it to the user account"""
    user = get_user(user_id)
    title = request.form["title"]
    content = request.form["content"] 
    new_post = Post(title=title, content=content, user_id=user_id)   
    db.session.add(new_post)
    db.session.commit()
    
    return redirect('/users')


@app.route('/users/<int:post_id>/posts/detail')
def show_user_post(post_id):
    """Shows all of a user's post"""
    
    post = get_post(post_id)
    user = post.user
    return render_template("posts/detail.html", post=post, user=user)
    
@app.route('/posts/<int:post_id>/edit')
def show_post_edit_page(post_id):
    """Takes user to the edit post page"""
    
    post = get_post(post_id)
    return render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_post_edit(post_id):
    """Handles an edit of a post and updates it to the database"""
    post = get_post(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    db.session.add(post)
    db.session.commit()
    post_id = post.user.id
    
    return redirect(f"/users/{post.id}/posts/detail")

# TODO Routes for tags

