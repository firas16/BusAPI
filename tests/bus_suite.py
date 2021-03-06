import unittest
import json
from app import create_app, db

class BusTestCase(unittest.TestCase):
    """ This class tests the bus class"""

    def setUp(self):
        """ Define test variables and initialize app"""
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.bus = {'name': 'hemla', 'line' : 27}

        # bind the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def register_user(self, email="user@test.com", password="test1234"):
        """This helper method helps register a test user."""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/register', data=user_data)

    def login_user(self, email="user@test.com", password="test1234"):
        """This helper method helps log in a test user."""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=user_data)


    def test_bus_creation(self):
        """ Test creation of a Bus Post request"""

        # register a test user, then log them in
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        ff = data=self.bus
        res = self.client().post('/buses/', headers=dict(Authorization="Bearer " + access_token), data=self.bus)
        self.assertEqual(res.status_code, 201)
        self.assertIn('hemla', str(res.data))

    def test_api_can_get_all_buses(self):
        """Test API can get a bus (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/buses/', headers=dict(Authorization="Bearer " + access_token), data=self.bus)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/buses/', headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('hemla', str(res.data))

    def test_api_can_get_bus_by_id(self):
        """Test API can get a single bus by using it's id."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post('/buses/', headers=dict(Authorization="Bearer " + access_token), data=self.bus)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/buses/{}'.format(result_in_json['id']), headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('hemla', str(result.data))

    def test_buses_can_be_edited(self):
        """Test API can edit an existing bus. (PUT request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post(
            '/buses/',
            headers = dict(Authorization="Bearer " + access_token),
            data={'name': 'hemla', 'line' : 27})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/buses/1',
            headers=dict(Authorization="Bearer " + access_token),
            data={
                "name": "hemla",
                "line": 27
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/buses/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('hemla', str(results.data))

    def test_bus_deletion(self):
        """Test API can delete an existing bus. (DELETE request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post(
            '/buses/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'hemla', 'line' : 27})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/buses/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/buses/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()