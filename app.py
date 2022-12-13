"""Blogly application."""

from flask import Flask, render_template, redirect, request, debughelpers
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Post, PostTag, Tag, get_user, get_post, get_tag
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
    tags = Tag.query.all()
    return render_template('users/home.html', users=users, tags=tags)

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
    tags = Tag.query.all()
    return render_template("posts/new.html", user=user, tags=tags)

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
@app.route('/tags')
def show_all_tags():
    """Shows all tags"""
    tags = Tag.query.all()
    
    return render_template("tags/tags.html", tags=tags)

@app.route('/tags/new')
def show_new_tag_page():
    """Shows page to create a new tag"""
    return render_template("tags/new.html")

@app.route('/tags/new', methods=["POST"])
def handle_new_tag():
    """Handles the creation of a new tag and commits it to the database"""
    name = request.form["tag-name"]
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/detail')
def show_tag_detail(tag_id):
    """List tag other associated posts and allows for user to edit
    or delete that tag"""
    tag = get_tag(tag_id)
    posts = tag.posts
    return render_template("tags/detail.html", tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit')
def show_tag_edit_page(tag_id):
    """Shows page for editing a tag"""
    tag = get_tag(tag_id)
    return render_template("tags/edit.html", tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def handle_tag(tag_id):
    """Handles editing a tag and updating the changes to the database"""
    tag = get_tag(tag_id)
    tag.name = request.form["tag-name"]
    db.session.add(tag)
    db.session.commit()
    
    return redirect(f"/tags/{tag.id}/detail")


@app.route('/tags/<int:tag_id>/delete')
def show_delete_tag_page(tag_id):
    """Shows the delete page for tags"""
    tag = get_tag(tag_id)
    return render_template("tags/delete.html", tag=tag)

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def handle_tag_delete(tag_id):
    """Updates the database once the tag has been deleted"""
    tag = get_tag(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return render_template("tags/delete.html", tag=tag)




