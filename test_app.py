import hashlib
import hmac
import unittest
import uuid

from connector import app, generate_token, get_user_id
from datetime import datetime


class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_generate_token(self):
        nonce = uuid.uuid4()
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        userid = app.config['CLIENT_ID']
        usertype = app.config['CLIENT_USERTYPE_NAME']
        token = generate_token(nonce, timestamp, userid, usertype)

        expected_token = hmac.new(
            app.config['SHARED_SECRET'].encode(),
            f"nonce{nonce}timestamp{timestamp}userid{userid}usertype{usertype}".encode(),
            hashlib.sha512
        ).hexdigest()
        self.assertEqual(token, expected_token)

    def test_get_user_id(self):
        user_id = get_user_id("careprovider")
        self.assertEqual(user_id, app.config['CAREPROVIDER_ID'])

        user_id = get_user_id("client")
        self.assertEqual(user_id, app.config['CLIENT_ID'])

    def test_redirect(self):
        response = self.client.get('/?usertype=careprovider')
        self.assertEqual(response.status_code, 302)

        self.assertIn(app.config['BASE_URL'], response.headers['Location'])

        response = self.client.get('/?usertype=client')
        self.assertEqual(response.status_code, 302)
        self.assertIn(app.config['BASE_URL'], response.headers['Location'])

    def test_missing_usertype(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn(app.config['BASE_URL'], response.headers['Location'])

    def test_invalid_usertype(self):
        """
        Test that an invalid usertype results in a 403 Forbidden response.
        """
        invalid_usertype = "invalid_user"
        response = self.client.get(f'/?usertype={invalid_usertype}')
        self.assertEqual(response.status_code, 403)
        self.assertIn("Given usertype isn't valid.", response.data.decode())


if __name__ == '__main__':
    unittest.main()
