from pprint import pprint
from django.test import TestCase, Client
import joi.data as data
from munch import munchify
import json

RESIDENTS_URL = '/joi/v1/residents/'
CAREPARTNER_RESIDENTS_URL = '/joi/v1/carepartnerresidents/'

def create_client(username, password):
    c = Client()
    if username is not None:
        login_response = c.login(username=username, password=password)
        if not login_response:
            raise Exception('Failed to login %s' % (username))
    return c

def response_to_list(response):
    return [munchify(o) for o in json.loads(response.content)]

def response_to_object(response):
    return munchify(json.loads(response.content))

class HomeTestCase(TestCase):
    def setUp(self):
        data.initialize_data()

    def test_1(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(200, response.status_code)

class LoginTestCase(TestCase):
    def setUp(self):
        data.initialize_data()

    def test_carepartner_1(self):
        c = Client()
        login_response = c.login(username='cp_1', password='testpassword')
        self.assertEqual(True, login_response)

    def test_carepartner_2(self):
        c = Client()
        login_response = c.login(username='cp_2', password='testpassword')
        self.assertEqual(True, login_response)

class ResidentTestCase(TestCase):
    def setUp(self):
        data.initialize_data()

    def test_list_resident_by_anonymous(self):
        c = create_client(None,None)
        response = c.get(RESIDENTS_URL)
        self.assertEqual(401, response.status_code)

    ### Care Partner 1 ########################

    def test_list_resident_by_carepartner_1(self):
        c = create_client('cp_1','testpassword')
        response = c.get(RESIDENTS_URL)
        self.assertEqual(200, response.status_code)
        objs = response_to_list(response)
        self.assertEqual(1, len(objs))
        self.assertEqual(str(data.UUID_1), objs[0].resident_id)

    def test_get_resident_1_by_carepartner_1(self):
        c = create_client('cp_1','testpassword')
        response = c.get('%s%s/' % (RESIDENTS_URL,data.UUID_1))
        self.assertEqual(200, response.status_code)
        obj = response_to_object(response)
        self.assertEqual(str(data.UUID_1), obj.resident_id)

    def test_get_resident_2_by_carepartner_1(self):
        c = create_client('cp_1','testpassword')
        response = c.get('%s%s/' % (RESIDENTS_URL,data.UUID_2))
        self.assertEqual(403, response.status_code)

    ### Care Partner 2 ########################

    def test_list_resident_by_carepartner_2(self):
        c = create_client('cp_2','testpassword')
        response = c.get(RESIDENTS_URL)
        self.assertEqual(200, response.status_code)
        objs = response_to_list(response)
        self.assertEqual(1, len(objs))
        self.assertEqual(str(data.UUID_2), objs[0].resident_id)

    def test_get_resident_2_by_carepartner_2(self):
        c = create_client('cp_2','testpassword')
        response = c.get('%s%s/' % (RESIDENTS_URL,data.UUID_2))
        self.assertEqual(200, response.status_code)
        obj = response_to_object(response)
        self.assertEqual(str(data.UUID_2), obj.resident_id)

    def test_get_resident_1_by_carepartner_2(self):
        c = create_client('cp_2','testpassword')
        response = c.get('%s%s/' % (RESIDENTS_URL,data.UUID_1))
        self.assertEqual(403, response.status_code)


class CarePartnerResidentTestCase(TestCase):
    def setUp(self):
        data.initialize_data()

    def test_list_carepartnerresident_by_anonymous(self):
        c = create_client(None,None)
        response = c.get(CAREPARTNER_RESIDENTS_URL)
        self.assertEqual(401, response.status_code)

    ### Care Partner 1 ########################

    def test_list_carepartnerresident_by_carepartner_1(self):
        c = create_client('cp_1','testpassword')
        response = c.get(CAREPARTNER_RESIDENTS_URL)
        self.assertEqual(200, response.status_code)
        objs = response_to_list(response)
        self.assertEqual(1, len(objs))
        self.assertEqual(str(data.UUID_1), objs[0].resident)

    def test_get_carepartnerresident_1_by_carepartner_1(self):
        c = create_client('cp_1','testpassword')
        response = c.get('%s%s/' % (CAREPARTNER_RESIDENTS_URL,data.UUID_1))
        self.assertEqual(200, response.status_code)
        obj = response_to_object(response)
        self.assertEqual(str(data.UUID_1), obj.resident)

    def test_get_carepartnerresident_2_by_carepartner_1(self):
        c = create_client('cp_1','testpassword')
        response = c.get('%s%s/' % (CAREPARTNER_RESIDENTS_URL,data.UUID_2))
        self.assertEqual(403, response.status_code)

    ### Care Partner 2 ########################

    def test_list_carepartnerresident_by_carepartner_2(self):
        c = create_client('cp_2','testpassword')
        response = c.get(CAREPARTNER_RESIDENTS_URL)
        self.assertEqual(200, response.status_code)
        objs = response_to_list(response)
        self.assertEqual(1, len(objs))
        self.assertEqual(str(data.UUID_2), objs[0].resident)

    def test_get_carepartnerresident_2_by_carepartner_2(self):
        c = create_client('cp_2','testpassword')
        response = c.get('%s%s/' % (CAREPARTNER_RESIDENTS_URL,data.UUID_2))
        self.assertEqual(200, response.status_code)
        obj = response_to_object(response)
        self.assertEqual(str(data.UUID_2), obj.resident)

    def test_get_carepartnerresident_1_by_carepartner_2(self):
        c = create_client('cp_2','testpassword')
        response = c.get('%s%s/' % (CAREPARTNER_RESIDENTS_URL,data.UUID_1))
        self.assertEqual(403, response.status_code)        