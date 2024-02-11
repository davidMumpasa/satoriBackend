import unittest
import requests

# Replace this URL with your actual server URL
BASE_URL = "http://127.0.0.1:5000"

# Test data
valid_user_email = "david@fluidintellect.com"
invalid_user_email = "nonexistent@domain.com"


class TestLoginEndpoint(unittest.TestCase):

    def test_successful_login(self):
        data = {'email': valid_user_email, 'password': 'DavidEbula$16'}
        response = requests.post(f"{BASE_URL}/login", json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Login successful')

    # def test_login_missing_user_email(self):
    #     response = requests.post(f"{BASE_URL}/login", json={})
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json()['error'], 'Missing required fields')

    # def test_login_invalid_user_email(self):
    #     data = {'email': invalid_user_email, 'password': 'DavidEbula$16'}
    #     response = requests.post(f"{BASE_URL}/login", json=data)

    #     try:
    #         self.assertEqual(response.status_code, 404)
    #         self.assertEqual(response.json()['error'], 'User not found')
    #     except AssertionError:
    #         print("Response content:", response.content)
    #         raise


if __name__ == '__main__':
    unittest.main()
