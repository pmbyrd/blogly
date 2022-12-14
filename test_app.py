from unittest import TestCase

from app import app
from models import db, User, Post, Tag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

app.app_context().push()
db.drop_all()
db.create_all()

class UserViewTestCase(TestCase):
    """Test for views for Users"""
    def setUp(self):
        """Add a sample User"""
        User.query.delete()
        
        user = User(first_name="Jon", last_name="Doe")
        db.session.add(user)
        db.session.commit()
        
        self.user_id = user.id
        
    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
        
    def test_home_view(self):
        """Test the home view"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"<h1> Users </h1>", html)
 
    
    def test_user_detail(self):
        """Test the user detail view"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/detail")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"""<p class="card-text">Jon Doe</p>""", html)
    
    def test_edit_page(self):
        """TEST the edit page"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"""<label for="first-name" class="form-label">First Name</label>""", html)
            
    def test_new_user(self):
        """Test the new user page"""
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"""<label for="first-name" class="form-label">First Name</label>""", html)
            
class PostViewTestCase(TestCase):
    """Test for views for Posts"""
    def setUp(self):
        """Add a simple post"""
        """Add a sample User"""
        User.query.delete()
        
        user = User(first_name="Jon", last_name="Doe")
        db.session.add(user)
        db.session.commit()
        
        self.user_id = user.id
        
        Post.query.delete()
        post = Post(title="Test Post", content="This is a test post", user_id=1)
        
        db.session.add(post)
        db.session.commit()
        
        self.post_id=post.id  
        
        Tag.query.delete()
        tag = Tag(name="Test_Tag")
        db.session.add(tag)
        db.commit()
        self.tag_id = tag.id
        
    def tearDown(self):
        """Clean up any fouled transaction."""
        
        db.session.rollback() 
        
    def test_post_detail_view(self):
        """Test the post detail view"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"""<h5 class="card-title">Test Post</h5>""", html)
    
    def test_new_post_view(self):
        """Test the new post view"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.post_id}/posts/new")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"""<label for="title" class="form-label">Title</label>""", html)
    
    def test_handle_post(self):
        """Test the handle post view"""
        
        with app.test_client() as client:
            resp = client.post(f"/users/{self.post_id}/posts/new",
                               data={"title": "Test Post", "content": "This is a test post"},
                               follow_redirects=True)
            
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"""<h1>Test Post</h1>""", html)
    
    def test_tag_detail_view(self):
        """Test the tag detail view"""
        
        with app.test_client() as client:
            resp = client.get(f"/tags/{self.tag_id}/detail")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"""<h3 class="card-title">Test_Tag</h3>""", html)