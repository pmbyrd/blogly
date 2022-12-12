# from unittest import TestCase

# from app import app
# from models import db, User, Post, Tag

# # Use test database and don't clutter tests with SQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
# app.config['SQLALCHEMY_ECHO'] = False

# # Make Flask errors be real errors, rather than HTML pages with error info
# app.config['TESTING'] = True

# # This is a bit of hack, but don't use Flask DebugToolbar
# app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# app.app_context().push()
# db.drop_all()
# db.create_all()

# class UserViewTestCase(TestCase):
#     """Test for views for Users"""
#     def setUp(self):
#         """Add a sample Pet"""
#         User.query.delete()
        
#         user = User(first_name="Jon", last_name="Doe")
#         db.session.add(user)
#         db.session.commit()
        
#         self.user_id = user.id
        
#     def tearDown(self):
#         """Clean up any fouled transaction."""
#         db.session.rollback()
        
#     def test_list_pets(self):
#         with app.test.client as client:
#             resp = client.get("/users")
#             html = resp.get_data(as_text=True)
            
#             self.assertEqual(resp.status_code, 200)
#             self.assertIn('Jon', html)        
    