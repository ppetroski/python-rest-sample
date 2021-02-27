import re
import components.tester as tester
from unittest import TestCase, main as unittest_main


class InteractionTestCase(TestCase):
    def setUp(self):
        self._endpoint = 'http://127.0.0.1:5000/interaction'
        self.data = {
            "pid_Profile": 1,
            "type": "email",
            "outcome": "no answer"
        }

    def test_1_list(self):
        resp = tester.api_list(self._endpoint)
        self.__class__.start_count = resp['count']

    def test_2_create(self):
        resp = tester.api_create(self._endpoint, self.data)
        self.__class__.record = resp['data']

    def test_3_update(self):
        new_outcome = 'no response'
        data = {'outcome': new_outcome}
        resp = tester.api_update(self._endpoint, self.__class__.record['uuid'], data, False)
        assert resp['data']['outcome'] == new_outcome.upper()
        self.__class__.record = resp['data']

    def test_4_validation(self):
        new_outcome = 'Invalid'
        data = {'outcome': new_outcome}
        resp = tester.api_update(self._endpoint, self.__class__.record['uuid'], data, False)
        assert bool(re.match(r'^Value ".+" for column ".+":.+$', resp['data']))

    def test_4a_exception(self):
        data = {
            'pid_Profile': 91919191,
            'outcome': 'no response'
        }
        resp = tester.api_update(self._endpoint, self.__class__.record['uuid'], data, False)
        assert bool(re.match(r'^Unexpected error:', resp['data']))

    def test_5_delete(self):
        tester.api_delete(self._endpoint, self.__class__.record['uuid'])

    def test_6_clean_up(self):
        resp = tester.api_list(self._endpoint)
        assert self.__class__.start_count == resp['count']


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest_main()
