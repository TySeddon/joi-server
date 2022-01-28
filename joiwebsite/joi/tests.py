from django.test import TestCase, Client
import joi.data as data

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

    def careparter_1(self):
        c = Client()
        login_response = c.login(username='cp_1', password='testpassword')
        self.assertEqual(True, login_response)
        response = c.get("/")
        self.assertEqual(200, response.status_code)
