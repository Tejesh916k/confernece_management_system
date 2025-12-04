import unittest
from app import app

class FlaskAppTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Conference', response.data)
    
    def test_login_page(self):
        response = self.client.get('/user/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    # You can add more tests for registration, file upload, etc.

if __name__ == '__main__':
    unittest.main()
