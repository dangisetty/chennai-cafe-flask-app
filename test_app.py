import unittest
from app import app

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        # Creates a test client
        self.client = app.test_client()
        self.client.testing = True

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_products_page(self):
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)

    def test_feedback_submission(self):
        response = self.client.post('/form', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'dish': 'Test Dish',
            'message': 'This is a test message.'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Thank you for your feedback!', response.data)

    def test_order_page(self):
        response = self.client.get('/order')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
