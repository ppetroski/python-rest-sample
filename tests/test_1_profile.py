import re
import components.tester as tester
from unittest import TestCase, main as unittest_main


class ProfileTestCase(TestCase):
    def setUp(self):
        self._endpoint = 'http://127.0.0.1:5000/profile'
        self.data = {
            "first_name": "Paul",
            "last_name": "Petroski",
            "email": "Paul.Petroski@hotmail.com",
            "address1": "123 Street",
            "address2": "Suite 123",
            "locality": "New York",
            "state": "New York",
            "postcode": "12345",
            "phone": "321-321-4321",
            "mobile": "123-123-1234"
        }

    def test_1_list(self):
        resp = tester.api_list(self._endpoint)
        self.__class__.start_count = resp['count']

    def test_2_create(self):
        resp = tester.api_create(self._endpoint, self.data)
        self.__class__.record = resp['data']

    def test_3_update(self):
        new_email = 'Paul.Petroski@gmail.com'
        data = {'email': new_email}
        resp = tester.api_update(self._endpoint, self.__class__.record['uuid'], data)
        assert resp['data']['email'] == new_email
        self.__class__.record = resp['data']

    def test_4_validation(self):
        new_email = 'Invalid'
        data = {'email': new_email}
        resp = tester.api_update(self._endpoint, self.__class__.record['uuid'], data, False)
        assert bool(re.match(r'^Value ".+" for column ".+":.+$', resp['data']))

    def test_5_delete(self):
        tester.api_delete(self._endpoint, self.__class__.record['uuid'])

    def test_6_clean_up(self):
        resp = tester.api_list(self._endpoint)
        assert self.__class__.start_count == resp['count']

# Make the tests conveniently executable
if __name__ == '__main__':
    unittest_main()