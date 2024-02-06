import unittest
from flask import json
from main import app, db

class TestRegistrationAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_successful_registration(self):
        data = {
            'email': 'test@example.com',
            'password': 'StrongPass123!'
        }

        response = self.app.post('/register', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.get_data(as_text=True))['user'], 'Registered Successfully')

    def test_missing_required_fields(self):
        data = {
            'email': 'test@example.com',
            # 'password': 'StrongPass123!'  # Missing password field
        }

        response = self.app.post('/register', json=data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(json.loads(response.get_data(as_text=True))['error'], 'Missing required fields')

    def test_weak_password_registration(self):
        data = {
            'email': 'test@example.com',
            'password': 'weakpass'  # Weak password
        }

        response = self.app.post('/register', json=data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(json.loads(response.get_data(as_text=True))['error'], 'Weak password. Password must be strong.')

    def test_existing_user_registration(self):
        # Add a user to the database
        existing_user_data = {
            'email': 'existing_user@example.com',
            'password': 'StrongPass123!'
        }
        self.app.post('/register', json=existing_user_data)

        # Try to register the same user again
        response = self.app.post('/register', json=existing_user_data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(json.loads(response.get_data(as_text=True))['error'], 'You have Already Registered')

    def test_successful_registration_check_db(self):
        data = {
            'email': 'test@example.com',
            'password': 'StrongPass123!'
        }

        self.app.post('/register', json=data)

        # Check if the user is added to the database
        from models.user import UserModel
        user = UserModel.query.filter_by(email=data['email']).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.password, 'StrongPass123!')  # You may need to adjust this based on your actual implementation

if __name__ == '__main__':
    unittest.main()
