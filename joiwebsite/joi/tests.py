from pprint import pprint
from django.test import TestCase, Client
import joi.data as data
from munch import munchify
import json

class HomeTestCase(TestCase):
    def setUp(self):
        data.initialize_data()

    def test_1(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(200, response.status_code)


class ResidentTestCase(TestCase):
    def setUp(self):
        data.initialize_data()

    def test_list_resident_by_anonymous(self):
        c = Client()
        response = c.get("/joi/v1/residents/")
        self.assertEqual(401, response.status_code)

    def test_list_resident_by_carepartner_1(self):
        c = Client()
        login_response = c.login(username='cp_1', password='testpassword')
        self.assertEqual(True, login_response)
        response = c.get("/joi/v1/residents/")
        self.assertEqual(200, response.status_code)
        objs = [munchify(o) for o in json.loads(response.content)]
        self.assertEqual(1, len(objs))
        self.assertEqual(str(data.UUID_1), objs[0].resident_id)

    def test_get_resident_1_by_carepartner_1(self):
        c = Client()
        login_response = c.login(username='cp_1', password='testpassword')
        self.assertEqual(True, login_response)
        response = c.get("/joi/v1/residents/00000000-0000-0000-0000-000000000001/")
        self.assertEqual(200, response.status_code)
        obj = munchify(json.loads(response.content))
        self.assertEqual(str(data.UUID_1), obj.resident_id)

    def test_get_resident_2_by_carepartner_1(self):
        c = Client()
        login_response = c.login(username='cp_1', password='testpassword')
        self.assertEqual(True, login_response)
        response = c.get("/joi/v1/residents/00000000-0000-0000-0000-000000000002/")
        self.assertEqual(403, response.status_code)
